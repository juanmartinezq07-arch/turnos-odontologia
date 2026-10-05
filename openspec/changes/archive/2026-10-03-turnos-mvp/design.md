# Design

## Context

Greenfield: no hay `app/` ni specs previas. Ver `proposal.md` (Why) para la motivación. Estado actual: solo KB, `CHANGES.md` (C-01) y `discovery/discovery.md`. Constraints que fijan el enfoque: RN02 como invariante en Postgres (la validación de aplicación no cierra la ventana de carrera), TDD estricto contra Postgres real, API pura sin frontend, guest sin auth, notificaciones mock, Ley 25.326 (solo datos ficticios). Ver specs `turnos`, `disponibilidad`, `reservas-guest`, `agenda` y `plataforma-mvp` para el comportamiento exigible.

## Goals / Non-Goals

**Goals:**

- Cerrar la carrera de doble reserva en la base (doble EXCLUDE parcial) con error 409 tipificado por constraint.
- Mantener reglas RN01/RN03/RN04/RN05 como funciones puras en `app/domain/rules.py`, testeables sin DB ni FastAPI.
- Dejar routers finos que delegan a `app/application/` y `main.py` solo como cableado, según layout KB-08.
- Cerrar IN-01 (RN05) dentro del change con decisión documentada.

**Non-Goals:**

- Frontend, panel admin, Celery/Redis, ficha clínica, WhatsApp real, pagos, multi-sucursal, OAuth/JWT completo, rate-limit distribuido.

## Decisions

### D-01 — Postgres como árbitro de RN02 (doble EXCLUDE parcial)

Doble `EXCLUDE USING gist` (`profesional_id WITH =` y `sillon_id WITH =` sobre `tstzrange(inicio, fin) WITH &&`) con `WHERE (estado = 'activo')` + `CHECK (fin > inicio)`; `CREATE EXTENSION IF NOT EXISTS btree_gist` primero; Alembic 001 tablas, 002 constraints; migraciones numeradas nunca editadas una vez aplicadas. Alternativa descartada: solo validación en Python (deja ventana de carrera entre check e insert; dos POST concurrentes crearían doble reserva). La app pre-valida para dar 409 claro, pero la base decide.

### D-02 — RN05 como índice único parcial funcional

`CREATE UNIQUE INDEX ... ON turno (paciente_id, (inicio::date)) WHERE estado='activo'`. Alternativa descartada: solo validación en aplicación (repite la ventana de carrera de RN02 para el mismo paciente). Cierra IN-01. El mapeo por nombre de constraint distingue `RN05` de `RN02_*`.

### D-03 — Capas finas: routers → application → domain; `rules.py` puras

`app/api/v1/` valida Pydantic y delega; `app/application/bookings.py` y `availability.py` orquestan transacciones; `app/domain/rules.py` expone RN01/RN03/RN04/RN05 como funciones puras (cálculo de `fin`, chequeo de pasado/horario, transición de cancelación, chequeo un-activo/día). Alternativa descartada: lógica en routers (acopla HTTP al dominio y rompe TDD puro).

### D-04 — `timestamptz` + `TZ_CONSULTORIO`, cliente nunca manda `fin`

Todo `datetime` timezone-aware; RN03 compara contra `now()` en `America/Argentina/Buenos_Aires`; schemas con `extra='forbid'` y sin campo `fin` en requests. Alternativa descartada: naive datetimes (rompe RN03 en cambios de hora y ambigüedad de zona).

### D-05 — Auth mínima por API keys + guest acotado

`app/core/security.py` valida `API_KEY_RECEPCION` / `API_KEY_ODONTOLOGO` por env; odontólogo solo lee su agenda (403 ajena); guest solo `GET /disponibilidad`, `POST /reservas`, `POST /reservas/{token}/cancelacion` + catálogos, con rate-limit en memoria 10/min (`RESERVA_RATE_LIMIT`). Alternativa descartada: JWT/OAuth (quema horas sin aportar al invariante evaluado).

### D-06 — Errores por nombre de constraint, nunca parseo de mensaje

Middleware traduce `IntegrityError` a 409 inspeccionando el nombre del constraint violado (`RN02_PROFESIONAL` / `RN02_SILLON` / `RN05`); Pydantic → 422; forma estable `{code, message}`. Alternativa descartada: parsear el texto del error de Postgres (frágil ante versiones/locales).

### D-07 — Notificación mock best-effort post-commit

`NotificationService` (abc) + `MockNotificationService` (`NOTIF_BACKEND=mock`); llamada tras commit en `try/except` con log, sin rollback. Alternativa descartada: notificar dentro de la transacción o de forma bloqueante (un fallo del canal tumbaría la agenda).

### D-08 — Disponibilidad como función determinista

`availability.py` computa huecos desde `HorarioAtencion` menos activos, recortando por duración RN01 y `now()`; misma entrada → misma salida. Alternativa descartada: cachear slots (invalidez compleja sin beneficio en MVP).

### D-09 — Reprogramación como cancelar+crear en una transacción

Un solo `BEGIN/COMMIT`: marca original `cancelado` e inserta el nuevo; cualquier violación → rollback total. Alternativa descartada: dos operaciones separadas (puede perder el turno original o duplicar).

### D-10 — Sillón auto-asignado al primero libre dentro de la transacción

Si `POST /reservas` omite `sillon_id`, el servicio itera sillones activos intentando el insert hasta el primer commit exitoso; si ninguno libera, 409 `RN02_SILLON`. Cierra la pregunta media de `10_preguntas_abiertas.md`.

## Risks / Trade-offs

- [Risk] Contención de writes bajo EXCLUDE (lock de rango) → Mitigación: MVP de 2–10 profesionales, sin optimización prematura; documentado como límite conocido.
- [Risk] `tstzrange` y zona horaria en el índice funcional RN05 (`inicio::date` depende de TZ) → Mitigación: fijar `TZ_CONSULTORIO` y computar la fecha en esa zona tanto en índice como en validación; test con borde de medianoche.
- [Risk] Rate-limit en memoria no escala multi-instancia → Mitigación: deuda documentada; suficiente para demo local de un proceso.
- [Risk] Token de cancelación opaco filtrado equivale a acceso → Mitigación: tokens aleatorios de alta entropía, únicos, solo entregados al creador; sin listado público.
- [Risk] Revisión línea por línea del `docker-compose.yml` (precaución High Risk `docker-patterns`) → Mitigación: Compose mínimo (un servicio `db`, imagen pineada, sin secretos commiteados, puerto solo localhost); checkpoint de revisión humana en tasks.
- [Risk] Datos de pacientes (Ley 25.326) → Mitigación: `PacienteGuest` solo contacto mínimo, rechazo 422 de campos clínicos, seeds/tests/docs solo ficticios.

## Migration Plan

1. `docker compose up db` (servicio `db` con healthcheck `pg_isready`).
2. `alembic upgrade head`: 001 crea tablas + `btree_gist`; 002 agrega doble EXCLUDE + `CHECK` + índice RN05.
3. Seed ficticio (profesionales, sillones, prestaciones, horario, 1 activo + 1 cancelado).
4. Deploy API (un proceso; `DATABASE_URL`, `TZ_CONSULTORIO`, `NOTIF_BACKEND=mock`, API keys por env).
5. Rollback: `alembic downgrade -1` (002) y luego base; nunca editar migración aplicada; ante EXCLUDE en datos legacy, limpiar solapamientos antes de re-aplicar.

## Open Questions

- Ninguna que cambie specs, enfoque o tasks. Deuda registrada para fase 2: consentimiento Ley 25.326 Art. 5.1 como entidad persistida (en MVP solo documentado, sin dato clínico), rate-limit distribuido, y normalización de idioma de anexos de research (IN-01/IN-02 de `10_preguntas_abiertas.md` no bloquean este change).

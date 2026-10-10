# Design

## Context

Greenfield: solo KB, `CHANGES.md` (C-01) y Discovery. Alcance acotado a CU01: alta de turno con prevención de solapamientos (RN02); RN01/RN03 solo como soporte del flujo. Constraints que fijan el enfoque: RN02 como invariante en Postgres (la validación de aplicación no cierra la ventana de carrera), TDD estricto contra Postgres real, API pura sin frontend, Ley 25.326 (solo datos ficticios). Ver specs `turnos` y `plataforma-mvp` para el comportamiento exigible.

## Goals / Non-Goals

**Goals:**

- Cerrar la carrera de doble reserva en la base (doble EXCLUDE parcial) con error 409 tipificado por constraint.
- Mantener RN01/RN03 como funciones puras en `app/domain/rules.py`, testeables sin DB ni FastAPI.
- Dejar routers finos que delegan a `app/application/` y `main.py` solo como cableado, según layout KB-08.
- Demostrar concurrencia real: dos altas concurrentes al mismo slot → una 201 + una 409.

**Non-Goals:**

- Reserva guest, cancelación, reprogramación, agenda, catálogos públicos, notificaciones (mock o reales), frontend, panel admin, Celery/Redis, ficha clínica, pagos, multi-sucursal, OAuth/JWT.

## Decisions

### D-01 — Postgres como árbitro de RN02 (doble EXCLUDE parcial)

Doble `EXCLUDE USING gist` (`profesional_id WITH =` y `sillon_id WITH =` sobre `tstzrange(inicio, fin) WITH &&`) con `WHERE (estado = 'activo')` + `CHECK (fin > inicio)`; `CREATE EXTENSION IF NOT EXISTS btree_gist` primero; Alembic 001 tablas, 002 constraints; migraciones numeradas nunca editadas una vez aplicadas. Alternativa descartada: solo validación en Python (deja ventana de carrera entre check e insert; dos POST concurrentes crearían doble reserva). La app pre-valida para dar 409 claro, pero la base decide.

### D-02 — Capas finas: routers → application → domain; `rules.py` puras

`app/api/v1/turnos.py` valida Pydantic y delega; `app/application/bookings.py` orquesta la transacción de alta; `app/domain/rules.py` expone RN01/RN03 como funciones puras (cálculo de `fin`, chequeo de pasado/horario). Alternativa descartada: lógica en routers (acopla HTTP al dominio y rompe TDD puro).

### D-03 — `timestamptz` + `TZ_CONSULTORIO`, cliente nunca manda `fin`

Todo `datetime` timezone-aware; RN03 compara contra `now()` en `America/Argentina/Buenos_Aires`; schemas con `extra='forbid'` y sin campo `fin` en requests. Alternativa descartada: naive datetimes (rompe RN03 en cambios de hora y ambigüedad de zona).

### D-04 — Auth mínima por API key de recepcionista

`app/core/security.py` valida `API_KEY_RECEPCION` por env en `POST /turnos`; sin credencial → 401. Alternativa descartada: JWT/OAuth (quema horas sin aportar al invariante evaluado).

### D-05 — Errores por nombre de constraint, nunca parseo de mensaje

Middleware traduce `IntegrityError` a 409 inspeccionando el nombre del constraint violado (`RN02_PROFESIONAL` / `RN02_SILLON`); Pydantic → 422; forma estable `{code, message}`. Alternativa descartada: parsear el texto del error de Postgres (frágil ante versiones/locales).

## Risks / Trade-offs

- [Risk] Contención de writes bajo EXCLUDE (lock de rango) → Mitigación: MVP de pocos profesionales, sin optimización prematura; documentado como límite conocido.
- [Risk] Revisión línea por línea del `docker-compose.yml` (precaución High Risk `docker-patterns`) → Mitigación: Compose mínimo (un servicio `db`, imagen pineada, sin secretos commiteados, puerto solo localhost); checkpoint de revisión humana en tasks.
- [Risk] Datos de pacientes (Ley 25.326) → Mitigación: `PacienteGuest` solo contacto mínimo, rechazo 422 de campos clínicos, seeds/tests/docs solo ficticios.

## Migration Plan

1. `docker compose up db` (servicio `db` con healthcheck `pg_isready`).
2. `alembic upgrade head`: 001 crea tablas + `btree_gist`; 002 agrega doble EXCLUDE + `CHECK`.
3. Seed ficticio mínimo (profesionales, sillones, prestaciones, horario).
4. Deploy API (un proceso; `DATABASE_URL`, `TZ_CONSULTORIO`, API key por env).
5. Rollback: `alembic downgrade -1` (002) y luego base; nunca editar migración aplicada; ante EXCLUDE en datos legacy, limpiar solapamientos antes de re-aplicar.

## Open Questions

- Ninguna que cambie specs, enfoque o tasks. Deuda registrada para trabajo futuro: reserva guest (CU02), cancelación/reprogramación (CU03), agenda (CU04), RN04/RN05, consentimiento Ley 25.326 Art. 5.1 como entidad persistida.

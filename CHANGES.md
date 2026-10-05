# CHANGES — Secuencia de Implementación

> Índice canónico de todos los changes del proyecto **TurnosAR (turnos-odontologia)**.
> Cada change es atómico: un agente puede implementarlo en una sesión (~4-6 horas).
> **Leer este archivo antes de ejecutar cualquier `/opsx:propose`.**

> **Nota de alcance (cátedra — Change OPSX 25% = 1 change):** este roadmap contiene
> **un único change** (`C-01 turnos-mvp`) que cubre CU01 (agendar recepcionista) +
> CU02 (reserva guest online) encadenadas, con RN01–RN05 como núcleo y CU03/CU04
> en alcance mínimo operable. Decisión registrada en Discovery (`change_scope`).

---

## Cómo usar este documento

1. Identificar el change a implementar (verificar que sus dependencias están en `openspec/changes/archive/`).
2. Leer los docs de la knowledge-base indicados en "Leer antes".
3. Ejecutar `/opsx:propose turnos-mvp`.
4. Al terminar el change, archivarlo con `/opsx:archive turnos-mvp`.
5. Marcar el checkbox `[x]` en este archivo.

---

## Árbol de dependencias

```
C-01 turnos-mvp                         ← único change (sin dependencias)
```

### Paralelismo por fase

> Cada "gate" es un punto de sincronización. Los changes dentro de un grupo pueden ejecutarse en paralelo.

```
GATE 0: ninguna
  → C-01 turnos-mvp (solo — un integrante, sin paralelismo real)
```

### Camino crítico (1 change — mínimo irreducible)

```
C-01
```

### Plan óptimo con 3 agentes

```
Paso │ Agente A (Backend Core) │ Agente B (Backend Aux) │ Agente C (Frontend)
─────┼─────────────────────────┼────────────────────────┼─────────────────────────
  1  │ C-01 turnos-mvp         │         —              │         —
```

> Con un solo change y un solo integrante no hay paralelismo explotable.
> La tabla se mantiene por contrato de formato. P0-sys = API/backend puro, sin frontend.

---

## FASE 0 — MVP Turnos (única fase)

> Sin forks ni gates intermedios: todo el MVP vive en un solo change demostrable.

### [C-01] `turnos-mvp`
- **Estado**: `[x]` archivado (`openspec/changes/archive/2026-10-03-turnos-mvp/`)
- **Scope**: MVP API puro FastAPI + PostgreSQL 16 con invariante RN02 en persistencia (CU01 + CU02, CU03/CU04 mínimo operable)
  - `docker-compose.yml`: servicio `db` Postgres 16 con extensión `btree_gist` habilitada
  - `alembic/versions/`: Migración 001 tablas (`profesional`, `sillon`, `prestacion`, `paciente_guest`, `turno`, `horario_atencion`); Migración 002 doble `EXCLUDE USING gist` (`profesional_id WITH =`, `sillon_id WITH =`, `tstzrange(inicio, fin) WITH &&`) `WHERE (estado = 'activo')` + `CHECK (fin > inicio)`
  - Modelos: `Profesional`, `Sillon`, `Prestacion`, `PacienteGuest` (solo contacto, sin DNI/clínico), `Turno` (`inicio`, `fin = inicio + duracion prestacion`, `estado activo/cancelado`, `token_cancelacion`, `cancelled_at`), `HorarioAtencion` (global + por profesional)
  - `app/domain/rules.py`: RN01 (cálculo `fin`), RN03 (pasado vs `now()` en `America/Argentina/Buenos_Aires` + horario), RN04 (cancelar = `UPDATE estado`), RN05 (máx. 1 activo por paciente/día — cierra IN-01 de `10_preguntas_abiertas.md`: índice parcial o validación + test) como funciones puras testeables
  - `POST /turnos` (US-001, con API key recepcionista): crea turno, calcula `fin` por RN01; 409 `RN02_PROFESIONAL`/`RN02_SILLON`/`RN05`, 422 pasado/fuera de horario; notificación mock best-effort sin bloquear persistencia
  - `GET /disponibilidad?profesional_id=&fecha=&prestacion_id=` (US-002): huecos desde `HorarioAtencion` menos turnos activos, respeta duración RN01, determinista
  - `POST /reservas` (US-003, público sin auth + rate-limit en memoria `10/min`): mismas validaciones que US-001, devuelve 201 + `token_cancelacion`; `sillon_id` opcional con auto-asignación al primero libre
  - `POST /reservas/{token}/cancelacion` (US-004 guest): cancela solo la reserva propia; `DELETE/PATCH /turnos/{id}` para recepcionista; reprogramación atómica transaccional (US-005): si el destino choca, rollback y el original sigue activo
  - `GET /agenda?profesional_id=&fecha=` (US-006, API key odontólogo, solo agenda propia, 403 ajena): activos ordenados por `inicio` con prestación/sillón/paciente; cancelados solo con `?incluir_cancelados=true`
  - `GET /profesionales`, `/sillones`, `/prestaciones` (lectura pública mínima para armar la reserva) + `GET /docs`, `/openapi.json`
  - `app/notifications/`: `NotificationService` (abc) + `MockNotificationService` (registra, no envía; `NOTIF_BACKEND=mock`)
  - `app/core/security.py`: auth mínima por rol (API keys por env `API_KEY_RECEPCION` / `API_KEY_ODONTOLOGO`); middleware traduce `IntegrityError` por EXCLUDE → 409 con código de regla, nunca 500; Pydantic → 422; rechazo explícito de campos clínicos con 422
  - Seed MVP: 2–3 profesionales, 2 sillones, 3 prestaciones (30/45/90 min), horario Lun–Vie 9–18 + Sáb 9–12, 1 turno activo + 1 cancelado de ejemplo; `.env.example` con `DATABASE_URL`, `TZ_CONSULTORIO`, rate-limit (sin secretos reales)
  - Tests: `test_rn02_solapamiento.py` (borde que se toca `[)` no choca, doble eje profesional/sillón, cancelado libera slot), `test_rn02_concurrencia.py` (2 `POST` concurrentes al mismo slot → una 201 + otra 409, contra Postgres real), `test_reserva_guest.py` (e2e guest + cancelación con token + RN05 un activo/día)
- **Dependencias**: ninguna
- **Governance**: MEDIO (lógica de negocio + invariante de concurrencia RN02; checkpoints por ser el núcleo evaluado. No escala a CRITICO/ALTO: guest sin auth real, notificaciones mock, sin pagos/facturación/ficha clínica en MVP)
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Turno (EXCLUDE x2, `btree_gist`, borde `[)`, RN05)
  - `knowledge-base/05_reglas_de_negocio.md` §RN02 (invariante central) + §Excepciones globales (409/422, mock best-effort)
  - `knowledge-base/06_funcionalidades.md` §US-001 + §US-003 (criterios de aceptación del núcleo)
  - `knowledge-base/07_flujos_principales.md` §Flujo 1 + §Flujo 2 (secuencia reserva/alta, casos de error concurrente)
  - `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios + §Seguridad (auth mínima, rate-limit, env vars)

---

## Checklist de validación al cerrar

- [x] El header dice "CHANGES — Secuencia de Implementación".
- [x] La sección "Cómo usar este documento" tiene los 5 pasos numerados.
- [x] El "Árbol de dependencias" usa ASCII art con `└──` y `│`. (N/A trivial: un solo nodo, sin ramas — formato conservado por contrato.)
- [x] Hay al menos un GATE por cada fork de paralelismo detectado. (GATE 0 único: sin forks en un roadmap de 1 change.)
- [x] El camino crítico tiene una flecha lineal sin ramas. (`C-01`.)
- [x] La tabla de "Plan óptimo con 3 agentes" tiene 3 columnas y los pasos enumerados.
- [x] Cada change tiene exactamente 5 campos: Estado, Scope, Dependencias, Governance, Leer antes.
- [x] Cada "Leer antes" tiene 3 a 5 archivos KB con sección cuando aplique. (5 archivos.)
- [x] El Scope tiene bullets operacionales (modelos, endpoints, migraciones, tests).
- [x] Cada Governance tiene uno de los 4 niveles: BAJO, MEDIO, ALTO, CRITICO. (MEDIO — ver justificación en el change.)
- [x] Los changes están agrupados en FASES con nombres semánticos (no "Fase 1, 2, 3" pelados). (FASE 0 — MVP Turnos.)

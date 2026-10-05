# Proposal

## Why

Los consultorios gestionan la agenda en cuadernos/planillas y coordinan por WhatsApp informal, lo que produce solapamientos de profesional y de sillón/box que ninguna validación de interfaz puede impedir bajo concurrencia. Este change crea el MVP de TurnosAR: una API pura donde el no-solapamiento (RN02) es un invariante en PostgreSQL, demostrable con tests reales de concurrencia.

## What Changes

- `POST /turnos` (recepcionista con API key): alta con cálculo servidor de `fin` (RN01), validación RN03/RN05, doble EXCLUDE RN02, notificación mock best-effort.
- `GET /disponibilidad?profesional_id=&fecha=&prestacion_id=`: cómputo determinista de huecos desde `HorarioAtencion` menos turnos activos.
- `POST /reservas` público sin auth (rate-limit 10/min en memoria) + `sillon_id` opcional con auto-asignación al primero libre; devuelve 201 + `token_cancelacion`.
- `POST /reservas/{token}/cancelacion` (guest, solo propia) + `DELETE/PATCH /turnos/{id}` (recepcionista) + reprogramación atómica transaccional con rollback total si el destino choca.
- `GET /agenda?profesional_id=&fecha=` (odontólogo, solo propia, 403 ajena; cancelados solo con `?incluir_cancelados=true`).
- Catálogos mínimos de lectura (`GET /profesionales`, `/sillones`, `/prestaciones`) + `/docs` y `/openapi.json`.
- Persistencia: Postgres 16 (`db`, `btree_gist`), Alembic 001 (tablas) + 002 (doble EXCLUDE parcial + `CHECK (fin > inicio)`), semántica `[)`; RN05 como índice parcial o validación + test (cierra IN-01).
- Transversal: auth mínima por API keys en env, error estable `{code, message}` (`IntegrityError` EXCLUDE → 409 `RN02_PROFESIONAL`/`RN02_SILLON`/`RN05`, nunca 500; Pydantic → 422; campo clínico → 422), `NotificationService` mock best-effort, seed ficticio, `docker-compose.yml`, `.env.example` con placeholders.
- Tests obligatorios contra Postgres real: `test_rn02_solapamiento.py`, `test_rn02_concurrencia.py`, `test_reserva_guest.py`.

## Capabilities

### New Capabilities

- `turnos`: alta por recepcionista, cancelación y reprogramación atómica; RN01/RN02/RN03/RN04/RN05 aplicadas a `POST /turnos` y `DELETE/PATCH /turnos/{id}`.
- `disponibilidad`: consulta determinista de huecos por profesional/fecha/prestación.
- `reservas-guest`: reserva pública sin auth, auto-asignación de sillón, token de cancelación, rate-limit y RN05 guest.
- `agenda`: lectura de agenda del odontólogo con autorización por agenda propia y filtro de cancelados.
- `plataforma-mvp`: invariante RN02 en persistencia, auth mínima, formato de errores, notificaciones mock, seed ficticio, catálogos, Compose y variables de entorno.

### Modified Capabilities

- Ninguna (repo sin specs previas; primer change).

## Impact

- Nuevo código: `app/` (layout KB-08), `alembic/versions/` (001 + 002), `tests/` (3 archivos obligatorios), `docker-compose.yml`, `.env.example`, seed ficticio.
- Nueva API: `POST /turnos`, `GET /disponibilidad`, `POST /reservas`, `POST /reservas/{token}/cancelacion`, `DELETE/PATCH /turnos/{id}`, `GET /agenda`, catálogos, `/docs`.
- Dependencias nuevas: FastAPI 0.110+, Pydantic v2, SQLAlchemy 2.0, Alembic 1.13+, Postgres 16 + `btree_gist`, pytest 8 + httpx 0.27+.
- Sistemas afectados: ninguno existente (greenfield). Non-goals explícitos: sin frontend, sin Celery/Redis, sin ficha clínica, sin WhatsApp real, sin pagos.

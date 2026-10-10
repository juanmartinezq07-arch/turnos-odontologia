# Proposal

## Why

Los consultorios gestionan la agenda en cuadernos/planillas y coordinan por WhatsApp informal, lo que produce solapamientos de profesional y de sillón/box que ninguna validación de interfaz puede impedir bajo concurrencia. Este change implementa una sola funcionalidad, el ejemplo de la consigna: crear un turno evitando solapamientos por profesional y por sillón/box, con la invariante RN02 viviendo en PostgreSQL y demostrable con tests reales de concurrencia.

## What Changes

- `POST /turnos` (recepcionista con API key): alta con cálculo de `fin` en el servidor (RN01), validación temporal y de horario (RN03, solo como soporte del flujo) y doble EXCLUDE RN02 con 409 tipificado por eje.
- Persistencia: Postgres 16 (`db`, `btree_gist`), Alembic 001 (tablas) + 002 (doble EXCLUDE parcial `WHERE estado='activo'` + `CHECK (fin > inicio)`), semántica `[)` (borde que se toca no choca).
- Transversal: auth mínima por API key en env, error estable `{code, message}` (`IntegrityError` EXCLUDE → 409 `RN02_PROFESIONAL`/`RN02_SILLON`, nunca 500; Pydantic → 422; campo clínico → 422), seed ficticio mínimo, `docker-compose.yml`, `.env.example` con placeholders.
- Tests contra Postgres real: `test_rn02_solapamiento.py` (borde `[)`, doble eje) y `test_rn02_concurrencia.py` (2 `POST` concurrentes al mismo slot → una 201 + otra 409).

## Capabilities

### New Capabilities

- `turnos`: alta por recepcionista con RN01/RN02/RN03 aplicadas a `POST /turnos`.
- `plataforma-mvp`: invariante RN02 en persistencia, auth mínima, formato de errores, seed ficticio, Compose y variables de entorno.

### Modified Capabilities

- Ninguna (primer change; las capabilities `disponibilidad`, `reservas-guest` y `agenda` de la versión anterior quedan retiradas por recorte de alcance: CU02/CU03/CU04 son trabajo futuro).

### Explicitly Out of Scope

- Reserva pública guest (CU02), cancelación y reprogramación (CU03), agenda del odontólogo (CU04), catálogos públicos, notificaciones, pagos, ficha clínica, frontend.

## Impact

- Nuevo código: `app/` (layout KB-08 reducido al flujo de alta), `alembic/versions/` (001 + 002), `tests/` (2 archivos), `docker-compose.yml`, `.env.example`, seed ficticio mínimo.
- Nueva API: `POST /turnos`, `/docs`, `/openapi.json`.
- Dependencias nuevas: FastAPI 0.110+, Pydantic v2, SQLAlchemy 2.0, Alembic 1.13+, Postgres 16 + `btree_gist`, pytest 8 + httpx 0.27+.
- Sistemas afectados: ninguno existente (greenfield). Non-goals explícitos: sin guest, sin cancelación, sin agenda, sin catálogos, sin notificaciones, sin frontend, sin ficha clínica, sin pagos.

# Tasks

## 1. Base e infraestructura local

- [x] 1.1 Crear `docker-compose.yml` (solo servicio `db`, `postgres:16` pineada, volumen nombrado, healthcheck `pg_isready`, puerto solo localhost) y `.env.example` (placeholders `DATABASE_URL`, `TZ_CONSULTORIO`, `API_KEY_RECEPCION`) y verificar con `docker compose config` + revisión humana línea por línea
- [x] 1.2 Crear layout KB-08 reducido al flujo de alta (`app/main.py` factory solo cableado, `app/core/config.py`, `app/core/security.py`, `app/domain/`, `app/application/`, `app/api/v1/turnos.py`, `app/schemas/`, `alembic/`, `tests/`) con `pyproject.toml` y verificar importando `app.main` sin errores
- [x] 1.3 Configurar `core/config.py` (solo env vars) + `core/security.py` (API key recepcionista) + `.gitignore` (`.env`, `__pycache__/`) y verificar que ningún secreto real queda commiteado

## 2. Modelos y persistencia con invariante RN02

- [x] 2.1 RED: escribir `tests/test_rn02_solapamiento.py` (borde `[)` no choca, doble eje profesional/sillón) en rojo contra Postgres real y verificar que falla por tablas inexistentes
- [x] 2.2 GREEN: implementar `app/domain/models.py` (Profesional, Sillon, Prestacion, PacienteGuest solo contacto, Turno, HorarioAtencion, `timestamptz`) + Alembic 001 (tablas, `btree_gist` primero) y verificar `alembic upgrade head` crea las tablas en `db`
- [x] 2.3 GREEN: implementar Alembic 002 (doble EXCLUDE parcial `WHERE estado='activo'` + `CHECK (fin > inicio)`) y verificar `test_rn02_solapamiento.py` pasa en verde contra `db` real
- [x] 2.4 REFACTOR: middleware de errores `{code, message}` (`IntegrityError` → 409 por nombre de constraint `RN02_PROFESIONAL`/`RN02_SILLON`, nunca 500; Pydantic → 422) y verificar forzando un doble insert que responde 409 con `code` correcto

## 3. Reglas puras RN01/RN03 + alta (US-001)

- [x] 3.1 RED: tests puros de `app/domain/rules.py` (RN01 calcula `fin`, RN03 pasado vs `now()` en `America/Argentina/Buenos_Aires` + fuera de horario) sin DB y verificar que fallan sin el módulo
- [x] 3.2 GREEN: implementar `rules.py` (funciones puras, `snake_case` + type hints, sin FastAPI ni DB) y verificar que los tests puros pasan
- [x] 3.3 Implementar `POST /turnos` (recepcionista, schemas `extra='forbid'` sin campo `fin`, delega a `application/bookings.py`) y verificar 201 feliz + 409 por eje + 422 pasado/fuera-horario + 422 con campo `fin` o clínico, con asserts por `code`

## 4. Concurrencia real

- [x] 4.1 RED: escribir `tests/test_rn02_concurrencia.py` (2 `POST` concurrentes al mismo slot → una 201 + otra 409, contra Postgres real, sin mocks de DB) y verificar que falla sin el endpoint
- [x] 4.2 GREEN: verificar `test_rn02_concurrencia.py` pasa en verde con el EXCLUDE como árbitro (la base decide, no la app)

## 5. Seed mínimo + verificación integral y cierre

- [x] 5.1 Crear seed ficticio mínimo (profesionales, sillones, prestaciones 30/45/90, horario Lun–Vie 9–18 + Sáb 9–12; nombres Demo, `11-0000-0000`, `@example.com`) + servir `/docs` y `/openapi.json`
- [x] 5.2 Correr suite completa (`pytest` + `openspec validate --strict`) y verificar los 2 archivos de test en verde y asserts por `code` en todos los 409/422
- [x] 5.3 Checkpoint governance MEDIO: revisar TDD ordenado (RN01→RN03→RN02 secuencial→RN02 concurrencia), semántica `[)`, `datetime` aware en todo el flujo y checklist de cierre de `CHANGES.md` listo para `/opsx:archive`

## Explícitamente fuera de este change (trabajo futuro)

- Reserva guest pública (CU02), cancelación/reprogramación (CU03), agenda del odontólogo (CU04), catálogos públicos, notificaciones, RN04/RN05.

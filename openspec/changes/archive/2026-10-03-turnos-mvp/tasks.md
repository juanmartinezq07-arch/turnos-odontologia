# Tasks

## 1. Base e infraestructura local

- [x] 1.1 Crear `docker-compose.yml` (solo servicio `db`, `postgres:16` pineada, volumen nombrado, healthcheck `pg_isready`, puerto solo localhost) y `.env.example` (placeholders `DATABASE_URL`, `TZ_CONSULTORIO`, `NOTIF_BACKEND`, `API_KEY_*`, `RESERVA_RATE_LIMIT`) y verificar con `docker compose config` + revisión humana línea por línea (checkpoint High Risk, sin `up` sin confirmación)
- [x] 1.2 Crear layout KB-08 (`app/main.py` factory solo cableado, `app/core/config.py`, `app/core/security.py`, `app/domain/`, `app/application/`, `app/notifications/`, `app/api/v1/`, `app/schemas/`, `alembic/`, `tests/`) con `pyproject.toml` (FastAPI, Pydantic v2, SQLAlchemy 2.0, Alembic, pytest, httpx) y verificar importando `app.main` sin errores
- [x] 1.3 Configurar `core/config.py` (solo env vars) + `core/security.py` (API keys recepcionista/odontólogo, guest público) + `.gitignore` (`.env`, `__pycache__/`, `.atl/`) y verificar que ningún secreto real queda commiteado (`git status` + grep de valores reales)

## 2. Modelos y persistencia con invariante RN02

- [x] 2.1 RED: escribir `tests/test_rn02_solapamiento.py` (borde `[)` no choca, doble eje profesional/sillón, cancelado libera) en rojo contra Postgres real y verificar que falla por tablas inexistentes
- [x] 2.2 GREEN: implementar `app/domain/models.py` (Profesional, Sillon, Prestacion, PacienteGuest solo contacto, Turno, HorarioAtencion, `timestamptz`) + Alembic 001 (tablas, `btree_gist` primero) y verificar `alembic upgrade head` crea las tablas en `db`
- [x] 2.3 GREEN: implementar Alembic 002 (doble EXCLUDE parcial `WHERE estado='activo'` + `CHECK (fin > inicio)` + índice parcial RN05 `D-02`) y verificar `test_rn02_solapamiento.py` pasa en verde contra `db` real
- [x] 2.4 REFACTOR: middleware de errores `{code, message}` (`IntegrityError` → 409 por nombre de constraint `RN02_PROFESIONAL`/`RN02_SILLON`/`RN05`, nunca 500; Pydantic → 422) y verificar forzando un doble insert que responde 409 con `code` correcto (assert por `code`, no solo status)

## 3. Reglas puras RN01/RN03 + alta y disponibilidad (US-001/US-002)

- [x] 3.1 RED: tests puros de `app/domain/rules.py` (RN01 calcula `fin`, RN03 pasado vs `now()` en `America/Argentina/Buenos_Aires` + fuera de horario) sin DB y verificar que fallan sin el módulo
- [x] 3.2 GREEN: implementar `rules.py` (funciones puras, `snake_case` + type hints, sin FastAPI ni DB) y verificar que los tests puros pasan
- [x] 3.3 Implementar `POST /turnos` (recepcionista, schemas `extra='forbid'` sin campo `fin`, delega a `application/bookings.py`, notify mock best-effort post-commit) y verificar 201 feliz + 409 por eje + 422 pasado/fuera-horario + 422 con campo `fin` o clínico, con asserts por `code`
- [x] 3.4 Implementar `GET /disponibilidad` determinista (`application/availability.py`: horario menos activos, duración RN01, sin pasado) + `GET /profesionales`, `/sillones`, `/prestaciones` y verificar doble consulta idéntica + hueco ocupado ausente + cancelado presente

## 4. Cancelación y reprogramación atómica (US-004/US-005)

- [x] 4.1 Implementar cancelación recepcionista (`DELETE/PATCH /turnos/{id}` → `UPDATE estado='cancelado'`) con notificación mock y verificar que el slot liberado responde 201 a un alta nueva y que re-cancelar es idempotente (409/422 sin doble efecto)
- [x] 4.2 Implementar reprogramación transaccional (cancelar+crear en un `BEGIN/COMMIT`, rollback total si el destino viola RN02/RN03/RN05) y verificar que un destino ocupado responde 409 y el original sigue `activo`

## 5. Reserva guest pública + concurrencia real (US-003)

- [x] 5.1 RED: escribir `tests/test_rn02_concurrencia.py` (2 `POST` concurrentes al mismo slot → una 201 + otra 409, contra Postgres real, sin mocks de DB) y verificar que falla sin el endpoint
- [x] 5.2 GREEN: implementar `POST /reservas` (público, mismas validaciones que US-001, `sillon_id` opcional con auto-asignación al primero libre en transacción `D-10`, devuelve 201 + `token_cancelacion`, rate-limit en memoria 10/min → 429) y verificar `test_rn02_concurrencia.py` pasa en verde
- [x] 5.3 Implementar `POST /reservas/{token}/cancelacion` (solo token propio, 404/403 ajeno) y escribir `tests/test_reserva_guest.py` (e2e guest + cancelación con token + RN05 un activo/día + rechazo clínico 422) y verificar que pasa en verde

## 6. Agenda del odontólogo + notificaciones + seed (US-006)

- [x] 6.1 Implementar `GET /agenda` (odontólogo solo propia, 403 ajena, orden por `inicio` con prestación/sillón/paciente, cancelados solo con `?incluir_cancelados=true`) y verificar 200 ordenada + 403 ajena + filtro de cancelados
- [x] 6.2 Implementar `notifications/interface.py` + `mock.py` (`NOTIF_BACKEND=mock`, best-effort `try/except` sin rollback) cableado en todas las escrituras y verificar que un fallo del mock deja el turno persistido con 201
- [x] 6.3 Crear seed ficticio (2–3 profesionales, 2 sillones, 3 prestaciones 30/45/90, horario Lun–Vie 9–18 + Sáb 9–12, 1 activo + 1 cancelado; nombres "Juan Pérez Demo", `11-0000-0000`, `@example.com`) + servir `/docs` y `/openapi.json` y verificar arranque demo sin datos reales (`grep` de DNI/clínico en repo da vacío)

## 7. Verificación integral y cierre

- [x] 7.1 Correr suite completa (`pytest` + `openspec validate --strict`) y verificar los 3 archivos obligatorios en verde, determinismo de disponibilidad y asserts por `code` en todos los 409/422
- [x] 7.2 Checkpoint governance MEDIO: revisar TDD ordenado (RN01→RN03→RN02sec→RN04→RN05→RN02conc→guest→agenda), semántica `[)`, `datetime` aware en todo el flujo y `diff AGENTS.md CLAUDE.md` vacío, y verificar checklist de cierre de `CHANGES.md` listo para `/opsx:archive`

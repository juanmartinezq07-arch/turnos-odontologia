# Proposal

## Why

El odontólogo necesita consultar su agenda diaria de turnos asignados (`GET /agenda?profesional_id=&fecha=`) ordenados cronológicamente con detalle de prestación (incluyendo su duración según RN01), sillón y datos de contacto del paciente para organizar su jornada (US-006 / CU04), garantizando por RBAC (`KB-03`) que cada odontólogo solo pueda ver su propia agenda (`403` ante agenda ajena) y que los turnos cancelados queden excluidos salvo filtro explícito (`?incluir_cancelados=true`).

## What Changes

- Actualizar `backend/app/core/security.py` y `backend/.env.example` para soportar la autenticación y autorización de agenda con `API_KEY_ODONTOLOGO` (`require_odontologo`), verificando que el odontólogo solo acceda a su propia agenda (mediante `X-Profesional-Id` coincidente con `profesional_id`, devolviendo `403` con código `AGENDA_AJENA` en caso contrario) y permitiendo lectura global a `API_KEY_RECEPCION` según la matriz RBAC de `KB-03`.
- Crear `backend/app/schemas/agenda.py` con los schemas Pydantic v2 (`ConfigDict(extra="forbid")`) para los ítems de la agenda: `AgendaPrestacionOut` (con `duracion_min` visible por RN01), `AgendaSillonOut`, `AgendaPacienteOut` (contacto mínimo Ley 25.326) y `AgendaTurnoOut`.
- Crear `backend/app/application/agenda.py` con el caso de uso `consultar_agenda_dia(session, profesional_id, fecha, incluir_cancelados=False)` que consulta los turnos del día en la zona horaria del consultorio (`America/Argentina/Buenos_Aires`), excluyendo cancelados por defecto y ordenando por `inicio` ascendente.
- Crear el router `backend/app/api/v1/agenda.py` con `GET /agenda` y registrarlo en `backend/app/main.py`.
- Agregar `backend/tests/test_agenda_odontologo.py` cubriendo orden por `inicio`, exclusión por defecto e inclusión explícita de cancelados (`?incluir_cancelados=true`), rechazo `403` en agenda ajena, `401` sin credencial válida y `422` ante fecha inválida contra PostgreSQL 16 real.

## Capabilities

### New Capabilities
- `agenda`: Consulta autenticada de la agenda diaria por profesional y fecha (`GET /agenda`) con RBAC de odontólogo (solo agenda propia → `403` en ajena) y filtro explícito de turnos cancelados.

### Modified Capabilities

## Impact

- **Nuevos archivos**: `backend/app/schemas/agenda.py`, `backend/app/application/agenda.py`, `backend/app/api/v1/agenda.py`, `backend/tests/test_agenda_odontologo.py`.
- **Archivos modificados**: `backend/app/core/security.py`, `backend/app/main.py`, `backend/.env.example`, `backend/tests/conftest.py`.
- **Base de datos**: Sin nuevas migraciones Alembic (opera sobre las tablas `turno`, `profesional`, `sillon`, `prestacion` y `paciente_guest` existentes).

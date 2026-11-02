# Tasks

## 1. RED — Tests de agenda del odontólogo y autorización RBAC que fallan antes de implementar

- [x] 1.1 Configurar `API_KEY_ODONTOLOGO` en `backend/tests/conftest.py` y `backend/.env.example`, y crear `backend/tests/test_agenda_odontologo.py` con tests unitarios de schemas (`extra="forbid"`, presencia en `/openapi.json`) y tests de integración contra PostgreSQL 16 (orden por `inicio` con prestación/`duracion_min`/sillón/paciente, exclusión por defecto de cancelados e inclusión con `?incluir_cancelados=true`, `403` `AGENDA_AJENA` al pedir agenda ajena con `API_KEY_ODONTOLOGO`, `401` sin credencial, `422` con fecha inválida), verificando que fallen en RED.

## 2. GREEN — Seguridad RBAC, schemas, caso de uso y router HTTP

- [x] 2.1 Actualizar `require_odontologo` en `backend/app/core/security.py` para validar `API_KEY_ODONTOLOGO` con coincidencia de `X-Profesional-Id == profesional_id` (`403` `AGENDA_AJENA` si es ajena) y permitir lectura global a `API_KEY_RECEPCION`, devolviendo `401` si falta o es inválida la API key.
- [x] 2.2 Crear `backend/app/schemas/agenda.py` con `AgendaPrestacionOut`, `AgendaSillonOut`, `AgendaPacienteOut` y `AgendaTurnoOut` (`ConfigDict(extra="forbid")`) y `backend/app/application/agenda.py` con `consultar_agenda_dia(session, profesional_id, fecha, incluir_cancelados=False)`.
- [x] 2.3 Crear `backend/app/api/v1/agenda.py` con `GET /agenda` y registrar el router en `backend/app/main.py`, verificando que `pytest tests/test_agenda_odontologo.py` pase completo en verde.

## 3. Verificación integral y regresión

- [x] 3.1 Ejecutar la suite completa `pytest` desde `backend/` contra PostgreSQL 16 y verificar que todos los tests existentes más los nuevos de `test_agenda_odontologo.py` pasen en verde sin regresiones.

## Workflow follow-up

- Archivar el change con `/openspec-archive-change` una vez completadas y verificadas las tasks.
- Marcar `[x]` en `C-27` dentro de `CHANGES.md`.

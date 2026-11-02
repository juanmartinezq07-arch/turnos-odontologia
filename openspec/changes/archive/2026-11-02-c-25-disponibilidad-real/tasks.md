# Tasks

## 1. RED — Tests de disponibilidad (función pura + API HTTP) que fallan antes de implementar

- [x] 1.1 Crear `backend/tests/test_disponibilidad.py` con tests unitarios puros para `rules.calcular_slots_disponibles` (huecos correctos, bloque que no entra completo al final del horario, borde `[)` no pisa activos, descarte de slots en el pasado con `now` inyectado, determinismo) y tests de integración para `GET /disponibilidad` contra PostgreSQL 16 (200 sin credencial, turno activo resta hueco, turno cancelado no resta hueco, determinismo en dos llamadas seguidas, presencia en `/openapi.json`), verificando que fallen en RED.

## 2. GREEN — Regla pura, servicio de disponibilidad, schema y router HTTP

- [x] 2.1 Implementar la función pura `calcular_slots_disponibles` en `backend/app/domain/rules.py` y verificar que los tests unitarios puros de `test_disponibilidad.py` pasen en verde.
- [x] 2.2 Crear `backend/app/schemas/disponibilidad.py` con `SlotDisponibilidadOut` (`ConfigDict(extra="forbid")`) y `backend/app/application/availability.py` con `consultar_disponibilidad(session, profesional_id, fecha, prestacion_id, ahora=None)` consultando `HorarioAtencion` y turnos `activos`.
- [x] 2.3 Crear `backend/app/api/v1/disponibilidad.py` con el endpoint público `GET /disponibilidad?profesional_id=&fecha=&prestacion_id=` y registrar el router en `backend/app/main.py`, verificando que `pytest tests/test_disponibilidad.py` pase completo en verde.

## 3. Verificación integral y regresión

- [x] 3.1 Ejecutar la suite completa `pytest` desde `backend/` contra PostgreSQL 16 y verificar que todos los tests existentes más los nuevos de `test_disponibilidad.py` pasen en verde sin regresiones.

## Workflow follow-up

- Archivar el change con `/openspec-archive-change` una vez completadas y verificadas las tasks.
- Marcar `[x]` en `C-25` dentro de `CHANGES.md`.

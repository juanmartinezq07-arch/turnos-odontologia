# Tasks

## 1. Schemas y Lógica de Aplicación

- [x] 1.1 Crear el schema `TurnoReprogramar` en `backend/app/schemas/turno.py` con `inicio: datetime`, `sillon_id: uuid.UUID | None = None` y `extra="forbid"`.
- [x] 1.2 Implementar la función `reprogramar_turno` en `backend/app/application/bookings.py` manejando validación de estado activo, transacción única y rollback ante conflictos.

## 2. Endpoint y Suite de Pruebas

- [x] 2.1 Exponer `POST /turnos/{turno_id}/reprogramacion` en `backend/app/api/v1/turnos.py` con `require_recepcion` y retorno `TurnoOut`.
- [x] 2.2 Escribir y verificar test del **Escenario 1 (Reprogramación exitosa)** en `backend/tests/test_reprogramacion_api.py::test_reprogramacion_exitosa`, comprobando original cancelado y nuevo activo con notificaciones.
- [x] 2.3 Escribir y verificar test del **Escenario 2 (Rollback atómico ante colisión RN02/RN05)** en `backend/tests/test_reprogramacion_api.py::test_reprogramacion_conflicto_destino_rollback_total`, comprobando 409 y que en base de datos el turno original sigue activo.
- [x] 2.4 Escribir y verificar test del **Escenario 3 (Validaciones de error 404, 409 turno no activo, 422 pasado y 401)** en `backend/tests/test_reprogramacion_api.py::test_reprogramacion_errores_validacion`.

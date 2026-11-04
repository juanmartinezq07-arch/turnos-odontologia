# Tasks

## 1. Contrato de Salida y Caso de Uso de Cancelación (`RN04`)

- [ ] 1.1 Extender `TurnoOut` en `backend/app/schemas/turno.py` agregando `cancelled_at: datetime | None = None` y actualizar `_out(turno)` en `backend/app/api/v1/turnos.py`, verificando que los tests existentes de `POST /turnos` siguen pasando (`pytest backend/tests/test_turnos_api.py`).
- [ ] 1.2 Implementar `cancelar_turno(session: AsyncSession, turno_id: uuid.UUID) -> Turno` en `backend/app/application/bookings.py` (lanzando `NotFound("NO_ENCONTRADO", ...)` si no existe, preservando `cancelled_at` si ya está `cancelado`, o seteando `estado="cancelado"`, `cancelled_at=_ahora()`, `commit()` y `notify_turn_updated` *best-effort*), verificando mediante test en `backend/tests/test_cancelacion_api.py`.

## 2. Endpoint HTTP y Verificación de Escenarios (TDD contra PostgreSQL 16 real)

- [ ] 2.1 Exponer `POST /turnos/{turno_id}/cancelacion` (`response_model=TurnoOut`, `status_code=200`, protegido con `Depends(require_recepcion)`) en `backend/app/api/v1/turnos.py`, verificando su presencia en `/openapi.json`.
- [ ] 2.2 Escribir y ejecutar el test del **Escenario 1 (Funcionamiento esperado + liberación de slot RN04)** en `backend/tests/test_cancelacion_api.py::test_cancelar_turno_libera_slot_y_notifica`, comprobando que tras `POST /turnos/{id}/cancelacion` (200 OK con `estado == "cancelado"` y `cancelled_at` no nulo) se registra la notificación mock y un nuevo `POST /turnos` al mismo horario/profesional/sillón/paciente responde `201 Created`.
- [ ] 2.3 Escribir y ejecutar el test del **Escenario 2 (Errores de negocio 404 y 401)** en `backend/tests/test_cancelacion_api.py::test_cancelar_turno_inexistente_404_y_sin_auth_401`, comprobando que un UUID inexistente devuelve `404` con `code == "NO_ENCONTRADO"` y una petición sin `X-API-Key` devuelve `401`.
- [ ] 2.4 Escribir y ejecutar el test del **Escenario 3 (Caso de borde: Idempotencia)** en `backend/tests/test_cancelacion_api.py::test_cancelar_turno_idempotente_conserva_cancelled_at`, comprobando que dos llamadas consecutivas a `POST /turnos/{id}/cancelacion` responden `200 OK`, mantienen el mismo `cancelled_at` original y no duplican la notificación.

## Workflow follow-up

- Ejecutar la suite completa de tests contra PostgreSQL 16 real y archivar el change con `/opsx:archive` una vez verificado.

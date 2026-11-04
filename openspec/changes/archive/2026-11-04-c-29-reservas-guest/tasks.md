# Tasks: C-29 Reservas Guest

## 1. Schemas y Aplicación

- [x] 1.1 Crear schemas `ReservaCreate` y `ReservaOut` en `backend/app/schemas/reserva.py` con `extra="forbid"`.
- [x] 1.2 Implementar lógica de auto-asignación de sillón y creación de reserva guest con emisión de `token_cancelacion` en `backend/app/application/reservas.py`.
- [x] 1.3 Implementar lógica de cancelación por token con idempotencia en `backend/app/application/reservas.py`.

## 2. API y Protección

- [x] 2.1 Implementar rate limiter en memoria para endpoint de reservas (`backend/app/core/rate_limit.py`).
- [x] 2.2 Exponer endpoints `POST /reservas` y `POST /reservas/{token}/cancelacion` en `backend/app/api/v1/reservas.py` y montarlos en `create_app()`.

## 3. Pruebas Strict TDD

- [x] 3.1 Test del **Escenario 1 (Happy Path y autoasignación de sillón)**: `backend/tests/test_reservas_guest_api.py::test_reserva_exitosa_autoasigna_sillon_y_emite_token`.
- [x] 3.2 Test del **Escenario 2 (Cancelación por token e idempotencia)**: `backend/tests/test_reservas_guest_api.py::test_cancelacion_por_token_libera_slot_e_idempotente`.
- [x] 3.3 Test del **Escenario 3 (Concurrencia real 201 vs 409)**: `backend/tests/test_reservas_guest_api.py::test_concurrencia_reservas_guest_ultimo_slot`.
- [x] 3.4 Test de **Errores de validación y Ley 25.326**: `backend/tests/test_reservas_guest_api.py::test_reserva_guest_errores_y_ley_25326` (token inexistente 404, campo extra 422, rate limit 429).

# Spec Delta: Reservas Públicas Guest

## ADDED Requirements

### Requirement: Alta de reserva pública guest (US-003, RN01, RN02)

El sistema SHALL exponer `POST /reservas` como endpoint público sin requerir cabeceras de autenticación. Debe aceptar datos de contacto, profesional, prestación, horario de inicio y opcionalmente sillón. Si el sillón no se especifica, el sistema SHALL auto-asignar el primer sillón disponible para el intervalo. El sistema SHALL generar y persistir un `token_cancelacion` único, retornando `201 Created` con el turno y su token.

#### Scenario: Reserva exitosa auto-asigna sillón y emite token_cancelacion

- **WHEN** un paciente guest solicita `POST /reservas` con un slot disponible sin enviar `sillon_id`
- **THEN** el sistema responde `201 Created` con el turno asignado a un sillón disponible, `estado = 'activo'`, y un `token_cancelacion` no nulo ni vacío

#### Scenario: Concurrencia real en reservas guest al último slot disponible

- **WHEN** dos solicitudes `POST /reservas` concurrentes compiten por el único sillón y slot disponible para un profesional
- **THEN** exactamente una solicitud responde `201 Created` y la otra responde `409` (`RN02_SILLON` o `RN02_PROFESIONAL`), garantizado por la exclusión atómica de PostgreSQL

### Requirement: Cancelación de reserva pública mediante token (US-004, RN04)

El sistema SHALL exponer `POST /reservas/{token}/cancelacion` como endpoint público. Si el token existe y corresponde a un turno, el sistema SHALL pasar su estado a `'cancelado'`, registrar `cancelled_at = now()`, emitir notificación *best-effort* y liberar el slot. Si el turno ya estaba cancelado, la operación SHALL ser idempotente respondiendo `200 OK` con el `cancelled_at` original. Si el token no existe, SHALL responder `404` con `code = "NO_ENCONTRADO"`.

#### Scenario: Cancelación por token libera el slot y es idempotente

- **WHEN** el paciente envía `POST /reservas/{token}/cancelacion` con un token válido de un turno activo
- **THEN** el sistema responde `200 OK` con `estado = 'cancelado'`, `cancelled_at` registrado, libera el slot para nuevas reservas y llamadas posteriores con el mismo token responden `200 OK` conservando el mismo timestamp

#### Scenario: Cancelación con token inexistente devuelve 404

- **WHEN** se invoca `POST /reservas/{token}/cancelacion` con un token que no existe en el sistema
- **THEN** el sistema responde `404` con `{"code": "NO_ENCONTRADO", "message": "..."}`

### Requirement: Protección ante abuso y rechazo de datos clínicos (Ley 25.326)

El sistema SHALL rechazar con `422` cualquier intento de inyección de campos no permitidos (`extra="forbid"`), garantizando la protección de datos personales. Asimismo, el sistema SHALL limitar las solicitudes a `POST /reservas` a un máximo configurable (10 solicitudes por minuto), respondiendo `429` ante exceso de peticiones.

#### Scenario: Intento de reserva con campos clínicos adicionales es rechazado con 422

- **WHEN** una petición `POST /reservas` incluye un campo no admitido como `obra_social` o `diagnostico`
- **THEN** el sistema responde `422` y no persiste el paciente ni el turno

#### Scenario: Exceso de solicitudes dispara rate limit 429

- **WHEN** un cliente supera el límite de 10 reservas por minuto
- **THEN** el sistema responde `429` con `{"code": "RATE_LIMIT_EXCEEDED", "message": "..."}`

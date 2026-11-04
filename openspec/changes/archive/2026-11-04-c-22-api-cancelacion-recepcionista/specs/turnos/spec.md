# Spec Delta

## ADDED Requirements

### Requirement: Cancelación de turno por recepcionista libera el slot (RN04)

El sistema SHALL permitir a la recepcionista autenticada (`X-API-Key`) cancelar un turno mediante `POST /turnos/{id}/cancelacion`, actualizando `estado = 'cancelado'` y `cancelled_at = now()`, liberando el intervalo en los predicados parciales `WHERE (estado = 'activo')` de profesional, sillón y paciente, y disparando notificación *best-effort*.

#### Scenario: Cancelación exitosa cambia estado y libera el slot

- **WHEN** la recepcionista envía `POST /turnos/{id}/cancelacion` con `X-API-Key` válida para un turno `activo`
- **THEN** el sistema responde 200 con `estado = 'cancelado'` y `cancelled_at` no nulo, registra el evento en el servicio de notificaciones mock, y permite crear un nuevo turno `activo` en el mismo horario, profesional, sillón y paciente sin conflicto RN02 ni RN05

### Requirement: Idempotencia en cancelación repetida (RN04)

El sistema SHALL procesar de forma idempotente toda llamada repetida a `POST /turnos/{id}/cancelacion` sobre un turno que ya se encuentra en `estado = 'cancelado'`, respondiendo 200 sin alterar el instante `cancelled_at` registrado en la primera cancelación.

#### Scenario: Segunda cancelación conserva el timestamp original

- **WHEN** la recepcionista envía `POST /turnos/{id}/cancelacion` sobre un turno cuyo `estado` ya es `'cancelado'` con `cancelled_at = T1`
- **THEN** el sistema responde 200 con `estado = 'cancelado'` y `cancelled_at == T1` intacto

### Requirement: Rechazo de cancelación por turno inexistente o falta de credencial

El sistema SHALL responder 404 con `{code: "NO_ENCONTRADO", message}` cuando el `id` del turno no exista en la base de datos y 401 cuando falte o sea inválida la cabecera `X-API-Key`.

#### Scenario: Turno inexistente devuelve 404 NO_ENCONTRADO

- **WHEN** la recepcionista autenticada envía `POST /turnos/{id}/cancelacion` con un UUID que no corresponde a ningún turno persistido
- **THEN** el sistema responde 404 con cuerpo JSON `{"code": "NO_ENCONTRADO", "message": "..."}`

#### Scenario: Solicitud sin credencial de recepcionista devuelve 401

- **WHEN** se invoca `POST /turnos/{id}/cancelacion` sin la cabecera `X-API-Key` o con una clave inválida
- **THEN** el sistema responde 401 y no modifica el estado de ningún turno

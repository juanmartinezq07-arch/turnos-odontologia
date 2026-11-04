# Spec Delta

## ADDED Requirements

### Requirement: Reprogramación atómica de turno en transacción única (US-005, RN04)

El sistema SHALL permitir a la recepcionista autenticada (`X-API-Key`) reprogramar un turno activo existente mediante `POST /turnos/{id}/reprogramacion` enviando el nuevo `inicio` (y opcionalmente nuevo `sillon_id`), cancelando el turno original y creando el nuevo en una única transacción de base de datos.

#### Scenario: Reprogramación exitosa cancela original y crea nuevo turno

- **WHEN** la recepcionista solicita `POST /turnos/{id}/reprogramacion` con nuevo `inicio` en horario disponible
- **THEN** el sistema responde 200 con los datos del nuevo turno `activo`, el turno original pasa a `estado = 'cancelado'` con `cancelled_at` registrado, y se emiten los eventos de notificación correspondientes

### Requirement: Rollback atómico ante conflicto en el destino

Si el nuevo horario o sillón solicitado viola las reglas de solapamiento (`RN02`), límite de paciente por día (`RN05`) o validación temporal (`RN03`), el sistema SHALL responder con el código de error correspondiente (`409` o `422`) y revertir completamente la transacción, garantizando que el turno original permanezca en estado `activo` con `cancelled_at = NULL`.

#### Scenario: Choque de horario en destino deja turno original activo (Rollback total)

- **WHEN** se intenta reprogramar un turno activo T1 hacia un horario ya ocupado por el mismo profesional (o sillón)
- **THEN** el sistema responde 409 con el código de conflicto (`RN02_PROFESIONAL` o `RN02_SILLON`) y en la base de datos el turno T1 permanece en `estado = 'activo'` con `cancelled_at = NULL`

#### Scenario: Destino en el pasado rechaza sin alterar turno original

- **WHEN** se intenta reprogramar un turno activo T1 hacia una fecha/hora en el pasado
- **THEN** el sistema responde 422 con `code = RN03_PASADO` y el turno T1 permanece `activo` e intacto

### Requirement: Validación de turno origen para reprogramación

El sistema SHALL responder 404 con `{code: "NO_ENCONTRADO", message}` si el turno origen no existe, 409 con `{code: "TURNO_NO_ACTIVO", message}` si el turno origen ya se encuentra cancelado, y 401 si falta la cabecera `X-API-Key`.

#### Scenario: Reprogramar turno inexistente devuelve 404

- **WHEN** se envía `POST /turnos/{id}/reprogramacion` con un ID que no existe
- **THEN** el sistema responde 404 con `code = NO_ENCONTRADO`

#### Scenario: Reprogramar turno ya cancelado devuelve 409

- **WHEN** se intenta reprogramar un turno cuyo estado es `cancelado`
- **THEN** el sistema responde 409 con `code = TURNO_NO_ACTIVO`

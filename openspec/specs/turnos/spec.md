# turnos Specification

## Purpose

Permite a la recepcionista crear, cancelar y reprogramar turnos sin solapamientos, con el cálculo de fin en el servidor y la liberación inmediata de slots al cancelar.

## Requirements

### Requirement: Alta de turno calcula fin en el servidor (RN01)

El sistema SHALL calcular `fin = inicio + duracion_min` de la prestación y SHALL rechazar con 422 cualquier request que incluya el campo `fin` o campos no declarados (`extra='forbid'`).

#### Scenario: Alta correcta calcula fin

- **WHEN** la recepcionista envía `POST /turnos` con `profesional_id`, `sillon_id`, `prestacion_id` (30 min), `inicio` válido y datos mínimos del paciente
- **THEN** el sistema responde 201 con el turno creado cuyo `fin` es exactamente `inicio + 30 min`

#### Scenario: Cliente que envía fin es rechazado

- **WHEN** el request incluye el campo `fin`
- **THEN** el sistema responde 422 con `{code, message}` y no persiste nada

### Requirement: Alta rechaza solapamiento indicando el eje (RN02)

El sistema SHALL rechazar con 409 y código `RN02_PROFESIONAL` o `RN02_SILLON` todo turno activo que se solape con otro activo del mismo profesional o del mismo sillón. El borde que se toca (`inicio_nuevo == fin_existente`) SHALL NOT considerarse solapamiento (semántica `[)`).

#### Scenario: Choque por profesional

- **WHEN** existe un turno activo del profesional P de 10:00 a 10:30 y se pide otro para P de 10:15 a 10:45
- **THEN** el sistema responde 409 con `code = RN02_PROFESIONAL`

#### Scenario: Choque por sillón con distinto profesional

- **WHEN** existe un turno activo en el sillón S de 10:00 a 10:30 y se pide otro en S de 10:15 a 10:45 con otro profesional
- **THEN** el sistema responde 409 con `code = RN02_SILLON`

#### Scenario: Borde que se toca no choca

- **WHEN** existe un turno activo de 10:00 a 10:30 y se pide otro de 10:30 a 11:00 con mismo profesional y sillón
- **THEN** el sistema responde 201

### Requirement: Alta valida temporalidad y horario (RN03)

El sistema SHALL rechazar con 422 todo turno con `inicio` en el pasado (contra `now()` en `America/Argentina/Buenos_Aires`) o fuera de `HorarioAtencion`.

#### Scenario: Turno en el pasado

- **WHEN** se pide un turno con `inicio` anterior a `now()` del consultorio
- **THEN** el sistema responde 422 y no persiste nada

#### Scenario: Turno fuera de horario

- **WHEN** se pide un turno fuera del horario configurado (ej. domingo sin atención)
- **THEN** el sistema responde 422

### Requirement: Alta aplica límite de un activo por día (RN05)

El sistema SHALL rechazar con 409 y código `RN05` todo turno activo cuando el mismo paciente (teléfono o email normalizado) ya tiene otro turno activo ese día calendario.

#### Scenario: Segundo activo el mismo día

- **WHEN** el paciente con teléfono `11-0000-0001` ya tiene un turno activo hoy y pide otro activo hoy
- **THEN** el sistema responde 409 con `code = RN05`

### Requirement: Cancelación libera el slot (RN04)

El sistema SHALL implementar la cancelación como `UPDATE estado='cancelado', cancelled_at=now()` (sin borrado físico) y SHALL volver a ofrecer ese rango en disponibilidad.

#### Scenario: Cancelar libera

- **WHEN** la recepcionista cancela un turno activo
- **THEN** el sistema responde 200, el turno queda `cancelado` con `cancelled_at` informado y un nuevo turno en ese mismo rango responde 201

#### Scenario: Cancelar lo ya cancelado es idempotente

- **WHEN** se pide cancelar un turno ya `cancelado`
- **THEN** el sistema responde 409 o 422 sin duplicar efectos

### Requirement: Reprogramación atómica con rollback

El sistema SHALL ejecutar la reprogramación en una sola transacción: si el destino viola RN02/RN03/RN05, SHALL hacer rollback total y el turno original SHALL permanecer activo.

#### Scenario: Destino choca, original intacto

- **WHEN** se reprograma un turno activo a un slot ocupado por otro activo
- **THEN** el sistema responde 409 y el turno original sigue `activo` en su horario inicial

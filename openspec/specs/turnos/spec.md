# Spec Delta

## Purpose

Permite a la recepcionista crear turnos sin solapamientos por profesional ni por sillón, con el cálculo de fin en el servidor.

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

#### Scenario: Concurrencia real al mismo slot

- **WHEN** dos `POST /turnos` concurrentes piden el mismo slot activo del mismo profesional y sillón
- **THEN** uno responde 201 y el otro responde 409 (con `RN02_PROFESIONAL` o `RN02_SILLON`)

### Requirement: Alta valida temporalidad y horario (RN03)

El sistema SHALL rechazar con 422 todo turno con `inicio` en el pasado (contra `now()` en `America/Argentina/Buenos_Aires`) o fuera de `HorarioAtencion`.

#### Scenario: Turno en el pasado

- **WHEN** se pide un turno con `inicio` anterior a `now()` del consultorio
- **THEN** el sistema responde 422 y no persiste nada

#### Scenario: Turno fuera de horario

- **WHEN** se pide un turno fuera del horario configurado (ej. domingo sin atención)
- **THEN** el sistema responde 422

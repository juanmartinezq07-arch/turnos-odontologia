# disponibilidad Specification

## Purpose

Expone los huecos reales reservables por profesional, fecha y prestación para que recepcionista y paciente elijan un horario que efectivamente existe.

## Requirements

### Requirement: Cómputo de huecos desde horario menos activos

El sistema SHALL computar los slots como `HorarioAtencion` del día menos los turnos en estado `activo` de ese profesional, y SHALL exponerlos en `GET /disponibilidad?profesional_id=&fecha=&prestacion_id=`.

#### Scenario: Hueco ocupado no se ofrece

- **WHEN** se consulta disponibilidad de un día con un turno activo de 10:00 a 10:30
- **THEN** ningún slot ofrecido se solapa con 10:00–10:30 y el resto del horario sí aparece

#### Scenario: Cancelado sí se ofrece

- **WHEN** el único turno de ese rango está `cancelado`
- **THEN** el rango vuelve a aparecer como disponible

### Requirement: Slots respetan la duración de la prestación (RN01)

El sistema SHALL generar slots cuya duración es exactamente la de la prestación pedida y SHALL NOT ofrecer fracciones menores.

#### Scenario: Prestación de 45 min

- **WHEN** se pide disponibilidad con una prestación de 45 min
- **THEN** todos los slots devueltos duran 45 min y encajan completos dentro del horario

### Requirement: Disponibilidad nunca ofrece el pasado (RN03)

El sistema SHALL excluir del resultado todo slot cuyo `inicio` sea anterior a `now()` en `America/Argentina/Buenos_Aires`.

#### Scenario: Consulta del día en curso por la tarde

- **WHEN** se consulta la fecha de hoy a las 15:00 del consultorio
- **THEN** ningún slot ofrecido inicia antes de las 15:00

### Requirement: Disponibilidad determinista

El sistema SHALL devolver el mismo resultado en dos consultas consecutivas sin altas, cancelaciones ni cambios de horario intermedios.

#### Scenario: Doble consulta idéntica

- **WHEN** se llama dos veces seguidas a `GET /disponibilidad` con los mismos parámetros y sin escrituras intermedias
- **THEN** ambas respuestas son idénticas en slots y orden

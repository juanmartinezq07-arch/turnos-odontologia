# Purpose

Provee el cálculo determinista y la consulta pública de slots disponibles (`GET /disponibilidad`) por profesional, fecha y prestación, respetando la duración de la prestación (RN01), el no solapamiento con turnos activos bajo semántica `[)` (RN02) y el horario de atención y no pasado (RN03).

## Requirements

### Requirement: Cálculo determinista de slots disponibles dentro del horario (RN01, RN03)

El sistema SHALL calcular los slots disponibles `[inicio, fin)` para un profesional, una fecha y una prestación de duración `duracion_min` como una función pura de los bloques de `HorarioAtencion` del día, los intervalos de turnos `activos`, la duración de la prestación y el instante `now` inyectado, asegurando que `fin = inicio + duracion_min` y que el bloque completo `[inicio, fin)` entre dentro del horario de atención sin ofrecer inicios en el pasado.

#### Scenario: Bloque que no entra completo al final del horario es descartado

- **WHEN** el horario de atención cierra a las 12:00 y la prestación dura 45 minutos
- **THEN** ningún slot devuelto tiene `fin` posterior a las 12:00 (un inicio a las 11:30 no se ofrece porque terminaría a las 12:15)

#### Scenario: Slots anteriores a now son descartados

- **WHEN** se consulta la disponibilidad del día actual siendo `now` las 10:15 en `America/Argentina/Buenos_Aires`
- **THEN** ningún slot devuelto tiene `inicio` anterior a las 10:15

#### Scenario: Día sin horario de atención devuelve lista vacía

- **WHEN** se consulta disponibilidad en un día sin bloques en `HorarioAtencion` (ej. domingo)
- **THEN** el sistema responde 200 con una lista vacía `[]`

### Requirement: Exclusión de turnos activos con semántica semiabierta (RN02, RN04)

El sistema SHALL excluir de la disponibilidad todo intervalo `[inicio, fin)` que se solape (`inicio < fin_turno AND fin > inicio_turno`) con un turno en estado `activo` del profesional, permitiendo que un slot comience exactamente en el `fin` de un turno activo o termine exactamente en el `inicio` de un turno activo (semántica `[)`), e ignorando los turnos en estado `cancelado`.

#### Scenario: Hueco libre y borde que se toca no pisa turnos activos

- **WHEN** el horario es de 09:00 a 11:00, la prestación dura 30 minutos y existe un turno `activo` de 09:30 a 10:00
- **THEN** la disponibilidad incluye `[09:00, 09:30)`, `[10:00, 10:30)` y `[10:30, 11:00)`, y excluye cualquier slot que pise `[09:30, 10:00)`

#### Scenario: Turno cancelado no resta disponibilidad

- **WHEN** existe un turno con `estado = 'cancelado'` de 10:00 a 10:30
- **THEN** el slot `[10:00, 10:30)` sigue ofreciéndose como disponible

### Requirement: Consulta pública determinista por HTTP

El sistema SHALL exponer `GET /disponibilidad?profesional_id=&fecha=&prestacion_id=` sin requerir autenticación (`X-API-Key`) y dos consultas sucesivas con los mismos parámetros, estado de base e instante `now` SHALL devolver exactamente la misma lista ordenada de slots.

#### Scenario: Dos consultas seguidas devuelven exactamente los mismos slots

- **WHEN** un cliente sin credencial invoca dos veces seguidas `GET /disponibilidad` con los mismos `profesional_id`, `fecha` y `prestacion_id` sin altas ni cancelaciones intermedias
- **THEN** ambas respuestas son 200 OK y contienen exactamente la misma lista de slots `[inicio, fin)`

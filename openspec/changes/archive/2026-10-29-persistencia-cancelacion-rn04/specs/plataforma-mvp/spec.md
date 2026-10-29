# Spec Delta

## ADDED Requirements

### Requirement: Persistencia de la cancelación (RN04)

El esquema `turno` SHALL incluir la columna `cancelled_at TIMESTAMPTZ` nullable, de modo que un turno `activo` tenga `cancelled_at = NULL` y la cancelación pueda registrar el instante en que ocurrió sin borrar el turno. La migración que agrega la columna SHALL preservar intactos el `CHECK (fin > inicio)`, el `CHECK` de `estado` y ambos `EXCLUDE USING gist` de RN02.

#### Scenario: Columna disponible tras la migración

- **WHEN** se aplica la migración 004 sobre una base con el esquema de la 003
- **THEN** la tabla `turno` tiene `cancelled_at` de tipo `TIMESTAMPTZ` nullable

#### Scenario: Turno activo no tiene instante de cancelación

- **WHEN** se inserta un turno sin indicar `cancelled_at`
- **THEN** el turno persiste con `cancelled_at = NULL` y `estado = 'activo'`

#### Scenario: Invariantes RN02 intactas tras la migración

- **WHEN** se aplica la migración 004
- **THEN** ambos constraints `rn02_profesional` y `rn02_sillon` siguen activos y el `CHECK (fin > inicio)` sigue vigente

#### Scenario: Downgrade reversible

- **WHEN** se ejecuta `downgrade` de la migración 004
- **THEN** el índice `idx_turno_paciente_fecha` y la columna `cancelled_at` se eliminan y el esquema vuelve al estado de la 003

### Requirement: Índice de consulta por paciente y fecha

El esquema SHALL incluir el índice `idx_turno_paciente_fecha` sobre `turno (paciente_id, inicio)` para soportar la consulta de turnos de un paciente por fecha.

#### Scenario: Índice presente tras la migración

- **WHEN** se aplica la migración 004
- **THEN** existe el índice `idx_turno_paciente_fecha` sobre `turno (paciente_id, inicio)`

#### Scenario: El índice no altera la unicidad ni las reglas

- **WHEN** se insertan dos turnos del mismo paciente en fechas distintas
- **THEN** ambos persisten, porque el índice es de consulta y no impone unicidad

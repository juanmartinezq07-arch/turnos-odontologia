# Spec Delta

## ADDED Requirements

### Requirement: Persistencia del token de cancelación para reserva guest

El esquema `turno` SHALL incluir la columna `token_cancelacion TEXT UNIQUE` nullable para almacenar el token de cancelación de las reservas públicas sin afectar los turnos creados por recepcionista (`NULL` permitido en múltiples filas).

#### Scenario: Columna token_cancelacion disponible y única

- **WHEN** se aplica la migración 005 sobre el esquema de la 004
- **THEN** la tabla `turno` tiene `token_cancelacion TEXT` nullable con restricción `UNIQUE`

#### Scenario: Token duplicado es rechazado por la base

- **WHEN** se intenta insertar un segundo turno con el mismo `token_cancelacion` no nulo
- **THEN** la base de datos rechaza el insert por violación de unicidad

### Requirement: Invariante declarativa RN05 en base de datos

El esquema SHALL incluir el índice único parcial `rn05_un_activo_por_dia` sobre `turno (paciente_id, ((inicio AT TIME ZONE 'America/Argentina/Buenos_Aires')::date)) WHERE (estado = 'activo')` para garantizar en la base de datos que un paciente no tenga más de un turno activo en el mismo día calendario del consultorio. La migración 005 SHALL ser reversible mediante `downgrade` sin alterar los constraints de RN02 ni `cancelled_at`.

#### Scenario: Segundo turno activo del mismo paciente en el mismo día viola el índice

- **WHEN** existe un turno `activo` para el paciente P en una fecha local de `America/Argentina/Buenos_Aires` y se inserta otro turno `activo` para P en la misma fecha local
- **THEN** la base de datos rechaza el insert violando `rn05_un_activo_por_dia`

#### Scenario: Turno activo del mismo paciente en otro día es permitido

- **WHEN** existe un turno `activo` para el paciente P en un día y se inserta otro turno `activo` para P en un día calendario distinto
- **THEN** el insert hace commit sin violar `rn05_un_activo_por_dia`

#### Scenario: Turno cancelado no bloquea un nuevo turno activo el mismo día

- **WHEN** el único turno del paciente P en ese día tiene `estado = 'cancelado'` y se inserta un nuevo turno `activo` para P en el mismo día
- **THEN** el insert hace commit porque el índice parcial filtra `WHERE (estado = 'activo')`

#### Scenario: Downgrade de migración 005 reversible

- **WHEN** se ejecuta `downgrade` de la migración 005
- **THEN** se eliminan el índice `rn05_un_activo_por_dia` y la columna `token_cancelacion` preservando intacto el esquema de la migración 004

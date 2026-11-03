# Spec Delta

## Purpose

Fija la base transversal del change: invariante anti-solapamiento en la base, auth mínima, errores estables e infraestructura local reproducible.

## Requirements

### Requirement: Doble EXCLUDE parcial con semántica de borde

La base de datos SHALL aplicar dos constraints `EXCLUDE USING gist` parciales `WHERE (estado = 'activo')` — uno por `profesional_id`, otro por `sillon_id` — sobre `tstzrange(inicio, fin) WITH &&`, más `CHECK (fin > inicio)`, con `btree_gist` instalada primero. El rango SHALL usar semántica `[)` (borde que se toca no choca).

#### Scenario: Constraint bloquea doble commit concurrente

- **WHEN** dos transacciones concurrentes insertan el mismo slot activo del mismo profesional
- **THEN** una hace commit y la otra viola el constraint `RN02_PROFESIONAL`

#### Scenario: Cancelado no bloquea

- **WHEN** existe un turno `cancelado` en un rango y se inserta un activo idéntico
- **THEN** el insert hace commit sin violar constraints

### Requirement: Auth mínima por API key de recepcionista

El sistema SHALL exigir API key de recepcionista (desde env `API_KEY_RECEPCION`) en `POST /turnos` y SHALL responder 401 sin credencial.

#### Scenario: Alta sin credencial rechazada

- **WHEN** se llama `POST /turnos` sin API key
- **THEN** el sistema responde 401

### Requirement: Formato de error estable y mapeo de constraints

Todo error SHALL usar la forma `{code, message}`; la violación de EXCLUDE SHALL mapearse a 409 con `RN02_PROFESIONAL` / `RN02_SILLON` y la violación del índice único parcial `rn05_un_activo_por_dia` SHALL mapearse a 409 con `RN05` (nunca 500, distinguiendo por nombre de constraint/índice, no por parseo del mensaje); los errores Pydantic SHALL mapearse a 422.

#### Scenario: Violación EXCLUDE es 409 con código

- **WHEN** un insert viola el EXCLUDE de sillón bajo concurrencia
- **THEN** la API responde 409 con `code = RN02_SILLON`

#### Scenario: Violación de índice RN05 es 409 con código RN05

- **WHEN** un insert viola el índice único parcial `rn05_un_activo_por_dia`
- **THEN** `conflict_code_from_integrity_error` retorna `RN05` y la API responde 409 con `code = RN05`

### Requirement: Infra local reproducible y seed ficticio

El repo SHALL incluir `docker-compose.yml` con un único servicio `db` (`postgres:16` pineada, volumen nombrado, healthcheck `pg_isready`, puerto solo en localhost), `.env.example` solo con placeholders (sin secretos reales) y un seed con datos exclusivamente ficticios (nombres tipo "Juan Pérez Demo", teléfonos `11-0000-0000`, mails `@example.com`).

#### Scenario: Levantar demo sin secretos reales

- **WHEN** un desarrollador sigue `docker-compose.yml` + `.env.example` con profesionales, sillones, prestaciones y horario de atención
- **THEN** la API arranca contra `db` y ningún dato real de pacientes existe en el repo

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

### Requirement: Frontera de seguridad para clientes web

Cualquier interfaz web (frontend) desarrollada para interactuar con la API SHALL acceder a los endpoints administrativos y autenticados sin exponer claves estáticas de API (`API_KEY_RECEPCION`, `API_KEY_ODONTOLOGO`) en el código ni en el bundle estático del navegador. Las operaciones públicas de reserva (`POST /reservas` y consulta de disponibilidad) no requieren credenciales, mientras que las operaciones con rol SHALL canalizarse mediante sesiones seguras o proxy autenticado.

#### Scenario: Cliente público no expone secretos

- **WHEN** un usuario accede a la interfaz de reservas públicas
- **THEN** las peticiones al catálogo y disponibilidad se realizan contra endpoints abiertos sin transmitir cabeceras sensibles embebidas en el bundle

#### Scenario: Operaciones de recepcionista protegidas

- **WHEN** un operador recepcionista utiliza una interfaz para dar turnos
- **THEN** la autenticación contra la API no permite la extracción de la API key global por parte de usuarios finales del navegador

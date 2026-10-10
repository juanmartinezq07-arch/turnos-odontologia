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

Todo error SHALL usar la forma `{code, message}`; la violación de EXCLUDE SHALL mapearse a 409 con `RN02_PROFESIONAL` / `RN02_SILLON` (nunca 500, distinguiendo por nombre de constraint, no por parseo del mensaje); los errores Pydantic SHALL mapearse a 422.

#### Scenario: Violación EXCLUDE es 409 con código

- **WHEN** un insert viola el EXCLUDE de sillón bajo concurrencia
- **THEN** la API responde 409 con `code = RN02_SILLON`

### Requirement: Infra local reproducible y seed ficticio

El repo SHALL incluir `docker-compose.yml` con un único servicio `db` (`postgres:16` pineada, volumen nombrado, healthcheck `pg_isready`, puerto solo en localhost), `.env.example` solo con placeholders (sin secretos reales) y un seed con datos exclusivamente ficticios (nombres tipo "Juan Pérez Demo", teléfonos `11-0000-0000`, mails `@example.com`).

#### Scenario: Levantar demo sin secretos reales

- **WHEN** un desarrollador sigue `docker-compose.yml` + `.env.example` con profesionales, sillones, prestaciones y horario de atención
- **THEN** la API arranca contra `db` y ningún dato real de pacientes existe en el repo

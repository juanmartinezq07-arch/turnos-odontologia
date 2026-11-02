# Spec Delta

## Purpose

Provee acceso público de solo lectura a los catálogos operativos activos del consultorio (`profesionales`, `sillones` y `prestaciones` con su duración RN01) para habilitar la consulta de disponibilidad y la reserva de turnos.

## ADDED Requirements

### Requirement: Consulta pública de profesionales activos

El sistema SHALL exponer `GET /profesionales` sin requerir autenticación y SHALL devolver con estado 200 únicamente los profesionales con `activo = true`, incluyendo `id`, `nombre`, `apellido` y `matricula`.

#### Scenario: Listado de profesionales sin credencial excluye inactivos

- **WHEN** un cliente realiza `GET /profesionales` sin header `X-API-Key` existiendo profesionales activos e inactivos
- **THEN** el sistema responde 200 con la lista de profesionales donde `activo = true` y omite los inactivos

### Requirement: Consulta pública de sillones activos

El sistema SHALL exponer `GET /sillones` sin requerir autenticación y SHALL devolver con estado 200 únicamente los sillones con `activo = true`, incluyendo `id` y `nombre`.

#### Scenario: Listado de sillones sin credencial excluye inactivos

- **WHEN** un cliente realiza `GET /sillones` sin header `X-API-Key` existiendo sillones activos e inactivos
- **THEN** el sistema responde 200 con la lista de sillones donde `activo = true` y omite los inactivos

### Requirement: Consulta pública de prestaciones activas con duración RN01

El sistema SHALL exponer `GET /prestaciones` sin requerir autenticación y SHALL devolver con estado 200 únicamente las prestaciones con `activa = true`, incluyendo `id`, `nombre` y `duracion_min` entero positivo (RN01).

#### Scenario: Listado de prestaciones expone duracion_min y excluye inactivas

- **WHEN** un cliente realiza `GET /prestaciones` sin header `X-API-Key` existiendo prestaciones con `activa = true` y `activa = false`
- **THEN** el sistema responde 200 solo con las prestaciones activas y cada elemento contiene `duracion_min`

### Requirement: Rutas de catálogos documentadas en OpenAPI

El sistema SHALL registrar `GET /profesionales`, `GET /sillones` y `GET /prestaciones` en el esquema `/openapi.json` generado por la aplicación.

#### Scenario: Esquema OpenAPI incluye los tres endpoints de catálogo

- **WHEN** un cliente consulta `GET /openapi.json`
- **THEN** el objeto `paths` incluye `/profesionales`, `/sillones` y `/prestaciones` con el método `get`

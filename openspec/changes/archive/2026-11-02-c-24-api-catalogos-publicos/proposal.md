# Proposal

## Why

Las entidades de catálogo (`Profesional`, `Sillon` y `Prestacion`) ya existen en la base de datos y cuentan con datos semilla desde `C-01`, pero no existe ningún endpoint HTTP para consultarlas. Sin los catálogos públicos, ni la recepcionista ni el paciente guest (en el flujo público `KB-07 §Flujo 1`) pueden descubrir qué profesionales, sillones y prestaciones están activos ni conocer la `duracion_min` (RN01) antes de consultar disponibilidad o reservar.

## What Changes

- Exponer tres endpoints públicos de solo lectura (`GET /profesionales`, `GET /sillones`, `GET /prestaciones`) sin requerir autenticación (`X-API-Key`), cubriendo 3 de las 5 rutas públicas definidas en `KB-03`.
- Filtrar únicamente registros activos (`Profesional.activo == True`, `Sillon.activo == True`, `Prestacion.activa == True`) con orden determinista.
- Exponer `duracion_min` en cada ítem de `GET /prestaciones` para hacer visible la duración que gobierna RN01.
- Definir schemas Pydantic v2 estrictos (`extra="forbid"`) en `backend/app/schemas/catalogo.py`, consultas de lectura en `backend/app/application/catalogs.py` y router fino en `backend/app/api/v1/catalogos.py` cableado en `backend/app/main.py`.
- Agregar suite de tests de integración en `backend/tests/test_catalogos_api.py` contra PostgreSQL 16 real verificando acceso público (`200 OK` sin credenciales), exclusión de inactivos, presencia de `duracion_min` y documentación en `/openapi.json`.

## Capabilities

### New Capabilities

- `catalogos`: consulta pública de catálogos operativos activos (`profesionales`, `sillones` y `prestaciones` con su duración RN01).

### Modified Capabilities

- Ninguna.

## Impact

- Código nuevo: `backend/app/schemas/catalogo.py`, `backend/app/application/catalogs.py`, `backend/app/api/v1/catalogos.py`, `backend/tests/test_catalogos_api.py`.
- Código modificado: `backend/app/main.py` (registro del router de catálogos).
- Base de datos / Migraciones: ninguna (las tablas `profesional`, `sillon` y `prestacion` ya existen desde la migración `001`).
- Dependencias desbloqueadas: habilita la rama de lectura necesaria para `C-29 reservas-guest` y `C-33` / `C-35`.

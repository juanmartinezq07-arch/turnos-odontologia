# Tasks

## 1. RED — Tests de catálogos públicos que fallan antes de la implementación

- [x] 1.1 Crear `backend/tests/test_catalogos_api.py` con tests para `GET /profesionales`, `GET /sillones`, `GET /prestaciones` (200 sin credencial, solo activos, `duracion_min` visible en prestaciones) y presencia de las 3 rutas en `GET /openapi.json`, verificando que fallen con 404/AssertionError antes de implementar el router.

## 2. GREEN — Schemas, servicio de aplicación y router de catálogos

- [x] 2.1 Crear `backend/app/schemas/catalogo.py` con `ProfesionalOut`, `SillonOut` y `PrestacionOut` usando `ConfigDict(extra="forbid", from_attributes=True)` y verificar que los modelos validen instancias ORM y rechacen campos extra.
- [x] 2.2 Crear `backend/app/application/catalogs.py` con `listar_profesionales_activos`, `listar_sillones_activos` y `listar_prestaciones_activas` filtrando por `activo == True` / `activa == True` con orden determinista.
- [x] 2.3 Crear `backend/app/api/v1/catalogos.py` con los endpoints públicos `GET /profesionales`, `GET /sillones` y `GET /prestaciones` y registrar el router en `backend/app/main.py`, verificando que `pytest tests/test_catalogos_api.py` pase completo en verde.

## 3. Verificación integral y regresión

- [x] 3.1 Ejecutar la suite completa `pytest` desde `backend/` contra PostgreSQL 16 y verificar que todos los tests (los 44 existentes más los nuevos de `test_catalogos_api.py`) pasen en verde sin regresiones.

## Workflow follow-up

- Archivar el change con `/openspec-archive-change` una vez completadas y verificadas las tasks.
- Marcar `[x]` en `C-24` dentro de `CHANGES.md`.

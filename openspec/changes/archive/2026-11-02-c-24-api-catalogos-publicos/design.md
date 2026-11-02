# Design

## Context

Las entidades `Profesional`, `Sillon` y `Prestacion` ya están definidas en `backend/app/domain/models.py` y creadas en la migración `001`. Actualmente solo existe el router `backend/app/api/v1/turnos.py` montado en la raíz de la aplicación (`POST /turnos`). Ver `proposal.md` para la motivación de negocio.

## Goals / Non-Goals

**Goals:**

- Exponer `GET /profesionales`, `GET /sillones` y `GET /prestaciones` sin dependencia de autenticación (`require_recepcion` / `require_odontologo`).
- Mantener la separación de capas exigida por `KB-08` y `AGENTS.md`: router fino en `app/api/v1/catalogos.py`, consultas en `app/application/catalogs.py` y schemas con `extra="forbid"` en `app/schemas/catalogo.py`.
- Garantizar orden determinista en las tres consultas SQL.

**Non-Goals:**

- Endpoints de alta, baja o modificación de catálogos (el MVP gestiona catálogos por seed según `KB-03`).
- Paginación o filtros adicionales por query params (escala de consultorio chico: 2–10 profesionales según DD-02).

## Decisions

### D-01 — Rutas en la raíz sin prefijo `/api/v1`

Los endpoints se montan como `/profesionales`, `/sillones` y `/prestaciones` para mantener coherencia con `/turnos` (implementado en `C-01`) y cumplir literalmente el contrato de `CHANGES.md` (`GET /profesionales`, `/sillones`, `/prestaciones`).

### D-02 — Separación en `application/catalogs.py`, `api/v1/catalogos.py` y `schemas/catalogo.py`

Para respetar la regla dura de `AGENTS.md` ("NUNCA lógica de dominio/DB en routers ni en `main.py`"), las consultas `SELECT ... WHERE activo/activa IS TRUE ORDER BY ...` viven en funciones asíncronas dentro de `backend/app/application/catalogs.py`. El router en `backend/app/api/v1/catalogos.py` solo inyecta `AsyncSession = Depends(get_session)` y serializa con `ProfesionalOut`, `SillonOut` y `PrestacionOut` (todos con `ConfigDict(extra="forbid", from_attributes=True)`).

### D-03 — Orden determinista por nombre/apellido

- `listar_profesionales`: `ORDER BY Profesional.apellido.asc(), Profesional.nombre.asc()`
- `listar_sillones`: `ORDER BY Sillon.nombre.asc()`
- `listar_prestaciones`: `ORDER BY Prestacion.nombre.asc()`

Esto evita respuestas con orden arbitrario de PostgreSQL tras updates.

## Risks / Trade-offs

- [Risk] Diferencia de nombre de columna entre `Profesional.activo` / `Sillon.activo` y `Prestacion.activa` → Mitigación: cubrir explícitamente los tres filtros con tests de exclusión de inactivos en `test_catalogos_api.py`.

## Migration Plan

No requiere migraciones Alembic. Solo código de aplicación, schemas, router y tests.

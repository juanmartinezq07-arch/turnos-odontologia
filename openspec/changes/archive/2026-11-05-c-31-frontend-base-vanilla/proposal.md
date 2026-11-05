# Proposal

## Why

El backend ya expone todos los contratos necesarios (catálogos, disponibilidad, reservas, turnos, agenda), pero no hay interfaz de usuario: la demo se ejerce solo por Swagger/curl. C-30 derogó DD-01 condicionadamente y DD-08 fijó la dirección: frontend **sin framework ni build** (HTML/CSS/JS nativo) servido por FastAPI en el mismo origen. C-31 construye esa base para que C-32…C-35 implementen las pantallas.

## What Changes

- Servir archivos estáticos desde `frontend/` con FastAPI (`StaticFiles`) en el mismo origen, sin CORS.
- Definir la organización de archivos: `index.html`, `css/`, `js/` (api, auth, router, screens).
- Cliente HTTP nativo (`fetch`) que consume el contrato `{code, message}` y expone `ApiError(code, message, status)`.
- Manejo centralizado de errores por código de regla (`RN02_*`, `RN05`, `RN03_*`, `AGENDA_AJENA`, etc.), sin parsear texto.
- Ingreso de credenciales de rol en runtime, guardadas solo en memoria (variable JS), enviadas como `X-API-Key` (+ `X-Profesional-Id` para odontólogo); nunca en archivos estáticos.
- Navegación entre pantallas por hash (`#/...`) con router mínimo.

## Capabilities

### New Capabilities

- `frontend-base`: base de interfaz web estática (HTML/CSS/JS) servida por FastAPI en el mismo origen, con cliente HTTP tipado por código de error y gestión de credenciales en memoria.

### Modified Capabilities

(none)

## Impact

- `backend/app/main.py` (montaje de `StaticFiles`).
- `frontend/` (nuevos archivos HTML/CSS/JS).
- `knowledge-base/08_arquitectura_propuesta.md` (árbol ya actualizado).
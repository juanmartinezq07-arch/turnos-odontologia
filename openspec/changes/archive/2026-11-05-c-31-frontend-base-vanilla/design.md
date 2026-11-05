# Design

## Context

Ver `proposal.md` — Why. El backend ya expone todos los endpoints; C-31 agrega la capa de presentación estática. C-30/C-23/C-29/C-27 archivados; DD-08 vigente (vanilla, mismo origen).

## Goals / Non-Goals

**Goals:**
- Servir `frontend/` desde FastAPI en mismo origen, sin CORS.
- Organizar archivos y navegación.
- Cliente `fetch` con `ApiError(code, message, status)`.
- Credenciales en memoria (runtime).

**Non-Goals:**
- No implementar pantallas específicas (C-32…C-35).
- No introducir build tooling ni framework.
- No tocar lógica de dominio.

## Decisions

### 1. Montaje de estáticos
`app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True))` **después** de registrar todos los routers y el mount de `/docs`. Orden: routers → StaticFiles. Esto evita que el catch-all oculte `/docs`/`/openapi.json`. `FRONTEND_DIR` resuelto relativo al backend (`../frontend`).

### 2. Organización de archivos
```
frontend/
  index.html
  css/app.css
  js/api.js       # fetch wrapper + ApiError
  js/auth.js      # credencial en memoria
  js/router.js    # hash router
  js/app.js       # bootstrap
```

### 3. Cliente HTTP
`api.js` expone `apiFetch(path, opts)` que parsea JSON, y en error lanza `ApiError(code, message, status)` leyendo `{code, message}`. Nunca parsea texto.

### 4. Credenciales
`auth.js` mantiene la key en una variable de módulo (no `localStorage`). `apiFetch` inyecta `X-API-Key` y, para odontólogo, `X-Profesional-Id` si está definido. Al recargar, se pierde.

### 5. Navegación
Hash router (`#/agenda`, `#/turno`, `#/reserva`) con listener `hashchange`; renderiza la sección correspondiente.

### 6. ES modules
Uso de `<script type="module">` para organización; funciona porque se sirve por HTTP (mismo origen).

## Risks / Trade-offs

- [Orden de mount] Mitigado registrando routers antes de `StaticFiles`.
- [Sin tipos estáticos] Mitigado por contrato `{code, message}` documentado.
- [Credencial visible en memoria] Aceptado por DD-08 (no se afirma ocultamiento).

## Migration Plan

Agregar dependencia `aiofiles` si StaticFiles la requiere (FastAPI la usa para servir archivos). Montaje en `main.py`. No migraciones.

## Open Questions

(none)
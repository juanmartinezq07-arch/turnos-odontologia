# Tasks

## 1. Servir estáticos desde FastAPI

- [x] 1.1 En `backend/app/main.py`, montar `StaticFiles(directory=..., html=True)` en `/` después de registrar todos los routers; resolver `FRONTEND_DIR` relativo a `backend/`. Verificar que `/docs` y `/openapi.json` siguen accesibles y que `/` sirve `index.html`.

## 2. Base de archivos frontend

- [x] 2.1 Crear `frontend/index.html`, `frontend/css/app.css`, `frontend/js/{api,auth,router,app}.js` con la estructura del design. Verificar que se sirven con content-type correcto.

## 3. Cliente HTTP y manejo de errores

- [x] 3.1 Implementar `api.js` con `apiFetch` y `ApiError(code, message, status)`; parsear `{code, message}` en errores. Verificar con una llamada real a un endpoint (ej. `/profesionales`).

## 4. Credenciales en memoria

- [x] 4.1 Implementar `auth.js` (key en variable de módulo, inyección de headers, pérdida al recargar). Verificar que recargar la página limpia la credencial.

## 5. Navegación

- [x] 5.1 Implementar hash router en `router.js` y bootstrap en `app.js`. Verificar cambio de pantalla sin recarga completa.

## 6. Verificación

- [x] 6.1 Ejecutar smoke manual: abrir `/`, navegar, llamar a un endpoint protegido con credencial ingresada, verificar 401 sin credencial. (Tests automatizados opcionales.)

## Workflow follow-up

- Archivar el change tras verificación.
- Marcar `C-31` como `[x]` en `CHANGES.md`.
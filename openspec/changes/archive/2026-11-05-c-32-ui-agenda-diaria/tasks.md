# Tasks

## 1. Pantalla de agenda

- [x] 1.1 Crear `frontend/js/screens/agenda.js` con formulario (profesional, fecha, incluir cancelados) y tabla de resultados. Verificar render en `/`.

## 2. Integración

- [x] 2.1 Registrar ruta `#/agenda` en `app.js` y agregar enlace en nav. Verificar navegación sin recarga.

## 3. Manejo de errores

- [x] 3.1 Mapear 403 (`AGENDA_AJENA`) y 401 a mensajes visibles. Verificar con credencial de odontólogo ajeno.

## 4. Verificación

- [x] 4.1 Smoke manual: cargar agenda con credencial de recepción, verificar orden y datos; probar 403 con odontólogo.

## Workflow follow-up

- Archivar el change tras verificación.
- Marcar `C-32` como `[x]` en `CHANGES.md`.
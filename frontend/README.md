# Frontend — TurnosAR (placeholder)

> **Decisión de alcance resuelta por `C-30 decision-frontend-alcance` (archivado)** y refinada por DD-08 (vanilla): la interfaz se implementa **sin framework ni build** (HTML, CSS y JavaScript nativo) servida por FastAPI en el mismo origen. No se usa React, Vite, TypeScript, npm ni bundler.
> Detalle: `knowledge-base/09_decisiones_y_supuestos.md` §DD-08 y `CHANGES.md` FASE 4.

Alcance previsto (`C-31`…`C-35`), sobre la base vanilla:

- `C-31` base HTML/CSS/JS + organización de archivos + cliente `fetch` para el contrato `{code, message}` (servido por FastAPI, mismo origen).
- `C-32` agenda diaria sobre `GET /agenda`.
- `C-33` alta de turno con errores por código (`RN02_*`, `RN05`, `RN03_*`).
- `C-34` reprogramar/cancelar con estados y rollback visible.
- `C-35` reserva pública con token de cancelación.

Credenciales de rol: se ingresan en tiempo de ejecución y viven solo en memoria del navegador; no se empaquetan en archivos estáticos. No se afirma que queden ocultas al usuario autorizado que las ingresa.

Solo datos ficticios (Ley 25.326): la UI no pide ni muestra dato clínico.
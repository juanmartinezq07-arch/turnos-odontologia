# Plan: Migrar los changes de frontend a HTML, CSS y JavaScript vanilla

## Problema y enfoque

El roadmap todavía plantea React + Vite en C-31 y presenta C-31…C-35 como bloqueados por C-30, aunque C-30 ya está archivado. DD-08 también habilita React explícitamente, y `frontend/README.md` y parte de la KB conservan información desactualizada. OpenCode debe corregir la decisión vigente y todos los artefactos dependientes sin editar el change archivado.

La dirección elegida es un frontend sin framework ni proceso de build: HTML, CSS y JavaScript nativo servidos por FastAPI en el mismo origen. Las credenciales de rol se ingresan en runtime y viven solo en memoria; no se afirmará que quedan ocultas al usuario autorizado que las ingresa.

## Todos

1. Auditar el estado real de C-30, la KB, `frontend/README.md`, el roadmap y los contratos/API existentes; preservar los artefactos archivados como historial.
2. Formalizar la decisión vanilla y el modelo de entrega/credenciales en un nuevo change documental OpenSpec; resolver la contradicción entre DD-08 y la documentación restante.
3. Replantear C-31 como base de frontend vanilla servida por FastAPI, sin React, Vite, TypeScript, npm ni bundler; definir navegación, organización de archivos y cliente `fetch` para errores `{code, message}`.
4. Ajustar C-32…C-35 a esa base, conservar sus objetivos funcionales y corregir dependencias, gates y estados según los cambios de API realmente archivados o pendientes (incluido C-23).
5. Sincronizar `CHANGES.md`, `frontend/README.md` y las secciones pertinentes de `knowledge-base/`; crear/revisar los artefactos OpenSpec de los changes frontend según el schema del proyecto.
6. Verificar consistencia: no quedan instrucciones activas de React/Vite para la UI, no se incorporan claves en archivos estáticos, cada flujo usa los endpoints ya definidos, y el grafo no declara como bloqueos dependencias ya completadas.

## Consideraciones

- No modificar ni reescribir los artefactos archivados de C-30; registrar la nueva decisión mediante un change posterior trazable.
- Mantener separados los cuatro changes funcionales de UI (agenda, alta de turno, reprogramar/cancelar y reserva pública), salvo que la revisión de alcance demuestre que alguno debe dividirse o combinarse.
- No tocar lógica del backend fuera de lo necesario para servir los archivos estáticos en el mismo origen; la decisión de alcance de credenciales se limita a ingreso en runtime y memoria del navegador.
- Preservar el backend como API desacoplada y la regla de no pedir ni mostrar información clínica.

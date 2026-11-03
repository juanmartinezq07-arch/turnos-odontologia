# Proposal

## Why
El roadmap contiene una rama de cambios de interfaz de usuario (`C-31` a `C-35`), los cuales se encuentran actualmente bloqueados por la decisión de arquitectura original **DD-01** ("API / backend puro, sin frontend propio"). Para avanzar ordenadamente en el proyecto o habilitar la fase de interfaz, es necesario formalizar documentalmente si DD-01 se mantiene (postergando UI para una etapa posterior fuera del MVP) o si se deroga/modifica (autorizando el desarrollo de una UI web bajo directrices claras de seguridad para el manejo de credenciales sin exponer API keys en el cliente).

## What Changes
- Formalización de la decisión de alcance en la Base de Conocimiento (`knowledge-base/09_decisiones_y_supuestos.md` § DD-08).
- Actualización de `knowledge-base/01_vision_y_objetivos.md` § Fuera de alcance para reflejar los límites exactos de la interfaz y la entrega.
- Definición de la estrategia de seguridad para clientes web (manejo de credenciales de recepcionista/odontólogo mediante backend-for-frontend o proxy de sesión, sin exponer variables de entorno sensibles en el bundle estático).
- Cierre de la condición de bloqueo sobre la Fase 4 del roadmap en `CHANGES.md`.

## Capabilities
### Modified Capabilities
- `plataforma-mvp`: Se explicita la política de arquitectura de clientes para el MVP y la resolución de la frontera entre API pura y aplicaciones frontend.

## Impact
- Documentación de arquitectura y decisiones de diseño.
- No introduce código ejecutable de frontend en este change; desbloquea formalmente la planificación y ejecución de los changes posteriores (`C-31` a `C-35`).

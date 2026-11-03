# Design

## Context
En la etapa inicial del proyecto se adoptó la decisión **DD-01**, orientando el MVP a ser una API REST pura evaluable mediante Swagger UI y tests automatizados con pytest/httpx, con el fin de priorizar el diseño robusto de invariantes de base de datos (RN02/RN05) y la concurrencia en un plazo acotado de entrega académica.
El roadmap previó una Fase 4 (`C-31` a `C-35`) para proveer interfaz web (React + Vite), pero la catalogó como bloqueada hasta formalizar las implicancias de seguridad, plazos y arquitectura de credenciales.

## Goals / Non-Goals

**Goals:**
- Resolver explícitamente el estado de DD-01 en la base de conocimiento y el roadmap.
- Establecer la política de seguridad para consumo web (evitar la fuga de `API_KEY_*` en bundles de React/Vite en el cliente).
- Delimitar las responsabilidades de las aplicaciones consumidoras respecto al contrato REST `{code, message}` y códigos de conflicto (`RN02_*`, `RN05`).

**Non-Goals:**
- No implementar componentes visuales ni inicializar el scaffolding de React en este change (eso corresponde a `C-31`).
- No modificar los endpoints del backend existentes ni alterar las invariantes del motor de base de datos.

## Decisions

### 1. Resolución de DD-01: Derogación condicionada (DD-08)
Se documenta la decisión **DD-08** en `knowledge-base/09_decisiones_y_supuestos.md`. DD-01 se mantiene como el alcance mínimo de evaluación central (backend puro con garantías de consistencia), pero se deroga su restricción excluyente para habilitar el desarrollo modular de la interfaz en Fase 4 bajo las siguientes condiciones:
1. El backend sigue siendo desacoplado y autónomo.
2. La interfaz de usuario es tratada como un consumidor cliente más.

### 2. Manejo de credenciales y seguridad web
- Los endpoints públicos (`/profesionales`, `/sillones`, `/prestaciones`, `/disponibilidad`, `/reservas`) no requieren autenticación y son de acceso directo desde la UI guest.
- Para los endpoints protegidos (recepción y agenda de odontólogo), el bundle de frontend no debe incluir claves maestras hardcodeadas. En el entorno de demo local, la UI requerirá el ingreso de la clave de acceso en tiempo de ejecución (guardada en memoria/sessionStorage) o mediante un proxy mínimo, previniendo que las claves maestras formen parte de los artefactos estáticos de distribución.

### 3. Trazabilidad de errores
El frontend debe mapear directamente los códigos de error del contrato `{code, message}` para informar al usuario de forma amigable (por ejemplo, distinguiendo choque de profesional vs choque de sillón vs límite diario de paciente), sin intentar parsear cadenas de texto no estructuradas.

## Risks / Trade-offs
- [Exposición de claves en demo] → Mitigado al no empaquetar API keys en archivos `.env` estáticos del frontend (`VITE_*`).
- [Sobrecarga de desarrollo] → Se mantiene el frontend como módulos incrementales e independientes tras completar la API transaccional.

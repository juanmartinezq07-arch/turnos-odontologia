# Ficha de Investigación: Integración de Skill Propia y Servidor MCP en TurnosAR

**Proyecto**: TurnosAR — Sistema de Gestión de Turnos Odontológicos (`turnos-odontologia`)  
**Materia**: Metodología de Sistemas I (TUP - UTN)  
**Fecha de consulta y elaboración**: 04/11/2026  

---

## 1. Necesidad Real Detectada y Change Elegido

### Estado del proyecto y selección del Change
Al revisar el roadmap canónico en `CHANGES.md`, la Fase 1 (`C-01`) y toda la Fase 2 (`C-20`, `C-21`, `C-24`, `C-25`, `C-26`, `C-27`, `C-28`, `C-30`) ya se encuentran implementadas y archivadas (`[x]`). Esto habilita el ingreso a la **Fase 3 — Agenda operable (GATE 2–4)**, integrada por tres changes pendientes de backend:
- **`C-22` (`api-cancelacion-recepcionista`)**: `POST /turnos/{id}/cancelacion` (dependencias `C-01` y `C-20` ya completadas).
- **`C-23` (`api-reprogramacion-atómica`)**: `POST /turnos/{id}/reprogramacion` en una única transacción con rollback total ante conflictos `RN02`/`RN03`/`RN05` (depende de `C-20` y `C-22`).
- **`C-29` (`reservas-guest`)**: `POST /reservas` y `POST /reservas/{token}/cancelacion` públicos con auto-asignación de sillón y rate-limit (dependencias `C-01`, `C-21`, `C-24`, `C-25` y `C-26` ya completadas).

Se elige **`C-22` (`api-cancelacion-recepcionista`)** como change principal para demostrar la preparación e integración inicial (por tener sus dependencias `C-01` y `C-20` cerradas), extendiendo el alcance de la herramienta a los otros dos changes de la Fase 3 (`C-23` y `C-29`).

### Necesidad de una Skill Propia (tarea repetible)
Al preparar y revisar los artefactos SDD (`proposal.md`, `specs/*/spec.md`, `design.md`, `tasks.md`) de los changes `C-22`, `C-23` y `C-29`, el equipo debe repetir manualmente una auditoría de dominio crítica:
1. Verificar que la especificación contenga al menos **tres escenarios verificables** (funcionamiento esperado, error de negocio con contrato `{code, message}` y caso de borde como idempotencia en `C-22`, rollback atómico en `C-23` o colisión concurrente/rate-limit en `C-29`).
2. Comprobar que no se violen las invariantes de PostgreSQL (`RN01` a `RN05`, liberación efectiva del slot parcial `WHERE estado='activo'` en `RN04` y preservación de `cancelled_at`).
3. Garantizar el cumplimiento de la **Ley 25.326** (`extra="forbid"` en schemas Pydantic para rechazar datos clínicos y uso exclusivo de datos ficticios en tests).

### Necesidad de un Servidor MCP (acceso a información externa)
Para diseñar e implementar con precisión las operaciones transaccionales de la Fase 3 sobre **SQLAlchemy 2.0 (`AsyncSession`)** y **FastAPI**, el agente necesita consultar documentación oficial actualizada sobre el manejo de transacciones asíncronas, bloqueos/concurrencia, preservación de atributos tras `commit`/`flush` y manejo de excepciones HTTP, evitando alucinar métodos deprecados de SQLAlchemy 1.x.

---

## 2. Investigación de Skill Creadora y Diseño de la Skill Propia (`auditor-changes-22-23-29`)

### Skill Creadora Investigada
- **Nombre**: `skill-creator`
- **Fuente oficial y autor**: Anthropic — repositorio oficial `anthropics/skills` (`https://github.com/anthropics/skills/tree/main/skills/skill-creator`).
- **Compatibilidad con el agente**: Nativa en Antigravity / Claude Code mediante formato estándar `SKILL.md` (frontmatter YAML `name` + `description` e instrucciones Markdown con *progressive disclosure*).
- **Instalación y comprobación**: Instalada en el directorio de configuración del agente (`~/.gemini/config/skills/skill-creator/SKILL.md`). Se comprueba listando las skills activas en la sesión del agente y leyendo su archivo `SKILL.md`.

### Diseño de la Skill Propia: `auditor-changes-22-23-29`
- **Propósito**: Auditar los artefactos OpenSpec (`proposal.md`, `spec.md`, `design.md`, `tasks.md`) y los tests de los changes de la Fase 3 (`C-22`, `C-23` y `C-29`) contra las reglas `RN01–RN05`, la matriz de escenarios obligatorios y la restricción legal Ley 25.326.
- **Cuándo se activa (Trigger)**: Al preparar (`/opsx:propose`), revisar o verificar (`/opsx:verify`) cualquiera de los changes `C-22` (cancelación), `C-23` (reprogramación atómica) o `C-29` (reservas guest).
- **Entradas necesarias**: Ruta de la carpeta del change (`openspec/changes/<change-name>/`), sección correspondiente en `CHANGES.md` y archivos de reglas de negocio (`knowledge-base/05_reglas_de_negocio.md`).
- **Procedimiento**:
  1. Inspecciona `specs/*/spec.md` verificando la presencia explícita de al menos 3 escenarios: (a) flujo esperado, (b) error de negocio (`404 NO_ENCONTRADO`, `409 RN02_*/RN05`, `422 RN03_*`, `401`) y (c) caso de borde específico del change (`C-22`: idempotencia de `cancelled_at`; `C-23`: rollback total si falla el nuevo turno; `C-29`: carrera concurrente y token).
  2. Contrasta `design.md` y `tasks.md` contra las invariantes de persistencia (`WHERE estado='activo'`, `now()` inyectado, zona horaria `America/Argentina/Buenos_Aires`, notificación *best-effort* `C-28`).
  3. Verifica el cumplimiento de Ley 25.326 (`extra="forbid"` y datos sintéticos).
- **Resultado esperado y criterios de revisión**: Emite un dictamen estructurado en tabla Markdown (`PASS` / `FAIL` por criterio) con hallazgos concretos y correcciones requeridas antes de pasar a `/opsx:apply`.
- **Ubicación y referencia**: Se guarda versionada dentro del repositorio en `.agents/skills/auditor-changes-22-23-29/SKILL.md` (con copia documental en `mcp-skill/auditor-changes-22-23-29/SKILL.md`), registrándola en `.atl/skill-registry.md` y `AGENTS.md`.

---

## 3. Comparación y Selección del Servidor MCP

Se relevaron y compararon dos servidores MCP existentes compatibles con el stack del proyecto:

| Criterio | Opción 1 (Seleccionada): **Context7 MCP** (`@upstash/context7-mcp`) | Opción 2 (Comparada): **PostgreSQL MCP** (`@modelcontextprotocol/server-postgres`) |
|---|---|---|
| **Propósito** | Recuperar documentación oficial actualizada y fragmentos de código de librerías específicas (`SQLAlchemy 2.0`, `FastAPI`, `Pydantic v2`, `pytest`). | Inspeccionar el esquema de una base de datos PostgreSQL y ejecutar consultas SQL de solo lectura (`SELECT`). |
| **Capacidades (Tools)** | `resolve-library-id` (resuelve el identificador canónico del paquete) y `query-docs` (consulta documentación oficial indexada). | `query` (ejecuta consultas SQL en una transacción `READ ONLY`) y exposición de recursos de tablas/columnas. |
| **Compatibilidad** | Compatible con Antigravity, Claude Code y Cursor vía protocolo estándar MCP (`stdio` / `http`). | Compatible con Antigravity y clientes MCP mediante ejecución local con Node.js (`npx`). |
| **Requisitos y conexión** | Node.js >= 18 (`npx -y @upstash/context7-mcp`). No requiere levantar contenedores adicionales. | Node.js >= 18 + contenedor Docker `postgres:16` activo y cadena de conexión `DATABASE_URL`. |
| **Permisos, credenciales y costos** | **Gratuito ($0)** y de acceso público. No requiere credenciales obligatorias ni accede a bases de datos ni archivos locales con datos de pacientes. | **Gratuito ($0)** (open-source). Requiere entregar usuario y contraseña de la base local en la configuración del cliente MCP. |

### Justificación de la elección (`Context7 MCP`)
Se selecciona **`Context7 MCP`** porque resuelve de forma directa la necesidad técnica de consultar patrones exactos de **SQLAlchemy 2.0 AsyncSession** y **FastAPI** para diseñar las operaciones transaccionales de `C-22`, `C-23` y `C-29`, sin exponer credenciales de base de datos ni abrir una superficie de acceso sobre registros de pacientes (cumpliendo estrictamente la restricción de **Ley 25.326** y presupuesto **$0**).

### Pasos de configuración, verificación y límites de uso
1. **Configuración en el cliente (Antigravity)**: Declarado en la configuración MCP del agente (`~/.gemini/antigravity-cli/mcp/context7/`) exponiendo las herramientas *lazy* `resolve-library-id` y `query-docs`.
2. **Comprobación de conexión y ejecución**: Se invoca `call_mcp_tool` sobre `ServerName: "context7"` ejecutando primero `resolve-library-id` (ej. `libraryName: "sqlalchemy"`) y luego `query-docs` con la consulta técnica del change.
3. **Información consultada y límites**: Solo consulta documentación técnica pública; **no modifica archivos ni bases de datos** y tiene prohibido enviar datos sensibles o reales en los parámetros de búsqueda (`query`).

---

## 4. Archivos de la Fundación que se Actualizarán

1. `.agents/skills/auditor-changes-22-23-29/SKILL.md`: Creación de la skill propia en el directorio de skills del repositorio.
2. `.atl/skill-registry.md`: Registro de `auditor-changes-22-23-29` en la tabla de skills de proyecto y sus reglas de activación.
3. `AGENTS.md`: Incorporación de las instrucciones de uso de la skill `auditor-changes-22-23-29` y documentación de `Context7 MCP` como integración externa (propósito, tools, cuándo usarlo y límites).
4. `README.md`: Documentación reproducible de requisitos, configuración sin secretos y prueba de conexión del servidor MCP.
5. `CHANGES.md` y `openspec/changes/c-22-api-cancelacion-recepcionista/`: Artefactos SDD preparados y auditados con ambas herramientas.

---

## 5. Fuentes Consultadas

1. **Anthropic Skills Repository (`skill-creator`)**: Documentación oficial y código fuente de la skill creadora. URL: `https://github.com/anthropics/skills/tree/main/skills/skill-creator` — Fecha de consulta: 04/11/2026.
2. **Model Context Protocol (MCP) Specification & Servers**: Repositorio oficial de referencia de servidores MCP (`@modelcontextprotocol/server-postgres`). URL: `https://github.com/modelcontextprotocol/servers` — Fecha de consulta: 04/11/2026.
3. **Upstash Context7 MCP**: Documentación oficial e integración del servidor MCP de documentación para agentes. URL: `https://github.com/upstash/context7` — Fecha de consulta: 04/11/2026.
4. **SQLAlchemy 2.0 AsyncIO Documentation**: Documentación oficial sobre `AsyncSession` y transacciones. URL: `https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html` — Fecha de consulta: 04/11/2026.

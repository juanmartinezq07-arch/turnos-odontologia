# Informe de Aplicación: Integración de Skill Propia y Servidor MCP en TurnosAR

**Proyecto**: TurnosAR — Sistema de Gestión de Turnos Odontológicos (`turnos-odontologia`)  
**Materia**: Metodología de Sistemas I (TUP - UTN)  
**Fecha**: 04/11/2026  

---

## 1. Resumen de Resultados e Incorporaciones

Se completó la integración de la skill propia **`auditor-changes-22-23-29`** (creada a partir de `skill-creator`) y del servidor MCP **`Context7 MCP`** (`@upstash/context7-mcp`) en la fundación de **TurnosAR**, aplicándolos en la preparación SDD del change **`C-22` (`c-22-api-cancelacion-recepcionista`)** y dejándolos operativos para los siguientes changes de la Fase 3 (`C-23` y `C-29`).

- **Estado de validación OpenSpec**: `openspec validate c-22-api-cancelacion-recepcionista --strict` → **`Change 'c-22-api-cancelacion-recepcionista' is valid`** (`4/4 artifacts complete`: `proposal.md`, `specs/turnos/spec.md`, `design.md`, `tasks.md`).

---

## 2. Evidencia de Uso del Servidor MCP y de la Skill Propia

### 2.1 Ejecución de Herramientas Reales del Servidor MCP (`Context7`)
- **Registro completo**: [`../../mcp-skill/evidencias/ejecucion-mcp-context7.md`](../../mcp-skill/evidencias/ejecucion-mcp-context7.md) y configuración reproducible en [`../../mcp-skill/config-mcp-ejemplo.json`](../../mcp-skill/config-mcp-ejemplo.json).
- **Solicitud realizada**:
  1. `resolve-library-id` con `libraryName: "SQLAlchemy"` → resolvió `/websites/sqlalchemy_en_20_orm`.
  2. `query-docs` sobre `/websites/sqlalchemy_en_20_orm` consultando el ciclo de vida de `AsyncSession`, `expire_on_commit=False`, `session.get`, `commit` y `rollback`.
- **Resultado obtenido y aporte al change `C-22` (y `C-23`)**:
  Confirmó que al usar `async_sessionmaker(engine, expire_on_commit=False)` los atributos de la entidad `Turno` (`id`, `estado`, `cancelled_at`) siguen disponibles en memoria luego de `await session.commit()` sin disparar consultas implícitas (`MissingGreenlet`). Esto fundamentó la decisión técnica **D-01** en `openspec/changes/c-22-api-cancelacion-recepcionista/design.md` para serializar `TurnoOut` y ejecutar el hook post-commit `notify_turn_updated(turno.id)`.

### 2.2 Invocación de la Skill Propia (`auditor-changes-22-23-29`)
- **Registro completo**: [`../../mcp-skill/evidencias/auditoria-skill-c22.md`](../../mcp-skill/evidencias/auditoria-skill-c22.md).
- **Solicitud realizada**: Auditar los 4 artefactos de `openspec/changes/c-22-api-cancelacion-recepcionista/` contra las reglas `RN01–RN05` (`KB-04`, `KB-05`, `KB-07`), los 3 escenarios verificables exigidos y la Ley 25.326.
- **Resultado obtenido y aporte al change `C-22`**:
  Emitió la matriz de auditoría sobre los 6 criterios obligatorios (`PASS` en los 6 tras aplicar las correcciones de revisión crítica), asegurando trazabilidad 1 a 1 entre los escenarios de `specs/turnos/spec.md` y las tareas de prueba en `tasks.md` (`T2.2`, `T2.3` y `T2.4`).

---

## 3. Archivos Modificados en el Proyecto y Motivo

| Archivo / Ruta | Tipo | Motivo de la creación o modificación |
|---|---|---|
| `.agents/skills/auditor-changes-22-23-29/SKILL.md` | Nuevo | Instalación de la skill propia versionada en el directorio de skills del repositorio. |
| `.atl/skill-registry.md` | Modificado | Registro de `auditor-changes-22-23-29` en la tabla `User Skills` y adición de sus `Compact Rules` para subagentes. |
| `AGENTS.md` y `CLAUDE.md` | Modificados | Instrucciones de cuándo/cómo usar la skill `auditor-changes-22-23-29` y documentación de `Context7 MCP` como integración externa (sin registrarlo como skill). |
| `README.md` | Modificado | Documentación reproducible de requisitos, configuración JSON sin secretos y prueba de conexión del MCP. |
| `CHANGES.md` | Modificado | Referencia de preparación de `C-22` (`openspec/changes/c-22-api-cancelacion-recepcionista/`) manteniendo su checkbox en `[ ]` según el Punto 7 de la consigna. |
| `openspec/changes/c-22-api-cancelacion-recepcionista/*` | Nuevos | Artefactos SDD completos (`proposal.md`, `specs/turnos/spec.md`, `design.md`, `tasks.md`) validados con `--strict`. |
| `mcp-skill/*` y `docs/skills-mcp/*` | Nuevos | Ficha de investigación (`investigacion.md`), informe de aplicación (`aplicacion.md`), configuración MCP y carpeta de evidencias. |

---

## 4. Revisión Crítica: Detección de Omisiones (Antes vs. Después) y Limitaciones

### Omisiones detectadas y corregidas gracias a `auditor-changes-22-23-29`
1. **No duplicación de notificaciones en reintentos idempotentes (`KB-07 §Flujo 3` L63)**:
   - *Antes*: Un enfoque ingenuo que ejecuta `commit()` y `notify_turn_updated(turno.id)` en toda llamada a `POST /turnos/{id}/cancelacion` habría registrado múltiples eventos `"updated"` en `MockNotificationService` ante reintentos de red sobre un turno ya cancelado.
   - *Después*: En `design.md` (§D-01/D-02) y `tasks.md` (`T2.4`) se especificó que cuando `turno.estado == "cancelado"`, el servicio retorna inmediatamente `200 OK` conservando el `cancelled_at` original (`T1`) **sin emitir una segunda notificación**.
2. **Liberación simultánea de `RN02` y `RN05` al cancelar**:
   - *Antes*: El borrador inicial del Escenario 1 solo verificaba que el slot quedara libre para los constraints `EXCLUDE` de profesional y sillón (`RN02`), omitiendo el índice único parcial `rn05_un_activo_por_dia` (`WHERE estado = 'activo'`).
   - *Después*: En `specs/turnos/spec.md` (L14) y `tasks.md` (`T2.2`) se exigió verificar que tras cancelar el turno se pueda dar de alta otro turno activo en el mismo horario con el **mismo profesional, sillón y paciente**, comprobando la liberación en los tres predicados parciales de PostgreSQL.

### Limitaciones identificadas
- **Alcance de la skill**: `auditor-changes-22-23-29` está especializada en las invariantes transaccionales de backend de la Fase 3 (`C-22`, `C-23`, `C-29`); para los changes visuales de la Fase 4 (`C-31` a `C-35`) se requiere combinarla con skills de frontend/UI.
- **Alcance del MCP (`Context7`)**: Al ser un servidor de documentación pública, valida el uso correcto de las APIs de `SQLAlchemy 2.0` y `FastAPI`, pero no reemplaza la ejecución de `pytest` contra el contenedor real de PostgreSQL 16 (`btree_gist`).

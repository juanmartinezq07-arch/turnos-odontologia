---
name: auditor-changes-22-23-29
description: Audita los artefactos OpenSpec (proposal.md, specs/*/spec.md, design.md, tasks.md) y la implementacion de los changes de Fase 3 de TurnosAR (C-22 api-cancelacion-recepcionista, C-23 api-reprogramacion-atomica y C-29 reservas-guest). Usala SIEMPRE que el usuario prepare, proponga (/opsx:propose), revise o verifique (/opsx:verify) los changes C-22, C-23 o C-29, o cuando pida validar escenarios de cancelacion, reprogramacion atomica o reservas publicas guest contra las reglas de negocio RN01-RN05 y la Ley 25.326.
---

# Auditor de Changes de Fase 3 (`C-22`, `C-23`, `C-29`) — TurnosAR

Esta skill estandariza el control de calidad de los tres changes que conforman la **Fase 3 (Agenda operable)** de **TurnosAR**, asegurando que tanto los artefactos de especificación como el código cumplan las invariantes declarativas en PostgreSQL 16 (`RN01`–`RN05`), la matriz de escenarios obligatorios de la cátedra y la restricción legal de protección de datos personales (**Ley 25.326**).

---

## Cuándo activar esta skill

Activá y seguí este procedimiento en dos momentos del flujo OPSX:
1. **Durante la preparación (`/opsx:propose`)**: Inmediatamente después de redactar `proposal.md`, `specs/*/spec.md`, `design.md` y `tasks.md` de `C-22`, `C-23` o `C-29`, para auditar que no falten escenarios ni reglas antes de escribir código.
2. **Durante la verificación (`/opsx:verify` / cierre de `/opsx:apply`)**: Para contrastar los tests de `pytest` implementados contra cada criterio de la tabla de auditoría.

---

## Entradas necesarias

Antes de emitir el dictamen, leé los siguientes archivos del proyecto:
1. **Sección del change en el roadmap**: `CHANGES.md` (sección `[C-22]`, `[C-23]` o `[C-29]`).
2. **Reglas de negocio y arquitectura**:
   - `knowledge-base/04_modelo_de_datos.md` (§Turno: columnas `estado`, `cancelled_at`, `token_cancelacion`, constraints `rn02_profesional`, `rn02_sillon`, `rn05_un_activo_por_dia`).
   - `knowledge-base/05_reglas_de_negocio.md` (§RN01 a §RN05 y §Excepciones).
3. **Artefactos del change bajo análisis**:
   - `openspec/changes/<nombre-change>/proposal.md`
   - `openspec/changes/<nombre-change>/specs/*/spec.md`
   - `openspec/changes/<nombre-change>/design.md`
   - `openspec/changes/<nombre-change>/tasks.md`

---

## Procedimiento paso a paso

### Paso 1 — Auditoría de los 3 Escenarios Verificables (Obligatorio en `spec.md` y `tasks.md`)
Verificá que el archivo `specs/*/spec.md` contenga **como mínimo tres escenarios** con formato `#### Scenario:` (`WHEN` / `THEN`), y que `tasks.md` indique explícitamente con qué test de `pytest` se verificará cada uno:

1. **Escenario de Funcionamiento Esperado (Happy Path)**:
   - En **`C-22`**: `POST /turnos/{id}/cancelacion` con `X-API-Key` válida sobre un turno `activo` pasa a `estado = 'cancelado'`, asigna `cancelled_at = now()` (UTC / `America/Argentina/Buenos_Aires`), dispara notificación *best-effort* (`notify_turn_updated`) y **libera el slot** para que otro turno activo pueda ocupar ese rango sin chocar con `rn02_*` ni `rn05_un_activo_por_dia`.
   - En **`C-23`**: `POST /turnos/{id}/reprogramacion` hacia un slot libre marca el turno original como `cancelado` (`cancelled_at = now()`) e inserta el nuevo turno `activo` con `fin` recalculado (`RN01`) en **una sola transacción**.
   - En **`C-29`**: `POST /reservas` público crea el turno `activo` (auto-asignando el primer sillón libre si `sillon_id` es nulo), genera y devuelve `token_cancelacion` (`201 Created`), y `POST /reservas/{token}/cancelacion` cancela ese turno liberando el slot.

2. **Escenario de Error de Negocio (Contrato `{code, message}`)**:
   - Todo error debe respetar el contrato JSON `{"code": "...", "message": "..."}` sin exponer trazas SQL (`500`).
   - En **`C-22`**: `404` con `code = "NO_ENCONTRADO"` si el `turno_id` no existe; `401` si falta o es inválida la `X-API-Key`.
   - En **`C-23`**: `409` (`RN02_PROFESIONAL`, `RN02_SILLON`, `RN05`) o `422` (`RN03_PASADO`, `RN03_FUERA_DE_HORARIO`) cuando el slot destino es inválido, o `404 NO_ENCONTRADO` si el turno original no existe / no está activo.
   - En **`C-29`**: `409` (`RN02_*`, `RN05`) cuando no hay sillón libre o el paciente ya tiene turno ese día; `404` con token inexistente; `429` al superar `RESERVA_RATE_LIMIT` (`10/min`).

3. **Escenario de Caso de Borde (Edge Case)**:
   - En **`C-22`**: **Idempotencia de cancelación** — llamar por segunda vez a `POST /turnos/{id}/cancelacion` sobre un turno que ya tiene `estado = 'cancelado'` devuelve `200 OK` y **conserva intacto el `cancelled_at` original** (no lo pisa con un nuevo timestamp).
   - En **`C-23`**: **Atomicidad y Rollback total** — si la inserción del nuevo turno falla por `RN02`, `RN03` o `RN05`, la transacción hace rollback completo y el turno original **permanece en `estado = 'activo'` con `cancelled_at = NULL`** en la base de datos.
   - En **`C-29`**: **Colisión concurrente** — dos `POST /reservas` simultáneos al último sillón/slot disponible terminan exactamente en un `201` y un `409` (garantizado por `EXCLUDE USING gist`).

### Paso 2 — Auditoría de Reglas Transversales del Dominio
Comprobá que el diseño (`design.md`) y las tareas (`tasks.md`) respeten:
- **Inyección de reloj (`now`) y zona horaria**: Uso de `America/Argentina/Buenos_Aires` y `timestamptz`, sin depender de `datetime.now()` naive.
- **Notificaciones *best-effort* (`C-28`)**: Llamada a `get_notification_service().notify_turn_updated(...)` o `notify_turn_created(...)` **después del `commit()`**, capturando cualquier excepción para no abortar la operación principal.
- **Base de datos real en tests**: Prohibido usar SQLite en memoria; todas las pruebas de persistencia y endpoints corren contra PostgreSQL 16 real.

### Paso 3 — Auditoría de Ley 25.326 (Protección de Datos Personales)
- **Schemas Pydantic**: Todo payload de entrada (`Request`) debe declarar `model_config = ConfigDict(extra="forbid")` para rechazar con `422` cualquier intento de enviar campos clínicos (`diagnostico`, `obra_social`, `observaciones_clinicas`, etc.).
- **Datos sintéticos**: Verificar que ningún ejemplo en specs ni fixture en tests contenga nombres, teléfonos, DNI o correos reales (usar formato `"Paciente Demo"`, `11-0000-xxxx`, `@example.com`).

---

## Formato de Salida (Reporte de Auditoría)

Al ejecutar esta skill, entregá **siempre** el resultado con la siguiente estructura:

```markdown
## Reporte de Auditoría — `auditor-changes-22-23-29`
- **Change auditado**: `<C-22 / C-23 / C-29>`
- **Etapa**: `<Preparación (propose) | Verificación (verify)>`

| # | Criterio de Auditoría | Estado | Evidencia / Ubicación |
|---|---|---|---|
| 1 | Escenario 1: Funcionamiento esperado + liberación de slot (RN04/RN01) | PASS / FAIL | `specs/.../spec.md` L... |
| 2 | Escenario 2: Error de negocio con contrato `{code, message}` | PASS / FAIL | `specs/.../spec.md` L... |
| 3 | Escenario 3: Caso de borde (Idempotencia / Rollback atómico / Concurrencia) | PASS / FAIL | `specs/.../spec.md` L... |
| 4 | Trazabilidad en `tasks.md` (1 tarea/test verificable por escenario) | PASS / FAIL | `tasks.md` L... |
| 5 | Integración post-commit con `NotificationService` (best-effort C-28) | PASS / FAIL | `design.md` / código |
| 6 | Cumplimiento Ley 25.326 (`extra="forbid"` + datos 100% ficticios) | PASS / FAIL | `spec.md` / `tests/` |

### Hallazgos y Correcciones Aplicadas
- **Observaciones detectadas**: [Detallar cualquier omisión, ambigüedad o caso de borde faltante, o indicar si pasó limpio en primera instancia y qué caso límite se puso a prueba].
- **Acción tomada**: [Explicar qué se ajustó en `spec.md`, `design.md`, `tasks.md` o en el código].
```

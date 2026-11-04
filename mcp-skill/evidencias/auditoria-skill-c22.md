# Evidencia de Invocación de la Skill Propia (`auditor-changes-22-23-29`)

**Fecha de ejecución**: 04/11/2026  
**Skill invocada**: `.agents/skills/auditor-changes-22-23-29/SKILL.md`  
**Change auditado**: `C-22` (`c-22-api-cancelacion-recepcionista`)  

---

## 1. Solicitud Realizada al Agente

Se solicitó aplicar el procedimiento completo de la skill `auditor-changes-22-23-29` sobre los artefactos generados para `openspec/changes/c-22-api-cancelacion-recepcionista/` (`proposal.md`, `specs/turnos/spec.md`, `design.md` y `tasks.md`), contrastándolos contra `CHANGES.md` §C-22, `knowledge-base/04_modelo_de_datos.md` y `knowledge-base/05_reglas_de_negocio.md`.

---

## 2. Revisión Crítica: Defecto Detectado y Corregido (Antes vs. Después)

Durante el Paso 1 de la auditoría (`Auditoría de los 3 Escenarios Verificables` y `Paso 2 — Reglas Transversales`), la skill detectó **dos omisiones críticas** en el borrador inicial de la especificación y diseño de `C-22`:

### Omisión 1: Comportamiento de `NotificationService` ante reintentos idempotentes
- **Antes (Borrador inicial)**: El diseño proponía ejecutar `UPDATE turno SET estado='cancelado', cancelled_at = COALESCE(cancelled_at, now())` y llamar siempre a `notify_turn_updated(turno.id)` al final del endpoint.
- **Problema detectado por la skill (`auditor-changes-22-23-29` + `KB-07 §Flujo 3` L63)**: `KB-07 §Flujo 3` establece que *"Cancelar algo ya cancelado → idempotente (no duplica el efecto)"*. Si una segunda llamada a `POST /turnos/{id}/cancelacion` vuelve a disparar `notify_turn_updated(turno.id)`, duplica el evento de notificación en `MockNotificationService.events`.
- **Después (Corregido en `design.md` §D-01/D-02 y `tasks.md` T2.4)**: Si `turno.estado == "cancelado"`, la función retorna inmediatamente el turno con su `cancelled_at` original (`T1`) **sin ejecutar un nuevo `commit()` ni emitir una segunda notificación**.

### Omisión 2: Verificación explícita de liberación del índice `RN05` además de `RN02`
- **Antes (Borrador inicial)**: El escenario 1 de `specs/turnos/spec.md` solo mencionaba que la cancelación liberaba el slot para los constraints `EXCLUDE` de profesional y sillón (`RN02`).
- **Problema detectado por la skill (`auditor-changes-22-23-29` + `KB-04 §Turno`)**: Desde `C-21`/`C-26`, la tabla `turno` también tiene el índice único parcial `rn05_un_activo_por_dia` con predicado `WHERE (estado = 'activo')`. Si el paciente cancela su único turno del día, debe poder agendar otro turno ese mismo día sin recibir `409 RN05`.
- **Después (Corregido en `specs/turnos/spec.md` L14 y `tasks.md` T2.2)**: Se actualizó el escenario 1 para exigir que un nuevo turno en el mismo horario con el **mismo profesional, sillón y paciente** se cree con `201 Created`, probando simultáneamente la liberación de `rn02_profesional`, `rn02_sillon` y `rn05_un_activo_por_dia`.

---

## 3. Resultado Obtenido (Tabla de Dictamen Final)

## Reporte de Auditoría — `auditor-changes-22-23-29`
- **Change auditado**: `C-22` (`c-22-api-cancelacion-recepcionista`)
- **Etapa**: `Preparación (propose)`

| # | Criterio de Auditoría | Estado | Evidencia / Ubicación |
|---|---|---|---|
| 1 | Escenario 1: Funcionamiento esperado + liberación de slot (RN04/RN02/RN05) | PASS | `openspec/changes/c-22-api-cancelacion-recepcionista/specs/turnos/spec.md` L10-L15 |
| 2 | Escenario 2: Error de negocio con contrato `{code, message}` (`404 NO_ENCONTRADO` y `401`) | PASS | `openspec/changes/c-22-api-cancelacion-recepcionista/specs/turnos/spec.md` L26-L39 |
| 3 | Escenario 3: Caso de borde (Idempotencia conservando `cancelled_at == T1`) | PASS | `openspec/changes/c-22-api-cancelacion-recepcionista/specs/turnos/spec.md` L17-L24 |
| 4 | Trazabilidad en `tasks.md` (1 tarea/test verificable por escenario) | PASS | `openspec/changes/c-22-api-cancelacion-recepcionista/tasks.md` T2.2, T2.3 y T2.4 |
| 5 | Integración post-commit con `NotificationService` (best-effort C-28 sin duplicar en reintentos) | PASS | `openspec/changes/c-22-api-cancelacion-recepcionista/design.md` §D-01 y §D-02 |
| 6 | Cumplimiento Ley 25.326 (`extra="forbid"` + datos 100% ficticios, sin body clínico) | PASS | `openspec/changes/c-22-api-cancelacion-recepcionista/design.md` §Risks / Trade-offs |

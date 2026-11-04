# Design

## Context

`C-22` resolvió la cancelación individual y la persistencia de `cancelled_at`. `C-23` aborda la operación combinada de reprogramación. En PostgreSQL, un `UPDATE turno SET estado='cancelado'` dentro de una transacción libera el slot cubierto por los constraints `EXCLUDE USING gist ... WHERE (estado='activo')` para esa misma transacción, permitiendo insertar el nuevo turno (o en otro horario) de forma limpia. Si el nuevo turno viola constraints (`rn02_profesional`, `rn02_sillon`, `rn05_un_activo_por_dia`), se genera una excepción que debe provocar `await session.rollback()`, restaurando el turno original a su estado `activo`.

## Goals / Non-Goals

**Goals:**
- Endpoint `POST /turnos/{turno_id}/reprogramacion` protegido con `require_recepcion`.
- Atomicidad garantizada: nunca puede quedar el turno original cancelado si el nuevo no se creó exitosamente.
- Soporte para cambio de fecha/hora manteniendo profesional, paciente y prestación, permitiendo cambiar opcionalmente de sillón.
- Notificaciones post-commit para ambos eventos: `notify_turn_updated(original.id)` y `notify_turn_created(nuevo.id)`.

**Non-Goals:**
- Modificar el profesional o la prestación (la reprogramación clínica reubica el turno de la misma prestación y odontólogo).
- Crear migraciones adicionales (el esquema actual soporta toda la operación).

## Decisions

### D-01: Ejecución en una sola transacción asíncrona con Savepoint o Rollback explícito
- **Decisión**: Dentro de `reprogramar_turno`:
  1. Obtener el turno original con `await session.get(Turno, turno_id)`.
  2. Validar que exista (si no, 404 `NO_ENCONTRADO`) y que `estado == "activo"` (si no, 409 `TURNO_NO_ACTIVO`).
  3. Pre-validar temporalidad (`_validar_temporalidad`) del nuevo rango `[nuevo_inicio, nuevo_fin)`. Si falla, abortar sin tocar nada.
  4. Marcar `original.estado = "cancelado"` y `original.cancelled_at = _ahora()`.
  5. Instanciar el nuevo `Turno` con los mismos `profesional_id`, `prestacion_id`, `paciente_id`, nuevo `inicio`, `fin` y sillón (nuevo o el mismo).
  6. Añadir el nuevo turno y ejecutar `await session.flush()`.
  7. Si `flush()` lanza `IntegrityError` o si un precheck detecta colisión, atrapar, ejecutar `await session.rollback()` y relanzar `DomainConflict` con el código mapeado (`RN02_PROFESIONAL`, `RN02_SILLON`, `RN05`).
  8. Si todo sale bien, `await session.commit()`, `await session.refresh(nuevo_turno)` y emitir notificaciones best-effort.
- **Justificación**: Mantiene una estricta atomicidad a nivel motor de base de datos.

### D-02: Schema estricto `TurnoReprogramar`
- **Decisión**: Payload de entrada en `backend/app/schemas/turno.py`:
  ```python
  class TurnoReprogramar(_Estricto):
      inicio: datetime
      sillon_id: uuid.UUID | None = None
  ```
  Con `model_config = ConfigDict(extra="forbid")` para impedir el ingreso de campos no contemplados o datos clínicos (Ley 25.326).

## Risks / Trade-offs

- **[Riesgo]** Carrera de concurrencia al mover de horario → **Mitigación**: Los constraints `EXCLUDE` en Postgres garantizan que si otro usuario toma el horario destino durante la transacción, el `flush()` falla con `IntegrityError`, el rollback restaura el turno original y el cliente recibe `409`.

# Proposal

## Why

La recepcionista necesita reprogramar un turno existente (`POST /turnos/{id}/reprogramacion`) moviéndolo a un nuevo horario y/o sillón de forma **atómica** (US-005 / CU03). En un consultorio, cancelar un turno y crear uno nuevo en pasos separados introduce el riesgo de que el nuevo turno choque (por `RN02`, `RN03` o `RN05`) y el paciente quede sin ningún turno. Este change garantiza que la cancelación del original y el alta del nuevo ocurran en una **única transacción**: si el nuevo slot choca o es inválido, se produce un **rollback total** y el turno original permanece intacto en estado `activo` (RN04).

## What Changes

- Agregar el endpoint `POST /turnos/{id}/reprogramacion` protegido por `require_recepcion` (`X-API-Key` con `API_KEY_RECEPCION`) en `backend/app/api/v1/turnos.py`.
- Crear el schema de entrada `TurnoReprogramar` en `backend/app/schemas/turno.py` con `inicio: datetime`, `sillon_id: uuid.UUID | None = None` y `model_config = ConfigDict(extra="forbid")`.
- Implementar `reprogramar_turno(session, turno_id, nuevo_inicio, nuevo_sillon_id=None)` en `backend/app/application/bookings.py`:
  - Verificar existencia del turno original; si no existe lanzar `NotFound("NO_ENCONTRADO")` -> 404.
  - Si el turno original no está `activo`, rechazar con 409 `TURNO_NO_ACTIVO`.
  - Recalcular `fin = rules.calcular_fin(nuevo_inicio, duracion_prestacion)`.
  - Validar temporalidad (`RN03_PASADO`, `RN03_FUERA_DE_HORARIO`) antes de modificar.
  - En una misma transacción: marcar el original `cancelado` (`cancelled_at = now()`), instanciar el nuevo turno con el mismo paciente, profesional y prestación (y nuevo o mismo sillón), y hacer `flush()`.
  - Si ocurre `IntegrityError` o precheck fallido (`RN02_PROFESIONAL`, `RN02_SILLON`, `RN05`), ejecutar `rollback()` completo asegurando que el original siga `activo`.
  - Si el commit es exitoso, emitir notificaciones best-effort (`notify_turn_updated` para el cancelado y `notify_turn_created` para el nuevo).
- Tests de integración en `backend/tests/test_reprogramacion_api.py` verificando reprogramación exitosa, rollback atómico ante choque RN02/RN05, rechazo de pasado (RN03) con original intacto, y errores 404/401.

## Capabilities

### New Capabilities
<!-- Extiende la capacidad existente turnos -->

### Modified Capabilities
- `turnos`: Agrega el requerimiento de reprogramación atómica de turno por recepcionista (`POST /turnos/{id}/reprogramacion`) con transacción única y rollback total ante conflictos.

## Impact

- **API (`backend/app/api/v1/turnos.py`)**: Nuevo endpoint `POST /turnos/{turno_id}/reprogramacion`.
- **Schemas (`backend/app/schemas/turno.py`)**: Nuevo schema `TurnoReprogramar`.
- **Aplicación (`backend/app/application/bookings.py`)**: Función transaccional `reprogramar_turno`.
- **Tests (`backend/tests/test_reprogramacion_api.py`)**: Nueva suite con aserciones de rollback y estado de la base de datos.

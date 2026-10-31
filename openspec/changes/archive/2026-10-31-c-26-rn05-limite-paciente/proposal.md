# Proposal

## Why

`C-21` creó la infraestructura de persistencia para RN05 (columna `token_cancelacion` e índice único parcial `rn05_un_activo_por_dia`), pero la regla no está implementada de punta a punta en la aplicación. Hoy dos turnos activos del mismo paciente el mismo día chocan en la base con `UniqueViolation` pero la API no devuelve el código `RN05` ni un mensaje claro. Este change cierra la pregunta de prioridad Alta de `KB-10` (IN-01) y el criterio L14 de US-001.

## What Changes

- Extender `conflict_code_from_integrity_error` en `app/core/errors.py` para mapear la violación del índice `rn05_un_activo_por_dia` al código `RN05`.
- Agregar validación de RN05 en la capa de aplicación (precheck antes del insert) para dar 409 con código `RN05` y mensaje claro, sin depender solo de la base.
- Agregar `require_odontologo` con `API_KEY_ODONTOLOGO` en `app/core/security.py` (necesario para C-27, pero incluido aquí por conveniencia de transversal).
- Tests: misma paciente mismo día → 409 `RN05`; distinto paciente → 201; otro día → 201.
- **Regresión anunciada en fixtures de C-01**: los fixtures existentes usan un único paciente (`11-0000-0001`) para dos turnos activos del mismo día. Con el índice de `C-21` hay que parametrizarlos con pacientes distintos para que los 26 tests originales sigan verdes.

## Capabilities

### New Capabilities

- `rn05-limite-paciente`: máximo 1 turno activo por paciente y día, con código de error `RN05` y mensaje machine-readable.

### Modified Capabilities

- `plataforma-mvp`: se agrega el código de error `RN05` al mapeo de `IntegrityError` y la validación de aplicación previa.

## Impact

- Código: `app/core/errors.py` (mapeo `rn05_un_activo_por_dia` → `RN05`), `app/core/security.py` (require_odontólogo), `app/application/bookings.py` (precheck RN05 si corresponde).
- Tests: `test_rn05_limite_paciente.py` (punta a punta), ajustes en fixtures de C-01 para separar pacientes.
- Regresión conocida: `test_rn02_solapamiento.py::test_borde_que_se_toca_no_choca` y `test_turnos_api.py::test_borde_201` usan un solo paciente para dos turnos activos mismo día; deben separarse en pacientes distintos.

## Open Questions

- Ninguna que cambie specs, enfoque o tasks.

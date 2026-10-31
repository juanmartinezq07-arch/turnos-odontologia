# Tasks

## 1. RED — tests de RN05 que fallan sin el código

- [x] 1.1 Escribir `backend/tests/test_rn05_limite_paciente.py`: POST a dos turnos activos mismo paciente/mismo día → espera 409 con `code="RN05"`; distintos pacientes → 201; otro día → 201. Verificar que falla porque el código de aplicación no devuelve RN05.
- [x] 1.2 Ajustar fixtures de C-01 que usan un solo paciente para dos turnos activos mismo día (`test_rn02_solapamiento.py`, `test_turnos_api.py`) para usar pacientes distintos, evitando la regresión del índice de C-21.

## 2. GREEN — código de aplicación

- [x] 2.1 Extender `conflict_code_from_integrity_error` en `app/core/errors.py` para mapear `rn05_un_activo_por_dia` → `"RN05"`.
- [x] 2.2 Agregar `require_odontologo` en `app/core/security.py` con `API_KEY_ODONTOLOGO`.
- [x] 2.3 Agregar precheck de RN05 en `app/application/bookings.py` (consulta turno activo del mismo paciente mismo día antes del insert).
- [x] 2.4 Verificar `pytest tests/test_rn05_limite_paciente.py` en verde.

## 3. Verificación integral

- [x] 3.1 Correr suite completa `pytest` y verificar 44 tests pasados (incluyendo los ajustados de C-01).
- [x] 3.2 Verificar que los tests de C-21 (migración 005, índice parcial) siguen verdes.

## Explícitamente fuera de este change

- Uso de `token_cancelacion` en endpoints (es `C-29`).
- Notificaciones mock (`C-28`).
- Agenda del odontólogo (`C-27`, aunque `require_odontologo` se agrega aquí por conveniencia).

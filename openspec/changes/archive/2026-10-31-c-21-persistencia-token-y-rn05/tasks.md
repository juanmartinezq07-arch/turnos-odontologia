# Tasks

## 1. RED — test de migración 005 y de índice RN05

- [x] 1.1 Escribir `backend/tests/test_migracion_005.py`: aplica `alembic upgrade head` sobre una base limpia, verifica que existe `token_cancelacion TEXT UNIQUE` nullable, que existe el índice único parcial `rn05_un_activo_por_dia`, que `rn02_profesional`, `rn02_sillon` y `ck_turno_fin_mayor_inicio` siguen presentes; verificar que el test falla porque la 005 todavía no existe.
- [x] 1.2 Escribir `backend/tests/test_rn05_indice_parcial.py`: insertar dos turnos activos del mismo paciente el mismo día → espera violación de unicidad del índice parcial; insertar dos turnos activos del mismo paciente en días distintos → ambos persisten; insertar un turno cancelado + uno activo mismo día → se permite (el `WHERE estado='activo'` excluye cancelados).

## 2. GREEN — migración 005 y modelo

- [x] 2.1 Crear `backend/alembic/versions/005_persistencia_token_y_rn05.py` (`down_revision = "004_cancelled_at_paciente_fecha"`) con `upgrade` que agrega `token_cancelacion TEXT UNIQUE` y el índice único parcial `rn05_un_activo_por_dia`; y `downgrade` reversible que elimina ambos; verificar `alembic upgrade head` y `alembic downgrade -1` contra la base local.
- [x] 2.2 Actualizar `Turno` en `backend/app/domain/models.py` con `token_cancelacion: Mapped[str | None] = mapped_column(Text, unique=True, nullable=True)`; verificar que `Base.metadata.create_all` produce la misma columna e índice que espera el test.
- [x] 2.3 Completar los tests con escenarios de `downgrade` reversible y comportamiento del índice RN05; verificar `pytest tests/test_migracion_005.py tests/test_rn05_indice_parcial.py` en verde.

## 3. Verificación integral

- [x] 3.1 Correr la suite completa `pytest` y verificar que los tests de `C-01` y `C-20` siguen verdes y que el esquema no perdió invariantes: **41 passed, 0 failed**.
- [ ] 3.2 Ejecutar `openspec validate c-21-persistencia-token-y-rn05 --strict` y verificar que el change valida sin errores.

## Explícitamente fuera de este change

- Generar, validar y usar `token_cancelacion` en endpoints (es `C-29`).
- Validación de RN05 en la capa de aplicación con código de error `RN05` (es `C-26`).
- Reserva guest pública (`C-29`).

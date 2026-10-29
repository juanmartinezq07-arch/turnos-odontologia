# Tasks

## 1. RED — test del esquema de la 004

- [x] 1.1 Escribir `backend/tests/test_migracion_004.py`: aplica `alembic upgrade head` sobre una base limpia, verifica `cancelled_at TIMESTAMPTZ` nullable, el índice `idx_turno_paciente_fecha` sobre `(paciente_id, inicio)`, y que `rn02_profesional`, `rn02_sillon` y `ck_turno_fin_mayor_inicio` siguen presentes; verificar que el test falla porque la 004 todavía no existe

## 2. GREEN — migración 004 y modelo

- [x] 2.1 Crear `backend/alembic/versions/004_cancelled_at_paciente_fecha.py` (`down_revision = "003_recorte_alcance_c01"`) con `upgrade` que agrega `cancelled_at TIMESTAMPTZ` y `idx_turno_paciente_fecha`, y `downgrade` reversible que elimina ambos; verificar `alembic upgrade head` y `alembic downgrade -1` contra la base local
- [x] 2.2 Actualizar `Turno` en `backend/app/domain/models.py` con `cancelled_at` nullable (`DateTime(timezone=True)`) e `Index("idx_turno_paciente_fecha", "paciente_id", "inicio")`; verificar que `Base.metadata.create_all` produce la misma columna e índice que espera el test
- [x] 2.3 Completar el test con los escenarios de `downgrade` reversible, turno activo con `cancelled_at = NULL` y dos turnos del mismo paciente en fechas distintas que persisten; verificar `pytest tests/test_migracion_004.py` en verde

## 3. Verificación integral

- [x] 3.1 Correr la suite completa `pytest` y verificar que los tests de `C-01` (RN02, concurrencia, alta) siguen verdes y que el esquema no perdió invariantes
- [x] 3.2 Ejecutar `openspec validate persistencia-cancelacion-rn04 --strict` y verificar que el change valida sin errores

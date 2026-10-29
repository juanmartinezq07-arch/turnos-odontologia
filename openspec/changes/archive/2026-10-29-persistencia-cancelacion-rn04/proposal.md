# Proposal

## Why

`C-01` recortó el alcance y la migración 003 eliminó `cancelled_at`, por lo que hoy no existe dónde registrar cuándo se canceló un turno. Sin esa columna la política RN04 no puede persistirse y el slot no puede liberarse de forma auditable; además falta el índice `idx_turno_paciente_fecha` que la KB exige para consultar la agenda de un paciente por día. Este change restituye el esquema mínimo para habilitar la cancelación, sin tocar todavía la API.

## What Changes

- Nueva migración Alembic **004** (`upgrade`): `ALTER TABLE turno ADD COLUMN cancelled_at TIMESTAMPTZ` (nullable) y `CREATE INDEX idx_turno_paciente_fecha ON turno (paciente_id, inicio)`.
- `downgrade` reversible: elimina el índice y la columna, devolviendo el esquema exacto de la 003.
- Se actualiza el modelo `Turno` para reflejar `cancelled_at` (nullable, `DateTime(timezone=True)`) y el índice, sin cambiar `estado`, `fin` ni los dos `EXCLUDE`.
- Test de migración que verifica que tras `upgrade` existe la columna y el índice, que `estado`, `fin` y ambos `EXCLUDE` siguen intactos, y que `downgrade` revierte sin residuos.

## Capabilities

### New Capabilities

- Ninguna.

### Modified Capabilities

- `plataforma-mvp`: se agrega el requisito de esquema para la persistencia de la cancelación (columna `cancelled_at` nullable) y el índice de consulta `idx_turno_paciente_fecha`, preservando la invariante RN02 y el `CHECK (fin > inicio)` ya existentes.

## Impact

- Código: `backend/alembic/versions/004_*.py` (nueva), `backend/app/domain/models.py` (columna + índice), `backend/tests/` (nuevo test de migración).
- Base de datos: una columna nullable y un índice nuevo; no se edita ninguna migración aplicada (001–003 intactas).
- API: ninguna; `POST /turnos` no cambia. La cancelación por endpoint es `C-22`.
- Dependencias: ninguna nueva. No introduce invariantes ni reglas de negocio.

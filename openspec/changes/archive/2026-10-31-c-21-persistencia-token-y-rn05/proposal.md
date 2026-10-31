# Proposal

## Why

`C-01` recortó el alcance y la migración 003 eliminó `token_cancelacion` y el índice parcial `rn05_un_activo_por_dia`. Hoy no existe dónde persistir el token de cancelación para la reserva guest (CU02), ni la invariante RN05 (máximo 1 turno activo por paciente y día) vive declarada en la base de datos. Este change restituye el esquema mínimo para habilitar tanto el token como RN05 como invariante declarativa, igual que RN02.

## What Changes

- Nueva migración Alembic **005** (`upgrade`):
  - `ALTER TABLE turno ADD COLUMN token_cancelacion TEXT UNIQUE` (nullable, solo para reserva guest).
  - `CREATE UNIQUE INDEX rn05_un_activo_por_dia ON turno (paciente_id, ((inicio AT TIME ZONE 'America/Argentina/Buenos_Aires')::date)) WHERE estado = 'activo'`.
- `downgrade` reversible: elimina el índice y la columna, devolviendo el esquema exacto de la 004.
- Actualizar el modelo `Turno` en `app/domain/models.py` para reflejar `token_cancelacion` nullable.
- Test de migración que verifica que tras `upgrade` existe la columna y el índice único parcial, y que `downgrade` revierte sin residuos.
- Test de comportamiento RN05: dos turnos activos mismo paciente mismo día → viola el índice; otro día → commit.

## Capabilities

### New Capabilities

- Ninguna (infra de persistencia).

### Modified Capabilities

- `plataforma-mvp`: se agrega el requisito de esquema para el token de cancelación y la invariante RN05 en persistencia, preservando los EXCLUDE de RN02 y el `CHECK (fin > inicio)`.

## Impact

- Código: `backend/alembic/versions/005_*.py` (nueva), `backend/app/domain/models.py` (columna + índice), `backend/tests/` (nuevos tests).
- Base de datos: una columna nullable y un índice único parcial nuevo; no se edita ninguna migración aplicada (001–004 intactas).
- API: ninguna; `POST /turnos` no cambia. El uso del token es `C-29`.
- Dependencias: ninguna nueva. No introduce reglas de negocio nuevas en la aplicación, solo la invariante en la base.

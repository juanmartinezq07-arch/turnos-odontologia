# Tasks

## 1. Corrección RN05 same-day

- [x] 1.1 En `backend/app/application/bookings.py::reprogramar_turno`, modificar el precheck RN05 para excluir `turno_orig.id` de la consulta (o realizarlo antes de cancelar filtrando el propio turno), de modo que reprogramar al mismo día del mismo paciente no se rechace falsamente. Verificar que el código compila y el endpoint responde.

## 2. Verificación

- [x] 2.1 Levantar Postgres (docker compose up db o instancia local en 5433) y ejecutar `pytest tests/test_reprogramacion_api.py`; todos los tests deben pasar. (6 passed)
- [x] 2.2 Agregar/ajustar test de reprogramación al mismo día del mismo paciente y verificar que pasa (rollback no aplica, turno original cancelado, nuevo activo).

## Workflow follow-up

- Archivar el change tras verificar verde.
- Marcar C-23 como `[x]` en `CHANGES.md`.
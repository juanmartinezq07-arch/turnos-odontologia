# Proposal

## Why

Hoy la recepcionista y el paciente guest pueden consultar los catálogos públicos (`C-24`), pero no existe ningún mecanismo para descubrir qué horarios reales están disponibles para un profesional, una fecha y una prestación dada (`US-002` / `KB-07 §Flujo 1`). Sin `GET /disponibilidad`, el cliente debería adivinar horarios a ciegas hasta no chocar con RN02 o RN03, y el flujo `C-29 reservas-guest` permanece bloqueado.

## What Changes

- Implementar el cálculo determinista de slots disponibles como **función pura** en `backend/app/domain/rules.py` y su orquestación en `backend/app/application/availability.py` a partir de `(HorarioAtencion, turnos activos, duracion_min RN01, fecha, ahora inyectado)` sin depender de aleatoriedad ni reloj implícito en la lógica pura.
- Exponer el endpoint público `GET /disponibilidad?profesional_id=&fecha=&prestacion_id=` en `backend/app/api/v1/disponibilidad.py` (sin requerir `X-API-Key`, cubriendo otra de las rutas públicas de `KB-03`).
- Garantizar que cada slot devuelto `[inicio, fin)` tenga `fin = inicio + duracion_min` (RN01), quepa completo dentro de algún bloque de `HorarioAtencion` del día (RN03), no se encuentre en el pasado respecto a `now()` en `America/Argentina/Buenos_Aires` (RN03), y no se solape con turnos `activos` del profesional respetando la semántica semiabierta `[)` (el borde que se toca no pisa turnos activos, y los turnos `cancelados` no restan disponibilidad).
- Definir schemas Pydantic v2 estrictos (`extra="forbid"`) en `backend/app/schemas/disponibilidad.py` y registrar el router en `backend/app/main.py`.
- Agregar tests unitarios puros y de integración contra PostgreSQL 16 en `backend/tests/test_disponibilidad.py` verificando huecos libres, bloques que no entran completos al final del horario, semántica de borde `[)` e idempotencia/determinismo en consultas sucesivas.

## Capabilities

### New Capabilities

- `disponibilidad`: cálculo determinista y consulta pública de slots disponibles por profesional, fecha y prestación respetando RN01, RN02 (`[)`) y RN03.

### Modified Capabilities

- Ninguna.

## Impact

- Código nuevo: `backend/app/schemas/disponibilidad.py`, `backend/app/application/availability.py`, `backend/app/api/v1/disponibilidad.py`, `backend/tests/test_disponibilidad.py`.
- Código modificado: `backend/app/domain/rules.py` (función pura de cálculo de slots disponibles), `backend/app/main.py` (cableado del router `disponibilidad`).
- Base de datos / Migraciones: ninguna (opera sobre `horario_atencion`, `turno`, `profesional` y `prestacion` ya existentes).
- Dependencias desbloqueadas: junto con `C-21`, `C-26` y `C-24` (todos ya archivados), **destraba por completo `C-29 reservas-guest`**.

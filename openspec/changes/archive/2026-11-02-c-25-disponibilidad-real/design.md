# Design

## Context

`C-01` implementó `POST /turnos` con las validaciones puras `calcular_fin`, `esta_en_pasado` y `dentro_de_horario` en `backend/app/domain/rules.py`, y `C-24` expuso los catálogos públicos (`/profesionales`, `/sillones`, `/prestaciones`). Ahora `C-25` agrega el cómputo real de slots libres (`US-002`) para que tanto la recepcionista como el paciente guest puedan consultar horarios válidos antes de reservar. Ver `proposal.md` para la motivación.

## Goals / Non-Goals

**Goals:**

- Implementar el cálculo de slots disponibles como una función pura y 100% determinista de `(bloques_horario, intervalos_ocupados, fecha, duracion_min, ahora, tz)`, sin reloj implícito ni efectos secundarios.
- Exponer `GET /disponibilidad?profesional_id=&fecha=&prestacion_id=` como ruta pública (`KB-03`), validando existencia/actividad de profesional y prestación.
- Respetar estrictamente RN01 (`fin = inicio + duracion_min`), RN02 (`[)` sobre turnos `activos` y al menos un sillón libre en ese rango si todos los sillones activos estuvieran ocupados) y RN03 (`[inicio, fin)` cabe completo en `HorarioAtencion` y `inicio >= ahora`).

**Non-Goals:**

- Reservar o bloquear slots durante la consulta (la lectura no escribe ni toma locks; la carrera en el alta la resuelve el doble `EXCLUDE` en `POST /turnos` y `POST /reservas`).
- Paginación o consulta multi-día en un solo request (`GET /disponibilidad` recibe una `fecha: date` específica).

## Decisions

### D-01 — Algoritmo puro de generación de slots sobre bloques y cortes de turnos

Dentro de cada bloque `[hora_desde, hora_hasta)` de `HorarioAtencion` para `fecha.weekday()`:
1. Se construye el intervalo aware `[bloque_inicio, bloque_fin)` en `ZoneInfo(TZ_CONSULTORIO)`.
2. Para recorrer el bloque sin perder alineación tras turnos de distinta duración (ej. un turno existente de 45 min seguido de una consulta de 30 min), el cursor avanza desde el inicio del bloque en pasos de `duracion_min`; si un candidato `[cursor, cursor + duracion_min)` se solapa (`cursor < t_fin and cursor + duracion_min > t_inicio`) con algún intervalo ocupado `[t_inicio, t_fin)`, el cursor salta exactamente al mayor `t_fin` de los intervalos que lo pisan (semántica `[)`: el borde que se toca `cursor == t_fin` es válido) y vuelve a evaluar hasta que `cursor + duracion_min <= bloque_fin`.
3. Todo slot con `inicio < ahora` se descarta (o el cursor arranca y salta slots en el pasado manteniendo la grilla determinista del bloque).
4. La función pura vive en `backend/app/domain/rules.py` (`calcular_slots_disponibles`) y es invocada por `backend/app/application/availability.py` con `ahora: datetime | None = None` (inyectable para tests deterministas; si es `None`, el servicio inyecta `datetime.now(ZoneInfo(get_tz_consultorio()))`).

### D-02 — Consideración de turnos activos del profesional (y sillones)

Un intervalo está ocupado para el profesional en `fecha` si:
- El profesional ya tiene un turno `activo` que se solapa con `[inicio, fin)`, **o**
- Todos los sillones activos del consultorio están ocupados simultáneamente en ese rango (si hay al menos 1 sillón activo libre, el slot es reservable).
- Los turnos con `estado = 'cancelado'` se ignoran en la consulta (`Turno.estado == "activo"`).

### D-03 — Contrato HTTP y validación de recursos

- Ruta: `GET /disponibilidad?profesional_id=<uuid>&fecha=<YYYY-MM-DD>&prestacion_id=<uuid>` (público).
- Si `profesional_id` o `prestacion_id` no existen o están inactivos (`activo=False` / `activa=False`), lanza `NotFound` (`404` con `{code, message}` estable, consistente con `_cargar_recursos` en `bookings.py`).
- Si `fecha` tiene formato inválido o falta un query param obligatorio, FastAPI/Pydantic devuelve `422` con `{code: "VALIDACION", message: ...}` vía el handler global de `main.py`.
- Respuesta `200 OK`: lista de `SlotDisponibilidadOut(inicio: datetime, fin: datetime)` con `ConfigDict(extra="forbid")`.

## Risks / Trade-offs

- [Risk] Turnos de 45 min que desplazan los bordes respecto de una grilla fija de 30 min → Mitigación: cuando un candidato choca con un turno activo `[t_ini, t_fin)`, avanzar el cursor a `t_fin` permite aprovechar inmediatamente el borde `inicio_nuevo == fin_existente` (RN02 `[)`).

## Migration Plan

Sin migraciones de base de datos. Solo función pura en `domain/rules.py`, servicio en `application/availability.py`, schema en `schemas/disponibilidad.py`, router en `api/v1/disponibilidad.py` y tests en `tests/test_disponibilidad.py`.

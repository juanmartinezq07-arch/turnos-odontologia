# Modelo de Datos

## Dominios

- **Agenda:** Turno como hecho central con intervalo `[inicio, fin)`.
- **Recursos:** Profesional y Sillón/Box como recursos excluyentes (doble eje de RN02).
- **Catálogo:** Prestación con duración estimada (RN01) y Horario de atención (RN03).
- **Paciente liviano:** datos de contacto mínimos para guest booking, sin cuenta ni ficha clínica.

## ERD (textual)

```
Profesional 1───* Turno *───1 Sillon
Prestacion  1───* Turno
PacienteGuest 1───* Turno (un paciente puede tener varios turnos, pero máx. 1 activo por día — RN05)
HorarioAtencion *───1 Profesional (o global del consultorio en MVP)

Turno: [profesional_id, sillon_id, prestacion_id, paciente_id, inicio, fin, estado]
  EXCLUDE (profesional_id WITH =, rango WITH &&) WHERE (estado = 'activo')
  EXCLUDE (sillon_id WITH =, rango WITH &&)      WHERE (estado = 'activo')
```

Estados del turno: `activo` (reservado/confirmado se colapsan en uno para el MVP) y `cancelado`. La cancelación es cambio de estado, no borrado físico (RN04 + auditabilidad mínima).

## Entidades

### Profesional
- Atributos: `id (uuid/pk)`, `nombre (text)`, `apellido (text)`, `matricula (text, unique, nullable)`, `activo (bool)`.
- Relaciones: 1→* Turno; 1→* HorarioAtencion.
- Constraints: `matricula` única cuando está presente.
- Índices: `idx_profesional_activo`.

### Sillon (sillón/box)
- Atributos: `id`, `nombre (text, ej. "Sillón 1", "Box 2")`, `activo (bool)`.
- Relaciones: 1→* Turno.
- Constraints: nombre único entre activos.

### Prestacion
- Atributos: `id`, `nombre (text)`, `duracion_min (int, > 0)`, `activa (bool)`.
- Seed MVP: consulta 30′, obturación 45′, endodoncia 90′ (RN01).
- Relaciones: 1→* Turno.

### PacienteGuest
- Atributos: `id`, `nombre (text)`, `telefono (text)`, `email (text, nullable)`, `created_at (timestamptz)`.
- **Suposición explícita:** no hay DNI ni obra social ni dato clínico en esta tabla. Solo contacto para la reserva. Sin auth, sin password, sin ficha.
- Relaciones: 1→* Turno.
- Índices: `idx_paciente_telefono`, `idx_paciente_email` (búsqueda operativa, no unicidad).

### Turno (entidad central)
- Atributos: `id (uuid/pk)`, `profesional_id (fk)`, `sillon_id (fk)`, `prestacion_id (fk)`, `paciente_id (fk)`, `inicio (timestamptz)`, `fin (timestamptz, generado = inicio + duracion prestacion)`, `estado (enum: activo/cancelado)`, `token_cancelacion (text, unique, nullable — solo para reserva guest)`, `created_at`, `cancelled_at (nullable)`.
- Relaciones: *→1 con las cuatro anteriores.
- Constraints:
  - `CHECK (fin > inicio)`.
  - `CHECK (estado IN ('activo','cancelado'))`.
  - `EXCLUDE USING gist (profesional_id WITH =, tstzrange(inicio, fin) WITH &&) WHERE (estado = 'activo')` — mitad 1 de RN02.
  - `EXCLUDE USING gist (sillon_id WITH =, tstzrange(inicio, fin) WITH &&) WHERE (estado = 'activo')` — mitad 2 de RN02.
  - Requiere extensión `btree_gist` (los `WITH =` sobre uuid/int la necesitan).
  - Borde que se toca NO es conflicto: `tstzrange` por defecto es `[)` así que `fin == inicio_vecino` no se solapa — coincide con RN02.
  - RN05 (máx. 1 activo por paciente por día) como índice único parcial funcional sobre `(paciente_id, date(inicio)) WHERE estado='activo'` o validación + test; definir en el change (ver 10_preguntas_abiertas).
- Índices: `idx_turno_profesional_inicio`, `idx_turno_sillon_inicio`, `idx_turno_estado`, `idx_turno_paciente_fecha`.

### HorarioAtencion
- Atributos: `id`, `profesional_id (fk, nullable — null = global consultorio)`, `dia_semana (int 0-6)`, `hora_desde (time)`, `hora_hasta (time)`.
- Uso: RN03 (rechazar fuera de horario). Seed MVP: lunes a viernes 9–18, sábado 9–12 (ajustable).

## Seed data inicial

- 2–3 profesionales (para que el doble eje se pueda demostrar con 2 como mínimo).
- 2 sillones/boxes.
- 3 prestaciones (30/45/90 min).
- Horario de atención global + algún turno activo y uno cancelado de ejemplo (para mostrar que el cancelado libera el slot).
- Usuario/credencial fija de recepcionista y odontólogo para la demo (no en Git como secreto real).

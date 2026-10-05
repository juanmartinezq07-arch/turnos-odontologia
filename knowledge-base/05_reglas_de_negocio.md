# Reglas de Negocio

Códigos estables de Discovery (RN01–RN05). Son los que evalúa la cátedra y los que trazan a los tests. No se renombran.

## Dominio: Prestaciones (RN01)

- **RN01 — Duración por prestación**: cada prestación define su duración estimada en minutos y determina el bloque requerido en agenda. Seed: consulta 30′, obturación 45′, endodoncia 90′. El `fin` del turno se calcula como `inicio + duracion_prestacion`; el cliente no manda `fin` arbitrario.

## Dominio: Agenda / solapamiento (RN02 — invariante central)

- **RN02 — Doble validación de solapamiento**: un turno en estado `activo` no puede solaparse con otro turno `activo` del **mismo profesional** ni del **mismo sillón/box** dentro de su intervalo.
- Criterio: hay solapamiento si `inicio_nuevo < fin_existente AND fin_nuevo > inicio_existente`. Dos turnos que se tocan en el borde (`inicio_nuevo == fin_existente`) **no** se solapan.
- Implementación obligatoria en persistencia:
  - `EXCLUDE USING gist (profesional_id WITH =, tstzrange(inicio, fin) WITH &&) WHERE (estado = 'activo')`
  - `EXCLUDE USING gist (sillon_id WITH =, tstzrange(inicio, fin) WITH &&) WHERE (estado = 'activo')`
- La capa de aplicación valida primero para devolver 409 con mensaje claro, pero **la base decide**: si dos requests concurrentes pasan la validación, una sola hace commit.
- Los turnos `cancelados` no participan del constraint (por eso el `WHERE`), lo que implementa RN04 a nivel de invariante.

## Dominio: Temporalidad (RN03)

- **RN03 — Validación temporal**: no se agenda ni se reserva en el pasado ni fuera del horario de atención configurado. El pasado se evalúa contra `now()` en zona horaria del consultorio (América/Argentina/Buenos_Aires); el horario contra `HorarioAtencion`.

## Dominio: Cancelación (RN04)

- **RN04 — Política de cancelación**: cancelar registra estado `cancelado` + `cancelled_at = now()` y **libera inmediatamente** el slot en ambas agendas (profesional y sillón). No es borrado físico. Reprogramar = cancelar + crear en una transacción; si el nuevo slot choca, todo hace rollback.

## Dominio: Paciente (RN05)

- **RN05 — Límite por paciente**: un mismo paciente (identificado por teléfono o email normalizado en guest booking) no puede tener más de un turno `activo` en el mismo día calendario. Se responde 409. Detalle de implementación (índice único parcial vs. validación + test de carrera) lo cierra el change.

## Dominio: Excepciones globales

- Los errores de invariante de DB (violación de `EXCLUDE`) se traducen siempre a `409 Conflict` con código de regla (`RN02_PROFESIONAL` / `RN02_SILLON` / `RN05`), nunca a 500.
- Toda escritura de turno dispara `NotificationService.notificar(...)` de forma best-effort: si el mock falla, el turno igual persiste (la notificación no bloquea la agenda).
- Sin ficha clínica en el MVP: ningún endpoint acepta ni persiste datos clínicos. Si llega un campo clínico, se rechaza con 422. Esto sostiene la mitigación legal de R3 (Ley 25.326 Art. 5.1/8/12.1).

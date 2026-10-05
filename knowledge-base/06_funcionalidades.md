# Funcionalidades

Organizadas por épica. Alcance del change: CU01 + CU02 encadenadas con RN01–RN05 como núcleo. CU03/CU04 quedan en alcance mínimo operable (sin panel ni extras).

## Épica A: Agenda sin solapamientos (CU01)

### US-001 — Alta de turno por recepcionista
**Como** recepcionista **Quiero** crear un turno indicando profesional, sillón/box, prestación y datos mínimos del paciente **Para** reservar la atención sin solapar horarios.

**Criterios de aceptación**:
- [ ] Acepta `profesional_id`, `sillon_id`, `prestacion_id`, `inicio`, datos paciente guest; calcula `fin` por RN01.
- [ ] Rechaza con 409 si viola RN02 (profesional o sillón), indicando cuál de los dos chocó.
- [ ] Rechaza con 422 si es pasado o fuera de horario (RN03).
- [ ] Rechaza con 409 si el paciente ya tiene un activo ese día (RN05).
- [ ] Dispara notificación via mock sin bloquear la persistencia.

**Reglas relacionadas**: RN01, RN02, RN03, RN05

### US-002 — Consulta de disponibilidad real
**Como** recepcionista (y paciente) **Quiero** ver slots libres por profesional/fecha/prestación **Para** elegir un horario que realmente existe.

**Criterios de aceptación**:
- [ ] `GET /disponibilidad` computa huecos desde turnos activos menos horario de atención.
- [ ] Los slots respetan la duración de la prestación (RN01) y no ofrecen pasado (RN03).
- [ ] Dos consultas seguidas sin altas intermedias devuelven lo mismo (determinismo).

**Reglas relacionadas**: RN01, RN02, RN03

## Épica B: Reserva online guest (CU02)

### US-003 — Reserva pública sin autenticación
**Como** paciente **Quiero** reservar un turno desde un enlace público eligiendo profesional y horario **Para** coordinar mi atención sin llamar.

**Criterios de aceptación**:
- [ ] `POST /reservas` no pide auth; pide datos mínimos + `profesional_id`, `sillon_id` (o auto-asignación si el change lo define), `prestacion_id`, `inicio`.
- [ ] Mismas validaciones que US-001 (RN01–RN05).
- [ ] Devuelve token de cancelación guest.
- [ ] Dos `POST /reservas` concurrentes al mismo slot → una gana (201), la otra pierde (409). Test de concurrencia real obligatorio.

**Reglas relacionadas**: RN01, RN02, RN03, RN05

## Épica C: Cancelación y reprogramación (CU03 — mínima)

### US-004 — Cancelación con liberación inmediata
**Como** recepcionista **Quiero** cancelar un turno **Para** liberar el slot del profesional y del sillón.

**Criterios de aceptación**:
- [ ] Cambia a `cancelado` + `cancelled_at`; el slot vuelve a aparecer en disponibilidad.
- [ ] El paciente guest puede cancelar el suyo con token; sin token no puede tocar turnos ajenos.
- [ ] La cancelación dispara notificación mock.

**Reglas relacionadas**: RN04, RN02 (el liberado deja de contar en el EXCLUDE)

### US-005 — Reprogramación atómica
**Como** recepcionista **Quiero** mover un turno a otro horario **Para** reasignarlo sin perderlo.

**Criterios de aceptación**:
- [ ] Operación transaccional: si el destino choca (RN02), el turno original queda intacto.
- [ ] Valida RN03 y RN05 sobre el nuevo slot.

**Reglas relacionadas**: RN02, RN03, RN04, RN05

## Épica D: Agenda del odontólogo (CU04 — lectura)

### US-006 — Ver agenda del día
**Como** odontólogo/a **Quiero** ver mis turnos del día con prestaciones asignadas **Para** organizar mi jornada.

**Criterios de aceptación**:
- [ ] `GET /agenda?profesional_id=&fecha=` lista turnos activos ordenados por `inicio` con prestación, sillón y paciente.
- [ ] Solo ve su propia agenda (autorización mínima por rol).
- [ ] No muestra turnos cancelados salvo filtro explícito.

**Reglas relacionadas**: RN01 (duración visible), RN04 (cancelados fuera por defecto)

# Spec Delta

## Purpose

Provee la consulta autenticada de la agenda diaria por profesional y fecha (`GET /agenda`) ordenada por horario de inicio con detalle de prestación (y su duración según RN01), sillón y paciente, restringiendo al odontólogo a su propia agenda (`403` en agenda ajena) y excluyendo turnos cancelados salvo filtro explícito (`?incluir_cancelados=true`).

## ADDED Requirements

### Requirement: Consulta de agenda diaria ordenada con detalle completo (US-006, RN01, RN04)

El sistema SHALL exponer `GET /agenda?profesional_id=&fecha=` devolviendo los turnos del profesional en esa fecha (evaluada en `America/Argentina/Buenos_Aires`) ordenados ascendentemente por `inicio`, incluyendo para cada turno los datos de la prestación (`id`, `nombre`, `duracion_min`), del sillón (`id`, `nombre`) y el contacto mínimo del paciente (`id`, `nombre`, `telefono`, `email`).

#### Scenario: Turnos activos del día devueltos en orden cronológico con duración visible

- **WHEN** un odontólogo autenticado consulta su propia agenda para una `fecha` donde tiene turnos activos a las 11:00 y a las 09:30
- **THEN** el sistema responde 200 OK con la lista ordenada `[09:30, 11:00]` incluyendo `prestacion.duracion_min`, `sillon` y `paciente`

#### Scenario: Fecha con formato inválido es rechazada con 422

- **WHEN** se invoca `GET /agenda` con un parámetro `fecha` que no es una fecha ISO válida (ej. `fecha=no-es-fecha`)
- **THEN** el sistema responde 422 Unprocessable Entity con `{code, message}`

### Requirement: Exclusión por defecto y filtro explícito de turnos cancelados (US-006, RN04)

El sistema SHALL excluir los turnos con `estado = 'cancelado'` cuando se consulta `GET /agenda` sin el parámetro `incluir_cancelados` o con `incluir_cancelados=false`, y SHALL incluirlos cuando se indica explícitamente `?incluir_cancelados=true`.

#### Scenario: Turnos cancelados no aparecen por defecto

- **WHEN** el profesional tiene un turno `activo` a las 10:00 y un turno `cancelado` a las 11:00 en la misma fecha y consulta `GET /agenda` sin `incluir_cancelados`
- **THEN** la respuesta contiene únicamente el turno `activo` de las 10:00

#### Scenario: Filtro explícito incluye turnos cancelados

- **WHEN** el profesional consulta `GET /agenda?profesional_id=&fecha=&incluir_cancelados=true`
- **THEN** la respuesta incluye tanto el turno `activo` de las 10:00 como el turno `cancelado` de las 11:00 ordenados por `inicio`

### Requirement: Autenticación y autorización por rol sobre la agenda (KB-03 RBAC)

El sistema SHALL exigir una credencial válida en `X-API-Key` (`API_KEY_ODONTOLOGO` o `API_KEY_RECEPCION`) para `GET /agenda`, respondiendo `401` si falta o es inválida, y cuando se autentica con `API_KEY_ODONTOLOGO` SHALL verificar que el header `X-Profesional-Id` coincida con el `profesional_id` consultado, respondiendo `403` si intenta consultar la agenda de otro profesional.

#### Scenario: Petición sin credencial o con API key inválida recibe 401

- **WHEN** un cliente invoca `GET /agenda` sin `X-API-Key` o con un valor inválido
- **THEN** el sistema responde 401 Unauthorized con `{code, message}`

#### Scenario: Odontólogo que pide agenda ajena recibe 403

- **WHEN** un odontólogo autenticado con `API_KEY_ODONTOLOGO` y `X-Profesional-Id` correspondiente al profesional A invoca `GET /agenda?profesional_id=<id_profesional_B>&fecha=...`
- **THEN** el sistema responde 403 Forbidden con `code = "AGENDA_AJENA"`

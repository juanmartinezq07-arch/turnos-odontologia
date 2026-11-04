# Spec Delta

## Purpose

Permite a la recepcionista crear turnos sin solapamientos por profesional ni por sillón, con el cálculo de fin en el servidor.

## Requirements

### Requirement: Alta de turno calcula fin en el servidor (RN01)

El sistema SHALL calcular `fin = inicio + duracion_min` de la prestación y SHALL rechazar con 422 cualquier request que incluya el campo `fin` o campos no declarados (`extra='forbid'`).

#### Scenario: Alta correcta calcula fin

- **WHEN** la recepcionista envía `POST /turnos` con `profesional_id`, `sillon_id`, `prestacion_id` (30 min), `inicio` válido y datos mínimos del paciente
- **THEN** el sistema responde 201 con el turno creado cuyo `fin` es exactamente `inicio + 30 min`

#### Scenario: Cliente que envía fin es rechazado

- **WHEN** el request incluye el campo `fin`
- **THEN** el sistema responde 422 con `{code, message}` y no persiste nada

### Requirement: Alta rechaza solapamiento indicando el eje (RN02)

El sistema SHALL rechazar con 409 y código `RN02_PROFESIONAL` o `RN02_SILLON` todo turno activo que se solape con otro activo del mismo profesional o del mismo sillón. El borde que se toca (`inicio_nuevo == fin_existente`) SHALL NOT considerarse solapamiento (semántica `[)`).

#### Scenario: Choque por profesional

- **WHEN** existe un turno activo del profesional P de 10:00 a 10:30 y se pide otro para P de 10:15 a 10:45
- **THEN** el sistema responde 409 con `code = RN02_PROFESIONAL`

#### Scenario: Choque por sillón con distinto profesional

- **WHEN** existe un turno activo en el sillón S de 10:00 a 10:30 y se pide otro en S de 10:15 a 10:45 con otro profesional
- **THEN** el sistema responde 409 con `code = RN02_SILLON`

#### Scenario: Borde que se toca no choca

- **WHEN** existe un turno activo de 10:00 a 10:30 y se pide otro de 10:30 a 11:00 con mismo profesional y sillón
- **THEN** el sistema responde 201

#### Scenario: Concurrencia real al mismo slot

- **WHEN** dos `POST /turnos` concurrentes piden el mismo slot activo del mismo profesional y sillón
- **THEN** uno responde 201 y el otro responde 409 (con `RN02_PROFESIONAL` o `RN02_SILLON`)

### Requirement: Alta valida temporalidad y horario (RN03)

El sistema SHALL rechazar con 422 todo turno con `inicio` en el pasado (contra `now()` en `America/Argentina/Buenos_Aires`) o fuera de `HorarioAtencion`.

#### Scenario: Turno en el pasado

- **WHEN** se pide un turno con `inicio` anterior a `now()` del consultorio
- **THEN** el sistema responde 422 y no persiste nada

#### Scenario: Turno fuera de horario

- **WHEN** se pide un turno fuera del horario configurado (ej. domingo sin atención)
- **THEN** el sistema responde 422

### Requirement: Alta rechaza más de un turno activo por paciente y día (RN05)

El sistema SHALL rechazar con 409 y `code = RN05` toda solicitud de turno para un paciente (identificado por teléfono normalizado con fallback a email normalizado según SU-03) que ya posea un turno `activo` en el mismo día calendario del consultorio (`America/Argentina/Buenos_Aires`), tanto en validación previa de aplicación como ante violación del índice `rn05_un_activo_por_dia`.

#### Scenario: Mismo paciente mismo día recibe 409 RN05

- **WHEN** existe un turno `activo` para el paciente con teléfono `11-0000-0001` el día D a las 10:00 y se solicita otro turno `activo` para el mismo teléfono el día D a las 10:45
- **THEN** el sistema responde 409 con `code = RN05` y no persiste el segundo turno

#### Scenario: Distinto paciente mismo día recibe 201

- **WHEN** existe un turno `activo` para `11-0000-0001` el día D a las 10:00 y se solicita otro turno en un horario libre del día D para `11-0000-0002`
- **THEN** el sistema responde 201 y persiste el turno

#### Scenario: Mismo paciente en día distinto recibe 201

- **WHEN** existe un turno `activo` para `11-0000-0001` el día D1 y se solicita otro turno `activo` para `11-0000-0001` en otro día hábil D2
- **THEN** el sistema responde 201 y persiste el turno

### Requirement: Cancelación de turno por recepcionista libera el slot (RN04)

El sistema SHALL permitir a la recepcionista autenticada (`X-API-Key`) cancelar un turno mediante `POST /turnos/{id}/cancelacion`, actualizando `estado = 'cancelado'` y `cancelled_at = now()`, liberando el intervalo en los predicados parciales `WHERE (estado = 'activo')` de profesional, sillón y paciente, y disparando notificación *best-effort*.

#### Scenario: Cancelación exitosa cambia estado y libera el slot

- **WHEN** la recepcionista envía `POST /turnos/{id}/cancelacion` con `X-API-Key` válida para un turno `activo`
- **THEN** el sistema responde 200 con `estado = 'cancelado'` y `cancelled_at` no nulo, registra el evento en el servicio de notificaciones mock, y permite crear un nuevo turno `activo` en el mismo horario, profesional, sillón y paciente sin conflicto RN02 ni RN05

### Requirement: Idempotencia en cancelación repetida (RN04)

El sistema SHALL procesar de forma idempotente toda llamada repetida a `POST /turnos/{id}/cancelacion` sobre un turno que ya se encuentra en `estado = 'cancelado'`, respondiendo 200 sin alterar el instante `cancelled_at` registrado en la primera cancelación.

#### Scenario: Segunda cancelación conserva el timestamp original

- **WHEN** la recepcionista envía `POST /turnos/{id}/cancelacion` sobre un turno cuyo `estado` ya es `'cancelado'` con `cancelled_at = T1`
- **THEN** el sistema responde 200 con `estado = 'cancelado'` y `cancelled_at == T1` intacto

### Requirement: Rechazo de cancelación por turno inexistente o falta de credencial

El sistema SHALL responder 404 con `{code: "NO_ENCONTRADO", message}` cuando el `id` del turno no exista en la base de datos y 401 cuando falte o sea inválida la cabecera `X-API-Key`.

#### Scenario: Turno inexistente devuelve 404 NO_ENCONTRADO

- **WHEN** la recepcionista autenticada envía `POST /turnos/{id}/cancelacion` con un UUID que no corresponde a ningún turno persistido
- **THEN** el sistema responde 404 con cuerpo JSON `{"code": "NO_ENCONTRADO", "message": "..."}`

#### Scenario: Solicitud sin credencial de recepcionista devuelve 401

- **WHEN** se invoca `POST /turnos/{id}/cancelacion` sin la cabecera `X-API-Key` o con una clave inválida
- **THEN** el sistema responde 401 y no modifica el estado de ningún turno

### Requirement: Reprogramación atómica de turno en transacción única (US-005, RN04)

El sistema SHALL permitir a la recepcionista autenticada (`X-API-Key`) reprogramar un turno activo existente mediante `POST /turnos/{id}/reprogramacion` enviando el nuevo `inicio` (y opcionalmente nuevo `sillon_id`), cancelando el turno original y creando el nuevo en una única transacción de base de datos.

#### Scenario: Reprogramación exitosa cancela original y crea nuevo turno

- **WHEN** la recepcionista solicita `POST /turnos/{id}/reprogramacion` con nuevo `inicio` en horario disponible
- **THEN** el sistema responde 200 con los datos del nuevo turno `activo`, el turno original pasa a `estado = 'cancelado'` con `cancelled_at` registrado, y se emiten los eventos de notificación correspondientes

### Requirement: Rollback atómico ante conflicto en el destino

Si el nuevo horario o sillón solicitado viola las reglas de solapamiento (`RN02`), límite de paciente por día (`RN05`) o validación temporal (`RN03`), el sistema SHALL responder con el código de error correspondiente (`409` o `422`) y revertir completamente la transacción, garantizando que el turno original permanezca en estado `activo` con `cancelled_at = NULL`.

#### Scenario: Choque de horario en destino deja turno original activo (Rollback total)

- **WHEN** se intenta reprogramar un turno activo T1 hacia un horario ya ocupado por el mismo profesional (o sillón)
- **THEN** el sistema responde 409 con el código de conflicto (`RN02_PROFESIONAL` o `RN02_SILLON`) y en la base de datos el turno T1 permanece en `estado = 'activo'` con `cancelled_at = NULL`

#### Scenario: Destino en el pasado rechaza sin alterar turno original

- **WHEN** se intenta reprogramar un turno activo T1 hacia una fecha/hora en el pasado
- **THEN** el sistema responde 422 con `code = RN03_PASADO` y el turno T1 permanece `activo` e intacto

### Requirement: Validación de turno origen para reprogramación

El sistema SHALL responder 404 con `{code: "NO_ENCONTRADO", message}` si el turno origen no existe, 409 con `{code: "TURNO_NO_ACTIVO", message}` si el turno origen ya se encuentra cancelado, y 401 si falta la cabecera `X-API-Key`.

#### Scenario: Reprogramar turno inexistente devuelve 404

- **WHEN** se envía `POST /turnos/{id}/reprogramacion` con un ID que no existe
- **THEN** el sistema responde 404 con `code = NO_ENCONTRADO`

#### Scenario: Reprogramar turno ya cancelado devuelve 409

- **WHEN** se intenta reprogramar un turno cuyo estado es `cancelado`
- **THEN** el sistema responde 409 con `code = TURNO_NO_ACTIVO`

### Requirement: Alta de reserva pública guest (US-003, RN01, RN02)

El sistema SHALL exponer `POST /reservas` como endpoint público sin requerir cabeceras de autenticación. Debe aceptar datos de contacto, profesional, prestación, horario de inicio y opcionalmente sillón. Si el sillón no se especifica, el sistema SHALL auto-asignar el primer sillón disponible para el intervalo. El sistema SHALL generar y persistir un `token_cancelacion` único, retornando `201 Created` con el turno y su token.

#### Scenario: Reserva exitosa auto-asigna sillón y emite token_cancelacion

- **WHEN** un paciente guest solicita `POST /reservas` con un slot disponible sin enviar `sillon_id`
- **THEN** el sistema responde `201 Created` con el turno asignado a un sillón disponible, `estado = 'activo'`, y un `token_cancelacion` no nulo ni vacío

#### Scenario: Concurrencia real en reservas guest al último slot disponible

- **WHEN** dos solicitudes `POST /reservas` concurrentes compiten por el único sillón y slot disponible para un profesional
- **THEN** exactamente una solicitud responde `201 Created` y la otra responde `409` (`RN02_SILLON` o `RN02_PROFESIONAL`), garantizado por la exclusión atómica de PostgreSQL

### Requirement: Cancelación de reserva pública mediante token (US-004, RN04)

El sistema SHALL exponer `POST /reservas/{token}/cancelacion` como endpoint público. Si el token existe y corresponde a un turno, el sistema SHALL pasar su estado a `'cancelado'`, registrar `cancelled_at = now()`, emitir notificación *best-effort* y liberar el slot. Si el turno ya estaba cancelado, la operación SHALL ser idempotente respondiendo `200 OK` con el `cancelled_at` original. Si el token no existe, SHALL responder `404` con `code = "NO_ENCONTRADO"`.

#### Scenario: Cancelación por token libera el slot y es idempotente

- **WHEN** el paciente envía `POST /reservas/{token}/cancelacion` con un token válido de un turno activo
- **THEN** el sistema responde `200 OK` con `estado = 'cancelado'`, `cancelled_at` registrado, libera el slot para nuevas reservas y llamadas posteriores con el mismo token responden `200 OK` conservando el mismo timestamp

#### Scenario: Cancelación con token inexistente devuelve 404

- **WHEN** se invoca `POST /reservas/{token}/cancelacion` con un token que no existe en el sistema
- **THEN** el sistema responde `404` con `{"code": "NO_ENCONTRADO", "message": "..."}`

### Requirement: Protección ante abuso y rechazo de datos clínicos (Ley 25.326)

El sistema SHALL rechazar con `422` cualquier intento de inyección de campos no permitidos (`extra="forbid"`), garantizando la protección de datos personales. Asimismo, el sistema SHALL limitar las solicitudes a `POST /reservas` a un máximo configurable (10 solicitudes por minuto), respondiendo `429` ante exceso de peticiones.

#### Scenario: Intento de reserva con campos clínicos adicionales es rechazado con 422

- **WHEN** una petición `POST /reservas` incluye un campo no admitido como `obra_social` o `diagnostico`
- **THEN** el sistema responde `422` y no persiste el paciente ni el turno

#### Scenario: Exceso de solicitudes dispara rate limit 429

- **WHEN** un cliente supera el límite de 10 reservas por minuto
- **THEN** el sistema responde `429` con `{"code": "RATE_LIMIT_EXCEEDED", "message": "..."}`



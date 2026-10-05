# Spec Delta

## Purpose

Permite que un paciente sin cuenta reserve y cancele su propio turno desde un enlace público, con las mismas garantías anti-solapamiento que el alta de recepcionista.

## ADDED Requirements

### Requirement: Reserva pública sin auth con validaciones completas

El sistema SHALL exponer `POST /reservas` sin autenticación y SHALL aplicarle las mismas validaciones que a `POST /turnos` (RN01, RN02, RN03, RN05). El cliente SHALL enviar `inicio` y SHALL NOT enviar `fin`.

#### Scenario: Reserva guest correcta

- **WHEN** un paciente envía nombre, teléfono, `profesional_id`, `prestacion_id` e `inicio` válido
- **THEN** el sistema responde 201 con el turno y un `token_cancelacion` opaco

#### Scenario: Reserva guest que choca

- **WHEN** el slot ya está ocupado por un turno activo del mismo profesional o sillón
- **THEN** el sistema responde 409 con `RN02_PROFESIONAL` o `RN02_SILLON`

### Requirement: Concurrencia guest con un solo ganador

El sistema SHALL garantizar que dos `POST /reservas` concurrentes al mismo slot producen exactamente una respuesta 201 y una 409, decidiendo la base de datos.

#### Scenario: Doble POST concurrente

- **WHEN** dos requests concurrentes piden el mismo slot libre
- **THEN** una responde 201 y la otra 409, y solo un turno activo queda persistido

### Requirement: Sillón opcional con auto-asignación

El sistema SHALL aceptar `sillon_id` opcional en `POST /reservas`; si falta, SHALL asignar en la misma transacción el primer sillón libre para ese rango, y si ninguno está libre SHALL responder 409 con `RN02_SILLON`.

#### Scenario: Reserva sin sillón asigna el primero libre

- **WHEN** se reserva sin `sillon_id` y el sillón 1 está ocupado pero el 2 está libre
- **THEN** el sistema responde 201 con el turno asignado al sillón 2

### Requirement: Cancelación guest solo con token propio

El sistema SHALL exponer `POST /reservas/{token}/cancelacion` sin auth, que SHALL cancelar únicamente el turno asociado a ese token y SHALL rechazar tokens inexistentes o ya usados.

#### Scenario: Cancelación propia correcta

- **WHEN** el paciente envía su `token_cancelacion` válido de un turno activo
- **THEN** el sistema responde 200 y el turno pasa a `cancelado`

#### Scenario: Token ajeno o inválido no cancela nada

- **WHEN** se envía un token inexistente o de otro turno
- **THEN** el sistema responde 404 o 403 sin modificar turnos

### Requirement: Rate-limit del endpoint público

El sistema SHALL limitar `POST /reservas` a 10 requests por minuto por cliente (ventana en memoria, configurable por `RESERVA_RATE_LIMIT`) y SHALL responder 429 al excederlo.

#### Scenario: Abuso del endpoint público

- **WHEN** un cliente supera 10 `POST /reservas` en un minuto
- **THEN** el sistema responde 429 hasta que vence la ventana

### Requirement: Rechazo de datos clínicos y límite RN05 guest

El sistema SHALL rechazar con 422 cualquier payload de reserva con campos clínicos o sensibles no declarados, y SHALL aplicar RN05 (un activo por día) también al guest con 409 `RN05`.

#### Scenario: Payload con campo clínico

- **WHEN** `POST /reservas` incluye un campo clínico (ej. `diagnostico`)
- **THEN** el sistema responde 422 y no persiste nada

#### Scenario: Guest con dos activos el mismo día

- **WHEN** el mismo teléfono ya tiene un activo hoy y reserva otro hoy
- **THEN** el sistema responde 409 con `code = RN05`

# Spec Delta

## Purpose

Agregar la pantalla de cancelación y reprogramación.

## ADDED Requirements

### Requirement: Pantalla de cancelación de turno

La interfaz SHALL permitir cancelar un turno activo vía `POST /turnos/{id}/cancelacion` y mostrar el estado `cancelado` con `cancelled_at`.

#### Scenario: Cancelación exitosa

- **WHEN** la recepcionista cancela un turno activo
- **THEN** la UI muestra el turno como `cancelado` con `cancelled_at`

#### Scenario: Idempotencia

- **WHEN** se cancela un turno ya cancelado
- **THEN** la UI muestra el mismo `cancelled_at` sin error

### Requirement: Pantalla de reprogramación de turno

La interfaz SHALL permitir reprogramar un turno activo vía `POST /turnos/{id}/reprogramacion` enviando el nuevo `inicio` (y opcionalmente `sillon_id`), mostrando original (cancelado) y nuevo (activo).

#### Scenario: Reprogramación exitosa

- **WHEN** el destino está libre
- **THEN** la UI muestra el original cancelado y el nuevo activo

#### Scenario: Fallo con rollback

- **WHEN** el destino viola RN02/RN03/RN05
- **THEN** la UI muestra el error y deja claro que el original sigue activo
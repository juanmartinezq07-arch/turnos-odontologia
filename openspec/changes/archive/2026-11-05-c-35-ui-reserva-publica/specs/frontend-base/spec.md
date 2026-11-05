# Spec Delta

## Purpose

Agregar el flujo de reserva pública guest.

## ADDED Requirements

### Requirement: Flujo de reserva pública guest

La interfaz SHALL ofrecer un flujo sin autenticación: catálogos → disponibilidad → `POST /reservas` → mostrar y guardar el `token_cancelacion` → cancelación con token.

#### Scenario: Reserva exitosa

- **WHEN** el guest completa el flujo con datos válidos
- **THEN** se crea la reserva (201) y se muestra el token de cancelación

#### Scenario: Cancelación con token

- **WHEN** el guest cancela con su token
- **THEN** la reserva se cancela y el slot se libera

#### Scenario: Conflicto (409)

- **WHEN** el slot ya está ocupado
- **THEN** la UI muestra el error por código (RN02_*, RN05)
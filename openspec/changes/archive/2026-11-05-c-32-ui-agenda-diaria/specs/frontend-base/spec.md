# Spec Delta

## Purpose

Agregar la pantalla de agenda diaria a la interfaz base.

## MODIFIED Requirements

### Requirement: Navegación entre pantallas sin recarga completa

El sistema SHALL permitir navegar entre las pantallas de la interfaz sin recargar la página completa, incluyendo la pantalla de agenda diaria.

#### Scenario: Cambio de pantalla

- **WHEN** el usuario navega a otra sección
- **THEN** solo el contenido principal se actualiza, sin recarga del documento completo

## ADDED Requirements

### Requirement: Pantalla de agenda diaria

La interfaz SHALL ofrecer una pantalla que consulte `GET /agenda?profesional_id=&fecha=` con credencial de recepcionista u odontólogo y muestre los turnos ordenados por `inicio`, incluyendo prestación (y duración), sillón y paciente, con opción de incluir cancelados.

#### Scenario: Agenda cargada

- **WHEN** el usuario ingresa profesional y fecha válidos con credencial válida
- **THEN** se listan los turnos ordenados por inicio con prestación, sillón y paciente

#### Scenario: Agenda ajena (403)

- **WHEN** un odontólogo consulta la agenda de otro profesional
- **THEN** la UI muestra un mensaje de acceso denegado (código `AGENDA_AJENA`)

#### Scenario: Sin credencial (401)

- **WHEN** se consulta la agenda sin credencial válida
- **THEN** la UI solicita el ingreso de la API key
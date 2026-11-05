# Spec Delta

## Purpose

Agregar la pantalla de alta de turno con manejo de errores por código.

## ADDED Requirements

### Requirement: Pantalla de alta de turno

La interfaz SHALL ofrecer una pantalla que, usando catálogos públicos y `GET /disponibilidad`, permita a la recepcionista crear un turno vía `POST /turnos` enviando solo `inicio` (sin `fin`), con datos mínimos del paciente, y mostrar el resultado o el error por código.

#### Scenario: Alta exitosa

- **WHEN** la recepcionista completa el formulario válido y hay slot disponible
- **THEN** se crea el turno (201) y se muestra confirmación con `fin` calculado

#### Scenario: Conflicto de agenda (409)

- **WHEN** el slot choca con otro turno (profesional/sillón/RN05)
- **THEN** la UI muestra un mensaje específico según el código (`RN02_PROFESIONAL`, `RN02_SILLON`, `RN05`)

#### Scenario: Validación (422)

- **WHEN** el inicio está en el pasado o fuera de horario o faltan campos
- **THEN** la UI muestra el error de validación sin crear el turno

#### Scenario: Sin credencial (401)

- **WHEN** se intenta crear un turno sin credencial de recepción
- **THEN** la UI solicita el ingreso de la API key
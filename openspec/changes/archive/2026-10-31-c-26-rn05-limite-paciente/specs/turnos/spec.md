# Spec Delta

## ADDED Requirements

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

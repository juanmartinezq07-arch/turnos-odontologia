# Spec Delta

## Purpose

Da al odontólogo la vista ordenada de sus propios turnos del día, ocultando cancelados por defecto y bloqueando el acceso a agendas ajenas.

## ADDED Requirements

### Requirement: Agenda propia ordenada con detalle

El sistema SHALL exponer `GET /agenda?profesional_id=&fecha=` que devuelve los turnos activos de ese profesional y día ordenados por `inicio`, con prestación (y duración), sillón y paciente.

#### Scenario: Agenda del día ordenada

- **WHEN** el odontólogo pide su agenda de hoy con tres activos (09:00, 10:00, 11:00)
- **THEN** el sistema responde 200 con los tres turnos en ese orden y con prestación, sillón y paciente informados

### Requirement: Autorización por agenda propia

El sistema SHALL permitir a cada odontólogo leer solo su propia agenda y SHALL responder 403 ante agenda ajena.

#### Scenario: Agenda ajena bloqueada

- **WHEN** el odontólogo A pide la agenda del profesional B
- **THEN** el sistema responde 403 sin devolver turnos

### Requirement: Cancelados ocultos por defecto

El sistema SHALL excluir los turnos `cancelados` salvo que el request incluya `?incluir_cancelados=true`.

#### Scenario: Cancelados filtrados y visibles bajo pedido

- **WHEN** se pide la agenda sin el filtro teniendo un activo y un cancelado
- **THEN** solo aparece el activo; con `?incluir_cancelados=true` aparecen ambos

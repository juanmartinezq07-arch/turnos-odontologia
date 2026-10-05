# Visión y Objetivos

## Propósito del sistema

**TurnosAR es un turnero odontológico para consultorios chicos de Argentina que convierte la noción de conflicto de agenda en un invariante del sistema.**

En los consultorios la agenda se lleva en cuadernos o planillas y la coordinación con pacientes por WhatsApp informal. Eso produce solapamientos entre profesionales y entre sillones, ausentismo por falta de confirmación y tiempo administrativo que compite con la atención clínica. TurnosAR ataca el primer daño: ningún turno puede existir si se solapa con otro del mismo profesional o del mismo sillón/box, y esa garantía vive en la base de datos, no en un chequeo best-effort de la interfaz.

## Objetivos por actor

| Actor | Objetivo principal | Objetivos secundarios |
|-------|--------------------|----------------------|
| Recepcionista / Asistente | Agendar sin solapar, asignando profesional + sillón/box + prestación en una sola operación | Cancelar y reprogramar liberando el slot al instante; manejar sobreturnos simples |
| Odontólogo/a | Ver su agenda del día/semana con prestaciones asignadas para organizar la jornada | Evitar choques de sillón que lo dejan sin box aunque su agenda parezca libre |
| Paciente | Reservar online 24/7 sobre disponibilidad real sin llamar por teléfono | Recibir confirmación y recordatorio; cancelar cuando lo necesita |

## Alcance v1.0 (MVP)

- CU01: alta de turno por recepcionista con profesional + sillón/box + prestación.
- CU02: consulta de disponibilidad real y reserva guest por enlace público, sin autenticación del paciente.
- Validación transaccional de RN01 a RN05 como núcleo del change.
- RN02 como constraint de exclusión en PostgreSQL (doble: por profesional y por sillón).
- CU03 y CU04 documentadas y modeladas (cancelación/reprogramación, agenda del odontólogo) como operaciones mínimas necesarias para que el MVP sea operable.
- Interfaz `NotificationService` con implementación mock (confirmación registrada, no enviada).
- API REST pura sin frontend propio; la demo se ejerce con pytest + httpx y/o Swagger UI.
- Un solo change OpenSpec, chico y demostrable.

## Fuera de alcance

- Ficha clínica y odontograma interactivo (decisión deliberada, reduce riesgo Ley 25.326).
- Confirmación y recordatorio real por WhatsApp Business API o email transaccional.
- Cobro de señas con Mercado Pago, gestión de obras sociales/prepagas.
- Reportes de liquidación, caja diaria, facturación electrónica ante ARCA.
- Multi-sucursal, roles configurables, sobreturno como primera clase.
- Autenticación del paciente, portal del paciente, historia de turnos por usuario.
- Frontend propio (web o móvil).

## Métricas de éxito

- 0 turnos solapados persistidos bajo test de concurrencia real (dos reservas simultáneas al mismo slot → una sola gana, la otra recibe 409).
- 100% de los intentos de doble reserva secuencial rechazados con error de conflicto.
- Reserva guest end-to-end (disponibilidad → alta → cancelación → slot liberado) verde en CI local.
- Demo reproducible en Docker local sin servicios pagos ni credenciales externas.
- Trazabilidad Discovery → KB → Change verificable por la cátedra (RN02 testeada en capa de persistencia).

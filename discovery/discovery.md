# Discovery — TurnosAR (Sistema de turnos odontológicos)

**Proyecto:** TurnosAR — gestión de turnos para consultorios odontológicos de Argentina
**Materia:** Metodología I — Tecnicatura Universitaria en Programación (UTN)
**Contexto:** Trabajo de Integración sobre Spec-Driven Development (OpenSpec) y Active Stack
**Fecha:** 2026-10-02
**Informe competitivo completo:** [`docs/discovery/informe-discovery.md`](../docs/discovery/informe-discovery.md) (y `.pdf`)
**Documentos de respaldo:** [`_research-argentina.md`](../docs/discovery/_research-argentina.md) · [`_research-latam.md`](../docs/discovery/_research-latam.md) · [`_research-compliance-integrations.md`](../docs/discovery/_research-compliance-integrations.md) · [`_verificacion-fuentes.md`](../docs/discovery/_verificacion-fuentes.md)

> **Alcance de este documento.** Es el artefacto de la fase de Discovery del flujo
> OpenSpec/Active Stack. Registra las 11 dimensiones investigated. El detalle
> comparativo con fuentes, la matriz de puntuación y la verificación de URLs viven
> en el informe competitivo; este documento los resume y los referencia.

---

## 1. Problema que resuelve

En los consultorios odontológicos de Argentina la gestión de turnos es manual o
fragmentada: cuadernos o planillas de Excel para la agenda interna de sillones, y
WhatsApp informal para coordinar con los pacientes. De ahí se derivan tres daños
concretos:

1. **Solapamientos** entre profesionales y entre sillones, por no existir una
   validación de conflicto sobre el recurso físico y no solo sobre el profesional.
2. **Ausentismo** de pacientes, por no haber confirmación ni recordatorio automático.
3. **Pérdida de tiempo administrativo** que compite con la atención clínica.

El proyecto se enfoca en **(1)**: hacer de la noción de conflicto un invariante del
sistema en lugar de un chequeo best-effort en la interfaz.

## 2. Usuarios / roles

- **Recepcionista / Asistente:** gestiona la agenda global, asigna sillones o boxes,
  cobra señas, maneja sobreturnos y cancelaciones.
- **Odontólogo:** consulta su agenda diaria y semanal, ve las prestaciones asignadas y
  registra la atención clínica.
- **Paciente:** accede a un enlace público de reserva 24/7, selecciona profesional y
  horario, recibe confirmaciones y recordatorios, y solicita o cancela turnos.

**Decisión de alcance:** el paciente **no se autentica**. La reserva es *guest booking*
por enlace público. Esto evita introducir RBAC de paciente y mantener el modelo de
datos inicial simple, sin sacrificar el caso de uso.

## 3. Casos de uso

1. **CU01** — Como recepcionista, quiero agendar un turno asignando profesional,
   sillón/box y prestación, para reservar la atención sin solapar horarios.
2. **CU02** — Como paciente, quiero consultar la disponibilidad real y reservar un turno
   en línea, para coordinar mi atención sin depender de llamadas telefónicas.
3. **CU03** — Como recepcionista, quiero cancelar o reprogramar un turno, para liberar
   el horario o reasignarlo adecuadamente.
4. **CU04** — Como odontólogo, quiero visualizar mi agenda del día con las prestaciones
   asignadas, para organizar mi jornada de atención.

**Alcance del change a implementar:** CU01 y CU02 encadenadas — el camino completo desde
la consulta de disponibilidad del paciente hasta el alta del turno por la recepcionista,
con la validación transaccional de RN01 a RN05 como núcleo. CU03 y CU04 quedan
documentadas y modeladas, sin implementación.

## 4. Competidores / soluciones existentes

Se relevaron **34 sistemas**: 14 argentinos, 12 de Latinoamérica y 8 internacionales.
Detalle completo y fuentes en el [informe competitivo](../docs/discovery/informe-discovery.md).

**Hallazgo central:** ningún competidor argentino publica de forma explícita la
validación de solapamiento simultánea **por profesional y por sillón/box**. Solo 4 de 14
documentan control por profesional, y solo 1 (Órbita, «choque imposible») declara el
control por recurso físico. DentalSoft —el competidor argentino más completo y el único
que publica simultáneamente precios, control de solapamiento y reserva sin login— **no
menciona sillón en ninguna página de su sitio**.

Segundo hallazgo: la **opacidad en cumplimiento normativo**. 10 de 14 proveedores no
publican ningún mecanismo de seguridad; ninguno menciona la Ley 25.326; Benty declara
almacenamiento de datos de salud en Estados Unidos, lo que interactúa con la
prohibición de transferencia internacional del Art. 12.1.

Tercer hallazgo: el **canal de notificaciones es la dependencia económica real** del
rubro y casi nunca se expone como parte del costo total — DentalSoft declara
USD 0,026 por recordatorio de WhatsApp, Gendu comercializa packs desde $3.900/mes hasta
$59.900/mes por 1.000, AgendaPro ofrece el add-on desde $7.900/mes.

**Cinco competidores prioritarios para demo:** DentalSoft, AgendaPro, Dentiqa, Órbita,
DenPro. **Tres referencias de UX:** DentalSoft (demo pública), AgendaPro (onboarding),
NexHealth (capa de experiencia sobre PMS).

> **Salvedad metodológica.** «No evidenciado» significa que no se halló prueba pública,
> **no que la funcionalidad no exista**. El vacío del punto 4 se sostiene como *ausencia
> de comunicación documentada*, no como ausencia de implementación. Es un riesgo
> epistemológico declarado (ver punto 10, R2).

## 5. Funcionalidades necesarias

1. **Agenda de turnos con detección estricta de solapamientos**, validada
   simultáneamente por profesional y por sillón/box.
2. **Reserva online del paciente sobre disponibilidad real**, vía enlace público sin
   autenticación, sin posibilidad de doble reserva.
3. **Cancelación y reprogramación** de turnos, con liberación inmediata del slot en la
   agenda del profesional y del sillón.

## 6. Funcionalidades opcionales (backlog)

- Confirmación y recordatorio automático por WhatsApp o email.
- Cobro de señas integrando Mercado Pago y control de ausentismo.
- Ficha clínica básica y odontograma interactivo.
- Reportes de liquidación por profesional y caja diaria.
- Gestión de obra social y prepagas.
- Sobreturnos como caso de primera clase.
- Multi-sucursal y roles configurables.
- Facturación electrónica ante ARCA.

## 7. Reglas de negocio

- **RN01 — Duración por prestación.** Cada prestación define su duración estimada en
  minutos (consulta 30′, obturación 45′, endodoncia 90′) y determina el bloque de tiempo
  requerido en la agenda.
- **RN02 — Doble validación de solapamiento.** Un turno no puede solaparse con otro turno
  agendado para el **mismo profesional** ni para el **mismo sillón/box**, dentro de su
  intervalo de tiempo. Criterio de solapamiento: `inicio_nuevo < fin_anterior` y
  `fin_nuevo > inicio_anterior`. Dos turnos que se tocan en el borde
  (`inicio_nuevo == fin_anterior`) **no** se solapan.
- **RN03 — Validación temporal.** No se pueden agendar ni reservar turnos en fechas u
  horas pasadas, ni fuera del horario de atención configurado.
- **RN04 — Política de cancelación.** La cancelación registra el estado `Cancelado` y
  libera de forma inmediata el slot de tiempo en el sillón y en la agenda del profesional.
- **RN05 — Límite por paciente.** Un mismo paciente no puede tener más de un turno
  activo en el mismo día.

**RN02 es la invariante central del proyecto** y la que la cátedra evalúa a través de los
tests. Su implementación debe vivir en la capa de persistencia, no solo en la aplicación.

## 8. Integraciones

- **Servicio de notificaciones — MOCKEADO.** El dominio depende de una interfaz de
  servicio de notificaciones; la implementación del proyecto es un mock. No se usa la
  WhatsApp Business API de Meta: requiere verificación empresarial, plantillas aprobadas
  con hasta 24 h de revisión y un costo por mensaje cobrado a Meta. Justificación
  documentada con cifras en el informe competitivo.
- **Sin integraciones de pago ni facturación en el MVP.** Mercado Pago y ARCA quedan en
  backlog.
- **Sin ficha clínica en el MVP.** Esto es deliberado y reduce el riesgo legal: si el
  sistema no guarda datos clínicos, la reserva pública sin autenticación no manipula
  datos sensibles de salud (ver R3).

## 9. Restricciones

- **Trabajo individual.** Un único integrante.
- **Plazo:** entrega la semana próxima.
- **Presupuesto de infraestructura: $0.** Todo local, sin servicios pagos.
- **Sin restricción de stack** — el stack es una decisión de `kb-creator`.
- **Criterios de evaluación oficiales (100 pts):** Informe de Discovery 25 % ·
  Verificación 10 % · Fundación 20 % · Change OPSX 25 % · Video 10 % · Reflexión 5 % ·
  Trazabilidad 5 %.
- **Consecuencia de los criterios:** Discovery y Verificación suman **35 %** y quedan
  cerrados con este documento y el informe competitivo. Fundación (20 %) cubre KB,
  Roadmap y reglas
  de agente. El Change OPSX (25 %) corresponde a **un solo change**, por lo que debe ser
  chico y demostrable antes que amplio.

## 10. Riesgos

- **R1 — Concurrencia en la reserva (riesgo técnico central).** La reserva online es
  concurrente por naturaleza: dos pacientes pueden pedir el mismo slot simultáneamente.
  Una validación en la capa de aplicación deja una ventana entre la consulta de
  disponibilidad y el alta del turno. *Mitigación:* llevar RN02 a la base de datos —
  constraint de exclusión por `profesional + rango` y otra por `sillón + rango`, o
  serialización con bloqueo. Es lo que DentalFLOW comercializa como «garantía a nivel de
  base de datos».
- **R2 — El vacío de mercado puede ser un artefacto de publicación.** Que ningún
  proveedor *declare* la doble validación no prueba que ninguno la implemente. El
  hallazgo se sostiene como «no se comunica», no como «no existe».
- **R3 — Riesgo legal de la reserva sin autenticación.** Cualquiera puede ocupar un
  turno. La exclusión del Art. 5.2 inc. d de la Ley 25.326 (relación profesional) es
  *interpretación*, no texto que cubra explícitamente el caso odontológico.
  *Mitigación:* el MVP no almacena ficha clínica ni dato sensible, y la reserva exige
  confirmación por un canal. A documentar como análisis, no como texto legal.
- **R4 — Alcance y calendario.** Cuatro casos de uso, cinco reglas, tres roles y el
  andamiaje completo de OpenSpec/Active Stack, con plazo de una semana y un solo
  integrante. El riesgo es de calendario, no técnico.
- **R5 — La demo puede parecer ficticia.** Notificaciones mockeadas frente a un mercado
  donde todos venden WhatsApp real. *Mitigación:* convertir la limitación en argumento
  declarando el costo real con cifras verificadas, en lugar de ocultarlo.

## 11. Preguntas abiertas

- **Qx — Modelo de persistencia para RN02.** ¿PostgreSQL con constraint de exclusión
  (`EXCLUDE USING gist`), o SQLite con serialización explícita? Depende de qué stack
  elija `kb-creator`. Determina si el conflict checking es *declarativo* o *procedural*.
- **Qy — Modelo de consentimiento.** ¿El consentimiento expreso del Art. 5.1 de la
  Ley 25.326 se implementa como entidad persistida en el MVP, o queda documentado como
  requisito de la fase siguiente? Ningún competidor argentino lo declara, así que es
  diferenciador de bajo costo.
- **Qz — Nombre definitivo.** `TurnosAR` es provisorio; la cátedra no requiere uno
  propio.
- **Qw — Profundidad de los tests.** ¿Los tests de RN02 cubren también el escenario de
  dos reservas concurrentes reales, o solo el solapamiento lógico? Lo primero exige
  infraestructura de concurrencia y es más costoso; lo segundo es más barato de
  defender pero más débil.

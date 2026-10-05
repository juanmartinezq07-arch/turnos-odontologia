# Informe de Discovery competitivo — Sistemas de gestión odontológica

**Proyecto:** Sistema de turnos odontológicos para consultorios de Argentina
**Materia:** Metodología I — Tecnicatura Universitaria en Programación (UTN)
**Contexto:** Trabajo de Integración sobre Spec-Driven Development (OpenSpec) y Active Stack
**Fecha de consulta de todas las fuentes:** 2026-10-02
**Versión:** 1.0

---

## Resumen ejecutivo

Se relevaron **34 sistemas**: 14 argentinos, 12 de Latinoamérica y 8 internacionales con potencial de aplicación regional. De ellos, 15 entran en la matriz de puntuación.

El hallazgo central del relevamiento es negativo, y a la vez una oportunidad: **ningún competidor argentino publica de forma explícita la validación de solapamiento simultánea por profesional *y* por sillón/box.** Solo 4 de 14 documentan control por profesional, y apenas 1 (Órbita) declara el control por recurso físico. Esta ausencia de evidencia publicada no prueba que la función no exista —la instancia más clara de por qué el relevamiento se apoya en fuentes públicas— pero sí revela que es un eje que el Mercado no comunica, y por lo tanto un eje en el que un producto puede diferenciarse de forma verificable.

A esto se suma un segundo vacío: **la opacidad en materia de cumplimiento normativo.** 10 de 14 proveedores argentinos no publican ningún mecanismo de seguridad o marco normativo. Benty declara almacenamiento de datos de salud en Estados Unidos. Ninguno menciona la Ley 25.326. Esto deja al comprador argentino sin forma de evaluar el cumplimiento de la normativa que le aplica.

> **Disciplina de evidencia.** Todo dato de este informe procede de fuente pública con URL y fecha de consulta. Cuando una característica no está públicamente evidenciada, la celda dice literalmente **«No evidenciado»**. No se infiere funcionalidad a partir de conocimiento general ni de productos del mismo tipo. La sección *Verificación de fuentes* documenta el resultado de comprobar por fetch directo 8 URLs críticas, y consigna los errores detectados en el relevamiento inicial.

---

## A. Tabla comparativa

Ordenada por relevancia para el mercado argentino. El criterio de orden combina presencia local verificable, completitud funcional del dominio odontológico y similitud con el alcance del proyecto.

### A.1 — Competidores argentinos

| # | Producto | Empresa | Segmento | Despliegue | Anti-solap. profesional | Anti-solap. sillón | Reserva pública sin login | Notificaciones | Odontograma | Precio publicado |
|---|----------|---------|----------|-----------|-----------------------|--------------------|------------------------|---------------|-------------|-----------------|
| 1 | **DentalSoft** | DentalSoft (La Plata / Rosario) | Clínicas multi-profesional | Nube | **Sí** | No evidenciado | **Sí** — web propia, 4 pasos | WhatsApp + email (solo Pro) | **Sí** — 18 estados, notación FDI | **Sí** — $0 / $30.000 / $60.000 |
| 2 | **DentalFLOW** | TrapelTech (Río Negro) | Consultorio / clínica | Nube | **Sí** — garantía a nivel BD | No evidenciado | **Sí** — solo DNI, sin cuentas | Parcial — hoy email | No evidenciado | No — a consultar |
| 3 | **Dentiqa** | Violet Wave | Consultorio / clínica | Nube | **Sí** — bloqueo por profesional | No evidenciado | **Sí** — chatbot IA por WhatsApp | **Sí** — WhatsApp Business API oficial | No evidenciado | **Sí** — USD 89 / 149 / 249 |
| 4 | **Órbita** | Órbita Global (La Plata) | Consultorio / clínica | Nube | Parcial — agenda por profesional | **Sí** — «choque imposible» | **Sí** — alta por QR | **Sí** — Órbita Chat con IA | No evidenciado | **Sí** — USD 25 / 113 |
| 5 | **Denteo** | Datasoluciones (Santa Fe) | Consultorio | Nube | No evidenciado | No evidenciado | No evidenciado | **Sí** — 7 plantillas WA Business | No evidenciado | **Sí** — AR$ 30.000 / 45.000 |
| 6 | **Bilog** | Bilog (20+ años en AR) | Cadena / consultorio | Nube | No evidenciado — admite sobreturno | No evidenciado | **Sí** — pack por QR | **Sí** — WhatsApp y SMS | No evidenciado | No — cotiza por usuario |
| 7 | **DentalTec** | Tándem Digital | Clínica | Nube | No evidenciado | No evidenciado | No evidenciado | **Sí** — WhatsApp, 98 % entrega | No evidenciado | No — packs desde USD 9 |
| 8 | **Benty** | BENTY SRL (CABA) | Cadena | Nube | No evidenciado | No evidenciado | Parcial — portal del paciente | **Sí** — WhatsApp | No evidenciado | No — a consultar |
| 9 | **DentalSaaS** | DelRioTech SAS (Sgo. del Estero) | Clínica | Nube | **Sí** | No evidenciado | Parcial — portal de paciente | **Sí** — WhatsApp | No evidenciado | **Sí** — $59.000 / $149.000 / $349.000 |
| 10 | **DentiClick** | ThunderSkills (AR + VE) | Consultorio | Nube | No evidenciado | No evidenciado | **Sí** — subdominio propio | No evidenciado | No evidenciado | **Sí** — USD 0 / 12 / 22 / 35 |
| 11 | **OdontLux** | Creative Software | Consultorio | Nube | No evidenciado | No evidenciado | **Sí** — turnero 24/7 | **Sí** — canal no especificado | No evidenciado | No — módulos a cotizar |
| 12 | **Sigo** | Hosting Bahía (Buenos Aires) | Consultorio | Nube | No evidenciado | No evidenciado | No evidenciado | **Sí** — recordatorios por email | No evidenciado | **Sí** — $25.000 (1 profesional) |
| 13 | **OdontoApp** | Sovil | Consultorio | Nube | No evidenciado | No evidenciado | No evidenciado | Declaradas, canal no especificado | No evidenciado | No evidenciado |
| 14 | **ClinIA / OdontoClinIA** | Emprinet | Consultorio | Nube | No evidenciado | No evidenciado | **Sí** — agenda 24/7 + asistente IA | **Sí** — WhatsApp | No evidenciado | No — demo sin costo |

### A.2 — Latinoamérica

| # | Producto | Empresa | País | Presencia AR | Anti-solap. profesional | Anti-solap. sillón | Reserva sin login | WhatsApp | Precio publicado |
|---|----------|---------|------|---------------|-----------------------|--------------------|-------------------|-----------|-----------------|
| 15 | **AgendaPro** | AgendaPro Inc. | Argentina | **Sí** — sede y teléfono local | No evidenciado | No evidenciado | No evidenciado | **Sí** — add-on desde $7.900/mes | **Sí** — USD 9 / 29 / 59 |
| 16 | **SimpleTurno** | — | Argentina / Río de la Plata | **Sí** | No evidenciado | No evidenciado | No evidenciado | **Sí** | **Sí** — plan gratuito |
| 17 | **Reservo** | — | Argentina | **Sí** | No evidenciado | No evidenciado | Parcial | **Sí** | No evidenciado |
| 18 | **Clinicorp** | — | Brasil | No evidenciado | No evidenciado | No evidenciado | **Sí** | **Sí** | **Sí** (BRL) |
| 19 | **Prontuário Verde** | — | Brasil | No evidenciado | No evidenciado | No evidenciado | **Sí** | **Sí** | No evidenciado |
| 20 | **Simples Dental** | — | Brasil | No evidenciado | No evidenciado | No evidenciado | **Sí** | **Sí** | No evidenciado |
| 21 | **Dentalis** | — | Brasil | No evidenciado | No evidenciado | No evidenciado | No evidenciado | **Sí** | No evidenciado |
| 22 | **Sistema ClínicaPro** | — | Brasil | No evidenciado | No evidenciado | No evidenciado | No evidenciado | **Sí** | No evidenciado |
| 23 | **Dentalink** | — | Chile | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No — cotización |
| 24 | **Doctoralia PRO** | Docplanner | España | **Sí** | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado |
| 25 | **UDENTIVA** | — | Uruguay | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado |
| 26 | **DentalCitas** | — | México | No evidenciado | **Sí** (declarado) | **Sí** (declarado) | **Sí** (declarado) | No evidenciado | **Sí** (MXN) |

### A.3 — Internacionales de referencia

| # | Producto | Empresa | País | Presencia regional | Vertical odontológica | Anti-solap. | Precio publicado |
|---|----------|---------|------|-------------------|----------------------|-------------|-----------------|
| 27 | **Open Dental** | Open Dental Software | EE. UU. | **Sí** — soporte en español en Perú y Uruguay; usuarios en Brasil | **Sí** — completo | No evidenciado públicamente | **Sí** (USD, variable) |
| 28 | **Oryx Dental** | Oryx Dental | EE. UU. | No evidenciado | **Sí** | No evidenciado | **Sí** — USD 0 a 400 |
| 29 | **NexHealth** | NexHealth | EE. UU. | No evidenciado | No — capa de experiencia sobre PMS | No evidenciado | No evidenciado |
| 30 | **CareStack** | CareStack | EE. UU. | No evidenciado | **Sí** | No evidenciado | **Sí** (tercero, USD) |
| 31 | **Curve Dental** | Curve Dental | EE. UU. | No evidenciado | **Sí** | No evidenciado | No evidenciado |
| 32 | **Weave** | Weave | EE. UU. | No evidenciado | **Sí** | No evidenciado | **Sí** (USD) |
| 33 | **Dentally** | Henry Schein One | R. Unido | No evidenciado | **Sí** | No evidenciado | No evidenciado |
| 34 | **Dentrix** | Henry Schein One | EE. UU. | No evidenciado | **Sí** | No evidenciado | No evidenciado |

### A.4 — Referencias de canal y precio (no odontológicos puros)

| Producto | Perfil | Rol en el análisis |
|----------|--------|--------------------|
| **Gendu** | Turnería y recordatorios (AR) | Modelo de negocio del canal de notificaciones |
| **DenPro** | Software odontológico con dominio AR, empresa de la UE | Referencia de seguridad y cumplimiento |

---

## B. Matriz de puntuación

Escala de 0 a 5. Los pesos son los fijados por la consigna.

| Criterio | Peso |
|----------|------|
| Gestión de turnos y automatización | 25 % |
| Funcionalidad odontológica clínica | 20 % |
| Integraciones locales y WhatsApp | 15 % |
| Administración, cobros y facturación | 15 % |
| Experiencia del paciente | 10 % |
| Seguridad, exportación y trazabilidad | 10 % |
| Precio y facilidad de adopción | 5 % |

| # | Producto | Turnos 25 % | Odont. 20 % | Integr. 15 % | Admin. 15 % | Exp. paciente 10 % | Seguridad 10 % | Precio 5 % | **Total ponderado** |
|---|----------|------------|------------|--------------|-------------|--------------------|---------------|-----------|---------------------|
| 1 | **DentalSoft** | 4 | 2 | 4 | 5 | 4 | 1 | 4 | **3,45** |
| 2 | **Open Dental** | 4 | 5 | 1 | 4 | 2 | 2 | 3 | **3,30** |
| 3 | **Dentiqa** | 4 | 2 | 4 | 2 | 4 | 3 | 3 | **3,15** |
| 3 | **Gendu** | 3 | 2 | 4 | 4 | 4 | 2 | 4 | **3,15** |
| 5 | **AgendaPro** | 3 | 2 | 4 | 4 | 4 | 1 | 5 | **3,10** |
| 6 | **Órbita** | 4 | 2 | 3 | 2 | 4 | 1 | 3 | **2,80** |
| 7 | **DentalFLOW** | 4 | 2 | 1 | 2 | 4 | 4 | 2 | **2,75** |
| 7 | **NexHealth** | 3 | 1 | 3 | 3 | 5 | 3 | 2 | **2,75** |
| 9 | **DenPro** | 3 | 3 | 1 | 2 | 2 | 5 | 4 | **2,70** |
| 9 | **Prontuário Verde** | 3 | 4 | 3 | 2 | 2 | 1 | 2 | **2,70** |
| 11 | **SimpleTurno** | 3 | 2 | 2 | 3 | 4 | 1 | 5 | **2,65** |
| 11 | **Clinicorp** | 3 | 3 | 3 | 2 | 3 | 1 | 3 | **2,65** |
| 13 | **Oryx Dental** | 3 | 3 | 1 | 2 | 2 | 3 | 3 | **2,45** |
| 14 | **Denteo** | 2 | 2 | 4 | 2 | 1 | 1 | 4 | **2,20** |
| 14 | **DentalCitas** | 3 | 3 | 1 | 1 | 3 | 1 | 3 | **2,20** |

### Lectura de la matriz

**DentalSoft encabeza el ranking** y lo hace por un motivo revelador: su ventaja no está en la gestión de turnos (4/5) sino en **administración y facturación (5/5)** — obra social, liquidaciones con comisiones de profesionales, caja diaria con MercadoPago, ranking de profesionales. Compite donde el consultorio argentino realmente gasta su complejidad.

**Open Dental es segundo (3,30)** pese a no tener presencia comercial declarada en Argentina, por una sola razón: 5/5 en funcionalidad odontológica clínica. Es el estándar de referencia mundial del dominio y sirve como especificación de qué debería incluir un odontograma.

**El hallazgo del relevamiento aparece como una ausencia, y como puntaje bajo, en la matriz:** la columna de *Seguridad, exportación y trazabilidad* es la más baja de todo el ranking en los competidores argentinos — 1/5 para seis de ellos. Ninguno publica mecanismos de seguridad; ninguno cita la Ley 25.326. Los dos únicos que alcanzan 4/5 y 5/5 (DentalFLOW y DenPro) lo hacen por declaración técnica (garantía a nivel de BD, cifrado AES-256 e ISO 27001), y DenPro lo hace desde la Unión Europea invocando GDPR, no la normativa que le corresponde al cliente argentino.

---

## C. Análisis competitivo

### C.1 — Funcionalidades que ya son estándar de mercado

Las siguientes capacidades aparecem en la mayoría del mercado y **no constituyen diferenciación**:

- **Reserva online 24/7.** Presente en 6 de 14 sistemas argentinos verificados. Es expectativa de mercado, no ventaja.
- **Recordatorio automático por WhatsApp y/o email.** Prácticamente universal, aunque su profundidad varía: DentalSoft lo automático solo en el plan Pro y manual en el plan Gestión; Gendu lo incluye como *add-on* con costo aparte.
- **Agenda por profesional con duración variable por prestación.** Implícito en todos los productos del rubro.
- **Odontograma con notación FDI.** DentalSoft es el único argentino que lo documenta con detalle (18 estados clínicos, historial por pieza con fecha y profesional).
- **Gestión de obra social y prepagas.** Estándar en Argentina, y un factor de diferenciación relevante frente a productos genéricos regionales.
- **Multi-sucursal.** Esperado en consultorios grandes; ausente en buena parte del mercado chico.

### C.2 — Diferenciadores reales y verificables

| Producto | Diferencial | Evidencia |
|----------|-------------|-----------|
| **DentalSoft** | Único argentino que documenta el ciclo administrativo completo: obra social aplicada por tratamiento, centro de liquidaciones con comisiones, reintegros de obras sociales, sincronización con Google Calendar por profesional | Sitio oficial, sección de funcionalidades |
| **Dentiqa** | Único con **WhatsApp Business API oficial** declarado y chatbot de IA como canal de reserva | Sitio oficial |
| **AgendaPro** | Mayor escala regional; único integrado con **Google Reserve / Google My Business**; IA de agenda («Sofia»); marketplace | `agendapro.com/ar` y `/ar/planes` |
| **Órbita** | **Único proveedor que declara control de conflicto por sillón** («choque imposible» por recurso físico) | Sitio oficial |
| **DentalFLOW** | Declara garantizar el anti-solapamiento **a nivel de base de datos**, no solo en la capa de aplicación | Sitio oficial |
| **Bilog** | El **sobreturno como acción de menú explícita**: el doble turno se trata como decisión asistida y no como error a evitar | Sitio oficial |
| **DenPro** | Único con cifrado **AES-256**, centros **ISO 27001** y declaración de cumplimiento Normativo — aunque desde la UE y bajo GDPR | `denpro.ar` |

Sobre Bilog conviene una lectura de diseño, no de mercado: tratar el solapamiento intencional como un caso de primera clase del modelo, y no únicamente como una violación a impedir. Es la diferencia entre una agenda que se *rechaza* y una agenda que distingue el error del overdbooking deliberado.

### C.3 — Vacíos frecuentes del mercado argentino

1. **La doble validación de solapamiento no se comunica.** 0 de 14 proveedores argentinos declaran control simultáneo por profesional y por sillón/box. Solo 4 declaran control por profesional; solo 1 por sillón. Este es el eje central del proyecto.
2. **Cumplimiento normativo opaco.** 10 de 14 no publican ningún mecanismo de seguridad. Benty declara datos de salud almacenados en **Estados Unidos**, lo que interactúa con la prohibición de transferencia internacional del Art. 12.1 de la Ley 25.326. **Ningún proveedor argentino menciona la Ley 25.326.**
3. **Precios poco publicados.** 8 de 14 no publican precios, lo que obliga al comprador a un contacto comercial y oculta el costo total.
4. **El canal de notificaciones es la dependencia económica silenciosa.** El recordatorio automático no es gratuito en la práctica: DentalSoft declara **USD 0,026 por recordatorio de WhatsApp** (pagado a Meta), Gendu comercializa packs desde **$3.900/mes por 50 recordatorios** hasta **$59.900/mes por 1.000**, y AgendaPro ofrece el add-on desde **$7.900/mes**. Un consultorio con 200 turnos mensuales paga del orden de $11.800/mes solo en recordatorios en el modelo de reseller. **Este costo recurrente no suele compararse entre proveedores.**
5. **Ausencia de estándar en reserva sin login.** Solo 6 de 14 ofrecen reserva pública sin autenticación, y normalmente lo hacen por web propia o QR, no como producto en sí.

### C.4 — Oportunidades de innovación

1. **Hacer de la invariante un diferencial verificable.** Si la doble validación por profesional y por sillón es el contrato del sistema —con tests que lo demuestren y una regla de base de datos que lo imponga—, eso es algo que ningún competidor argentino publica. No es una función más: es la ausencia documentada del mercado.
2. **Declarar el costo del canal de notificaciones.** Un producto que expone el costo por notificación como parte del modelo, o que separa el canal del dominio detrás de una interfaz, elimina la sorpresa que hoy atraviesa a todo el comprador argentino.
3. **Consentimiento expreso como funcionalidad.** El Art. 5.1 de la Ley 25.326 exige consentimiento **libre, expreso e informado, que conste por escrito**. Ningún proveedor argentino declara esto. Convertirlo en un artefacto del sistema —registro de consentimiento en la reserva, sin datos clínicos expuestos en la URL— es una diferencia de cumplimiento genuinamente defendible.
4. **Reserva pública sin login como estándar, con verificación por canal.** El patrón guest booking resuelve fricción de adopción, y combinado con confirmación por un canal verificado reduce el abuso sin introducir RBAC.
5. **Interfaz de notificación como costura arquitectónica.** Diseñar el sistema con una interfaz de notificaciones por detrás, en vez de contra una API de terceros, es exactamente lo que permite pasar de la simulación a la integración real sin reescribir el dominio. Es una ventaja de arquitectura, no un atajo.

---

## D. Recomendación final

### D.1 — Cinco competidores prioritarios para analizar mediante demo

| Orden | Producto | Motivo de la demo |
|--------|----------|-------------------|
| 1 | **DentalSoft** | El competidor más completo del mercado argentino y el único que publica precios, control de solapamiento y reserva sin login simultáneamente. Hay una demo pública en `dentalsoft.com.ar/demo` y un flujo de reserva de 4 pasos observable. Referencia directa para el alcance del proyecto. |
| 2 | **AgendaPro** | Mayor escala y el precio más bajo de la categoría (USD 9/mes). Su flujo de onboarding y su integración con Google Reserve muestran el estándar de experiencia del paciente que el mercado considera aceptable. |
| 3 | **Dentiqa** | El único con **WhatsApp Business API oficial** declarado. Es la referencia para entender qué implica una integración real con Meta, y quéoty argumento de venta construye alrededor de la IA conversacional. |
| 4 | **Órbita** | El único que declara **control de conflicto por sillón** («choque imposible»). Es el competidor más cercano al eje central del proyecto y el mejor para contrastar el alcance exacto de un control por recurso físico. |
| 5 | **DenPro** | Dominio argentino con empresa de la UE. Publica cifrado AES-256 e ISO 27001, y un precio bajo. Sirve como contraste de posicionamiento entre seguridad declarada y cumplimiento normativo local. |

### D.2 — Tres productos de referencia para experiencia de usuario

| Producto | Qué tomar de él |
|----------|------------------|
| **DentalSoft** (demo pública) | El flujo de reserva en 4 pasos —datos, profesional, fecha, confirmar— es el patrón de menor fricción observado. Referencia para el formulario público del paciente. |
| **AgendaPro** | Onboarding y propuesta de valor. Muestra cómo se comunica el valor de las automatizaciones a un consultorio chico que no tiene departamento de sistemas. |
| **NexHealth** | Su arquitectura de *capa de experiencia del paciente sobre un sistema de gestión* es la referencia conceptual para separar el dominio de la notificaciones y de los canales, que es la decisión de diseño central de este proyecto. |

### D.3 — MVP sugerido

#### Imprescindibles — constituyen el change a implementar

Estos son los tres casos de uso del MVP y las cinco reglas de negocio que los sostienen:

| Regla | Descripción | Por qué es imprescindible |
|-------|-------------|---------------------------|
| **RN01** | Duración por prestación: cada prestación define su duración en minutos y determina el bloque de tiempo en agenda | Sin duración variable no hay forma de validar solapamientos con sentido |
| **RN02** | **Doble validación de solapamiento:** un turno no puede solaparse con otro del **mismo profesional** ni del **mismo sillón/box** dentro de su intervalo (`inicio ≤ nuevo < fin`) | Eje del proyecto y del vacío de mercado detectado |
| **RN03** | Validación temporal: no se pueden agendar ni reservar turnos en el pasado ni fuera del horario de atención configurado | Regla de integridad básica, testeable |
| **RN04** | Política de cancelación: la cancelación registra estado `Cancelado` y libera de inmediato el slot en sillón y agenda del profesional | Cierra el ciclo de vida del turno; sin ella el sistema no puede volver a ofrecer ese horario |
| **RN05** | Límite por paciente: un paciente no puede tener más de un turno activo en el mismo día | Regla de negocio real del consultorio, con caso borde claro |

Casos de uso asociados: **CU01** (recepcionista agenda asignando profesional, sillón y prestación), **CU02** (paciente consulta disponibilidad y reserva en línea), **CU03** (recepcionista cancela o reprograma), **CU04** (odontólogo ve su agenda del día con las prestaciones asignadas).

#### Diferenciadores — el valor que el mercado no cubre

1. **La invariante doble, declarada y testeada.** RN02 llev Consistency a la capa de persistencia (constraint o transacción), no solo a la validación de la capa de aplicación, y acompañada de tests que cubren: solapamiento parcial por profesional, solapamiento parcial por sillón, solapamiento en las dos dimensiones simultáneamente, y el caso límite de contacto exacto de borde (`inicio_nuevo == fin_anterior`), que debe permitirse.
2. **Interfaz de notificaciones detrás de una costura arquitectónica.** Implementación mockeada, con el costo real documentado en el informe. Convierte la limitación en una decisión de diseño explícita y trazable.
3. **Consentimiento expreso registrado en la reserva.** Requisito del Art. 5.1 de la Ley 25.326, y ningún proveedor argentino lo declara.
4. **Reserva pública sin autenticación, con verificación por canal.** Patrón guest booking que evita el RBAC del paciente sin abrir el dominio a reservas libres sin control.

#### Para etapas posteriores — backlog

- Cobro de señas con integración de Mercado Pago y control de ausentismo (no-show).
- Ficha clínica básica y odontograma interactivo.
- Confirmación y recordatorio por WhatsApp con la Cloud API real, una vez resuelta la verificación empresarial.
- Reportes de liquidación por profesional y caja diaria.
- Gestión de obra social y prepagas.
- Sobreturnos como caso de primera clase, en la línea del patrón que Bilog documenta.
- Multi-sucursal y roles configurables.
- Facturación electrónica ante ARCA.

---

## Verificación de fuentes

Se comprobó por fetch directo (HTTP GET, sin caché de terceros) la vigencia y el contenido de 8 URLs críticas. Criterio: **CONFIRMADO** = la página dice lo que se afirma con cita literal; **PARCIAL** = parte se confirma; **REFUTADO** = la página contradice o no contiene lo atribuido; **NO CONFIRMABLE** = no hay cita textual en la URL indicada.

| # | URL | Estado | Resultado |
|---|-----|--------|-----------|
| V1 | `dentalsoft.com.ar/precios` | **Datos CONFIRMADOS / URL REFUTADA** | La ruta `/precios` **no publica precios**: devuelve el sitio de la clínica de demostración. Los precios están en la home: Gratis $0, Gestión $30.000/mes, Pro $60.000/mes, +$10.000/mes por profesional adicional. Confirmado textualmente que el plan Gestión dice «No se manda nada de forma automática» mientras el Pro ofrece «Recordatorios automáticos» con **0,026 USD por recordatorio** atribuido a Meta. **Corrección aplicada:** todas las citas de DentalSoft apuntan a la home, no a `/precios`. |
| V2 | `agendapro.com/ar` | **PARCIAL** | Existe página argentina (`<title>`: «Software & App para Agendar Turnos #1 en Argentina») y publica teléfono local, pero **sin prefijo +54** («11 5032 6351»). Confirma «Más de 20.000 negocios» en la home y «Recordatorios por WhatsApp y email», con add-on desde $7.900/mes por 50 mensajes. **La afirmación de reserva sin cuenta NO aparece**: no hay «sin login», «sin registro» ni «sin cuenta». **Corrección aplicada:** eliminada esa afirmación; la cifra de `/ar/planes` (+30.000 negocios en Latinoamérica) se distingue de la de la home. |
| V3 | `argentina.gob.ar/normativa/nacional/ley-25326-64790/actualizacion` | **CONFIRMADO** | Texto actualizado, sancionada el 04-10-2000, Boletín Oficial 29517. **Matiz:** la URL rotula «TEXTO ACTUALIZADO», no «vigente». El Art. 2 define la categoría **«Datos sensibles»** —incluida «información referente a la salud»— y la expresión «datos personales sensibles» **no aparece en la norma**. Art. 5.1 exige consentimiento «libre, expreso e informado, el que deberá constar por escrito». Art. 7.3 prohíbe archivos que almacenen datos sensibles; Art. 8 habilita a establecimientos sanitarios bajo secreto profesional; Art. 12.1 prohíbe transferencias internacionales sin protección adecuada. **Corrección aplicada:** se usa la definición literal del Art. 2. |
| V4 | `whatsappbusiness.com/products/platform-pricing` | **Modelo CONFIRMADO / Precios NO CONFIRMABLES** | Confirma cobro **por mensaje entregado**, **cuatro** categorías (marketing, utility, authentication, service) y que **dentro de la ventana de 24 h los mensajes `service` no se cobran**, más una ventana gratuita de 72 h tras un anuncio con clic a WhatsApp. **Los precios no son verificables en esta URL**: la tabla de tarifas es interactiva (selectores de mercado/moneda/categoría) y no expone valores en el HTML. La tarifa oficial para Argentina en ARS queda como **No evidenciado**. **Corrección aplicada:** ningún precio por mensaje se atribuye a esta URL. |
| V5 | `gendu.com.ar/planes` | **CONFIRMADO** | Planes: Básico **Gratis**, Comercial $9.100/mes, Profesional $14.400/mes, Premium $24.000/mes, **Master $42.100/mes** (máximo, confirmado). Packs de recordatorios WhatsApp **adicionales al plan**: 50 → $3.900/mes, 100 → $5.900/mes, 300 → $17.900/mes, 1.000 → **$59.900/mes**. **Matiz crítico:** el plan Básico gratis **no incluye WhatsApp**, solo recordatorios automáticos por email; y en los planes pagos el envío por WhatsApp incluido es **manual de un clic**. **Corrección aplicada:** el pack de 1.000 es costo adicional, no total. |
| V6 | `mercadopago.com.ar/herramientas-para-vender/check-out` | **PARCIAL** | Se confirman 4,39 % + IVA a 10 días y 6,29 % + IVA al instante, **pero la afirmación era incompleta**: la página publica **cuatro** tramos — también **1,49 % + IVA a 35 días** y **3,39 % + IVA a 18 días**. La tabla **no está rotulada «Checkout Pro»** y la propia página advierte que el costo varía según provincia, medio de pago y plazo. **Corrección aplicada:** se documentan los cuatro tramos con la ambigüedad señalada. |
| V7 | `bcra.gob.ar/estadisticas-indicadores` | **NO CONFIRMABLE** | Es un índice con columnas Fecha y Valor **vacías** (render por JavaScript). El valor de **1.545,12 ARS/USD del 25/09/2026 no puede sostenerse con esta URL** y no aparece en ninguna parte de la página. **Corrección aplicada:** las conversiones a USD se presentan como aproximación y quedan marcadas como **No evidenciado**, o se citan las series correspondientes (`/tipo-de-cambio-minorista/`, serie 7927). |
| V8 | `denpro.ar` | **CONFIRMADO** | Plan Basic **$19.900/mes** (1 usuario) y Team **$29.900/mes** (usuarios ilimitados); 30 días de prueba sin tarjeta. **Dato no verificado previamente y relevante:** «Utilizamos cifrado AES-256, almacenamos todos los datos en centros de datos certificados ISO 27001 en la UE y cumplimos totalmente con el GDPR». Soporte **+34** (España); marca registrada de **Elite Digital Services, LLC**. **Corrección aplicada:** DenPro **no es un competidor argentino local** sino un proveedor con dominio dirigido al mercado argentino y categoría de datos en la UE, bajo GDPR y no bajo Ley 25.326. |

### Resumen de la verificación

**3 de 8 fuentes quedaron enteramente confirmadas, 3 parcialmente, 1 refutada en su URL y 1 no confirmable.** Los errores detectados fueron materiales, no cosméticos:

- Una URL de precios **inexistente** había servido de base para las citas de un competidor principal. Los datos eran correctos; la dirección no.
- Se había atribuido a AgendaPro una **funcionalidad que la página no declara**.
- Un competidor presentado como **argentino** es en realidad una empresa de la Unión Europea con datos alojados en la UE.
- Se había citado un **tipo de cambio sin fuente verificable**, del que dependían conversiones de precios a USD.
- La definición legal se había citado con una fórmula textual que **no aparece en la norma**.

La lección metodológica que corresponde a este trabajo de Integración es directa: **la verificación por fetch directo no es un control de calidad opcional, es parte del método.** Un relevamientoCompetitive sin comprobación de fuentes arrastra afirmaciones que sobreviven porque suenan razonables.

---

## Anexo — Documentos de respaldo

| Archivo | Contenido |
|---------|-----------|
| `docs/discovery/_research-argentina.md` | 14 sistemas argentinos, 15 campos cada uno, con URL y fecha |
| `docs/discovery/_research-latam.md` | 20 sistemas de Latinoamérica e internacionales, con matriz de presencia por país |
| `docs/discovery/_research-compliance-integrations.md` | WhatsApp Business API, Mercado Pago, Ley 25.326, rangos de precio |
| `docs/discovery/_verificacion-fuentes.md` | Verificación por fetch de 8 URLs, con cita textual literal |

**Convención aplicada en todos los documentos:** «No evidenciado» significa que no se encontró prueba pública. **No implica que la funcionalidad no exista.**

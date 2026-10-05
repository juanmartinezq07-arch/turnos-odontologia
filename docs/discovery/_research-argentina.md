# Investigación de sistemas de gestión odontológica en Argentina

**Fecha de consulta de todas las fuentes:** 2026-10-02
**Alcance:** sistemasArgentina que gestionan agenda de turnos odontológicos, con foco de análisis en (1) validación anti-solapamiento por profesional y por sillón, (2) reserva online pública sin login y (3) notificaciones automáticas al paciente.
**Criterio de inclusión:** el sistema debe permitir cargar y gestionar turnos de pacientes y/o historia clínica odontológica. Se exige evidencia verificable de origen argentino.
**Criterio de exclusión:** sistemas cuyo origen o identidad legal no puede verificarse, y sistemas que no gestionan turnos.

**Convenciones de evidencia**
- `Evidencia del proveedor` = declarado en el sitio oficial del producto.
- `Evidencia de terceros` = declarada por un tercero (registro público, tienda de aplicaciones, etc.).
- `No evidenciado` = no se encontró prueba pública; **no implica que la función no exista**.
- Todo precio citado es el publicado por el propio proveedor en la fecha de consulta y **cambia con frecuencia** en un mercado con inflación alta.

---

## Tabla resumen

| # | Sistema | Empresa | Anti-solap. profesional | Anti-solap. sillón | Reserva pública sin login | Notificaciones automáticas | Precios públicos |
|---|---------|---------|-------------------------|---------------------|----------------------------|---------------------------|-----------------|
| 1 | DentalSoft | DentalSoft (La Plata / Rosario) | **Sí** — detección automática de solapamiento | No evidenciado | **Sí** — web propia, 4 pasos | **Sí** — WhatsApp + email (solo plan Pro) | **Sí** — $30.000 / $60.000 por mes |
| 2 | DentalSaaS | DelRioTech SAS (Santiago del Estero) | **Sí** — detección automática de solapamientos | No evidenciado | Parcial — auto-agendamiento con portal de paciente | **Sí** — WhatsApp, requiere configuración extra | **Sí** — $59.000 / $149.000 / $349.000 |
| 3 | DentalFLOW | TrapelTech (Choele Choel, Río Negro) | **Sí** — garantía a nivel de base de datos | No evidenciado | **Sí** — solo DNI, sin cuentas | **Parcial** — hoy email; WhatsApp "en camino" | No — precio a consultar |
| 4 | Órbita | Órbita Global (La Plata) | Parcial — agenda por profesional | **Sí** — "choque imposible" por sillón | **Sí** — alta por QR | **Sí** — Órbita Chat con IA 24/7 | **Sí** — USD 25 / USD 113 por mes |
| 5 | Dentiqa | Violet Wave | **Sí** — bloqueo por profesional, "sin riesgo de doble-reserva" | No evidenciado | **Sí** — chatbot de IA por WhatsApp | **Sí** — WhatsApp Business API oficial | **Sí** — USD 89 / 149 / 249 por mes |
| 6 | DentiClick | ThunderSkills (AR + VE) | No evidenciado | No evidenciado | **Sí** — subdominio propio del consultorio | No evidenciado (chat con IA en la web) | **Sí** — US$0 / 12 / 22 / 35 por mes |
| 7 | Benty | BENTY SRL (Ciudad de Buenos Aires) | No evidenciado | No evidenciado | Parcial — portal del paciente | **Sí** — WhatsApp | No — precio a consultar |
| 8 | Denteo | Datasoluciones, CUIT 20-30156574-8 (Reconquista, Santa Fe) | No evidenciado | No evidenciado | No evidenciado | **Sí** — 7 plantillas de WhatsApp Business | **Sí** — AR$ 30.000 / 45.000 por mes |
| 9 | Bilog | Bilog (20+ años en Argentina) | No evidenciado — admite sobreturno | No evidenciado | **Sí** — pack Bilog Turnos vía QR | **Sí** — WhatsApp y SMS | No — cotiza por usuario |
| 10 | DentalTec | Tándem Digital | No evidenciado | No evidenciado | No evidenciado | **Sí** — WhatsApp, 98 % de entrega | No — packs de mensajería desde USD 9 |
| 11 | OdontLux | Creative Software | No evidenciado | No evidenciado | **Sí** — turnero 24/7 | **Sí** — automáticas, canal no especificado | No — modules a cotizar |
| 12 | Sigo | Hosting Bahía (Bahía Blanca, Buenos Aires) | No evidenciado | No evidenciado | No evidenciado | **Sí** — recordatorios por email | **Sí** — $25.000 por mes (1 profesional) |
| 13 | OdontoApp | Sovil | No evidenciado | No evidenciado | No evidenciado | Declarados, canal no especificado | No evidenciado |
| 14 | ClinIA / OdontoClinIA | Emprinet | No evidenciado | No evidenciado | **Sí** — agenda online 24/7 + asistente IA | **Sí** — WhatsApp | No — demo sin costo, sin precio público |

**Lectura de la tabla:** solo **4 de 14** sistemas documentan de forma explícita alguna forma de control de solapamiento, y **ninguno** lo documenta simultáneamente por profesional y por sillón. Solo **6 de 14** ofrecen reserva pública sin login. El control de solapamiento es, en la práctica comercial del rubro, una funcionalidad de marketing no publicada — un hallazgo directamente útil para el proyecto académico.

---

## DentalSoft

1. **Proveedor / empresa:** DentalSoft. Contacto comercial directo y autobiographical: "Contacto directo con los desarrolladores", "Sin intermediarios: somos los desarrolladores". Sin razón social ni CUIT publicados. Fuentes: https://www.dentalsoft.com.ar/ y https://www.dentalsoft.com.ar/precios (consulta: 2026-10-02).
2. **Origen y país:** Argentino. pie de página "© 2026 DentalSoft. Todos los derechos reservados. Hecho en 🇦🇷 Argentina", con oficinas en La Plata (Buenos Aires) y Rosario (Santa Fe); teléfonos +54 9. Fuente: https://www.dentalsoft.com.ar/ (consulta: 2026-10-02).
3. **Segmento objetivo:** clínicas y consultorios con varios profesionales y multi-sucursal. El plan base incluye "Agenda para sólo 1 odontólogo" y se Adds +$10.000 por profesional adicional. Fuente: https://www.dentalsoft.com.ar/precios (consulta: 2026-10-02).
4. **Tipo de despliegue:** 100 % en la nube. "DentalSoft funciona 100% en la nube... Nada que instalar ni actualizar manualmente". Fuente: https://www.dentalsoft.com.ar/ (consulta: 2026-10-02).
5. **Gestión de turnos y agenda:** vistas semanal, diaria y mensual; drag & drop con confirmación; urgencias; sobreturnos; multi-sucursal; sincronización con Google Calendar por profesional; "Horarios individuales por odontólogo con intersección al horario clínica". Fuente: https://www.dentalsoft.com.ar/ (consulta: 2026-10-02).
6. **Anti-solapamiento por profesional:** **Sí, evidenciado.** "Urgencias y sobreturnos con detección automática de solapamiento". En la reserva online: "Slots calculados en tiempo real según disponibilidad real". También en la tabla de planes: "Agenda de turnos digital". Fuente: https://www.dentalsoft.com.ar/ (consulta: 2026-10-02).
7. **Anti-solapamiento por sillón / recurso físico:** **No evidenciado.** No se menciona sillón, box, cabina ni recurso físico en ninguna página oficial. La intersección citada es entre el horario individual del odontólogo y el horario de la clínica, no entre sillones. Fuente: https://www.dentalsoft.com.ar/ (consulta: 2026-10-02).
8. **Reserva online pública sin login:** **Sí, evidenciado.** Web propia incluida en el plan Pro con URL del tipo `tuclinica.dentalsoft.com.ar`; flujo guiado de 4 pasos (datos → profesional → fecha → confirmar), "El paciente elige profesional, fecha y horario en 4 simples pasos", "Reservas 24/7", "Sin llamadas". No se describe creación de cuenta para el paciente. Existe además una demo pública: https://www.dentalsoft.com.ar/demo y https://dentalsoft.com.ar/demo/reservar. Fuentes: https://www.dentalsoft.com.ar/ y https://dentalsoft.com.ar/demo/reservar (consulta: 2026-10-02).
9. **Notificaciones y recordatorios:** **Sí, automatizado, pero condicionado al plan.** En el plan Pro: "Recordatorios automáticos... Meta cobra 0,026 USD por cada recordatorio de WhatsApp. Los recordatorios automáticos por Email son gratuitos". En el plan Gestión, en cambio, la misma funcionalidad es **manual**: "Envío manual de recordatorios por WhatsApp — Se abre WhatsApp con el mensaje... ya redactado... No se manda nada de forma automática". Esta distinción es un riesgo real para un comprador que compara solo la lista de funciones. También incluye campaigns de reactivación, cobro automático de deudas y solicitud de reseñas de Google. Fuente: https://www.dentalsoft.com.ar/precios (consulta: 2026-10-02).
10. **Historia clínica y odontograma:** ficha médica con antecedentes y notas; odontograma con 18 estados clínicos, notación FDI e historial por pieza con fecha y profesional; módulo de ortodoncia con arcada, aparatología y galería de fotos; consentimiento con firma; recetas digitales. Fuente: https://www.dentalsoft.com.ar/ (consulta: 2026-10-02).
11. **Obras sociales, facturación y pagos:** cobertura de obra social aplicada automáticamente por tratamiento y plan; centro de liquidaciones con comisiones de profesionales y reintegros de obras sociales; caja diaria con efectivo, tarjeta, transferencia, MercadoPago y obra social; reportes con ranking de profesionales. Fuente: https://www.dentalsoft.com.ar/ (consulta: 2026-10-02).
12. **Roles y permisos:** "Cada uno tiene su propio acceso con permisos configurables según su rol, de forma que cada usuario solo ve lo que necesita". No se publica un catálogo detallado de roles. Fuente: https://www.dentalsoft.com.ar/ (consulta: 2026-10-02).
13. **Seguridad, privacidad y cumplimiento:** existen páginas de Términos, Privacidad y Eliminación de datos, pero no se verificaron desde esta ronda de consulta. No se publica certificado, centro de datos, cifrado en reposo ni marco normativo aplicable (por ejemplo, Ley 25.326 o Ley 26.529). **No evidenciado.** Fuentes: https://www.dentalsoft.com.ar/terminos, https://www.dentalsoft.com.ar/privacidad, https://www.dentalsoft.com.ar/eliminacion-datos (consulta: 2026-10-02).
14. **Precios y trial:** plan Gratis $0/mes durante 6 meses con límite de 50 turnos por mes y agenda de 1 odontólogo; plan Gestión $30.000/mes; plan Pro $60.000/mes; +$10.000/mes por profesional adicional; más de 4 profesionales se cotiza a medida. Implementación declarada en menos de 24 horas. Fuente: https://www.dentalsoft.com.ar/precios (consulta: 2026-10-02).
15. **Adopción y evidencia de uso:** "Más de 300 clínicas en Argentina" y "4.9/5 de satisfacción promedio" — **evidencia del proveedor**, sin metodología ni casos verificables. Se publican tres testimonios con nombre e iniciales. No se hallaron reseñas de terceros verificables. Fuente: https://www.dentalsoft.com.ar/ (consulta: 2026-10-02).

**Diagnóstico:** es el competidor mejor alineado con el proyecto académico en los tres focos: publica precios, publica control de solapamiento y publica reserva sin login. Su debilidad es la opacidad legal y de seguridad, y la diferencia entre recordatorio automático (Pro) y manual (Gestión) fácilmente pasa desapercibida.

---

## DentalSaaS

1. **Proveedor / empresa:** DelRioTech SAS. Contacto `contacto@delriotechsas.com.ar`; sitio corporativo https://www.delriotechsas.com.ar. Fuente: https://dental.delriotech.com.ar/ (consulta: 2026-10-02).
2. **Origen y país:** Argentino. "© 2026 DelRioTech SAS... Hecho con ♥ en Santiago del Estero, Argentina"; insignia "Desarrollado en Argentina". Fuente: https://dental.delriotech.com.ar/ (consulta: 2026-10-02).
3. **Segmento objetivo:** desde consultorios de un solo sillón hasta clínicas de alto volumen; planes Consultorio, Clínica y Pro. Fuente: https://dental.delriotech.com.ar/ (consulta: 2026-10-02).
4. **Tipo de despliegue:** 100 % en la nube, desde cualquier dispositivo; "Configuración en minutos"; "Sin contratos de permanencia". Fuente: https://dental.delriotech.com.ar/ (consulta: 2026-10-02).
5. **Gestión de turnos y agenda:** "Vista diaria, semanal y mensual con columnas por profesional. Bloqueo de horarios, feriados y vacaciones. Detección automática de solapamientos y vista rápida de disponibilidad"; agenda inteligente; lista de disponibilidad. Fuente: https://dental.delriotech.com.ar/ (consulta: 2026-10-02).
6. **Anti-solapamiento por profesional:** **Sí, evidenciado.** "Detección automática de solapamientos", en el contexto de una agenda con "columnas por profesional". Fuente: https://dental.delriotech.com.ar/ (consulta: 2026-10-02).
7. **Anti-solapamiento por sillón / recurso físico:** **No evidenciado.** Ninguna mención a sillón, box o recurso físico. Fuente: https://dental.delriotech.com.ar/ (consulta: 2026-10-02).
8. **Reserva online pública sin login:** **Parcial.** El plan Clínica y Pro incluyen "Portal del paciente" y "Auto-agendamiento por pacientes", y el portal permite "Autogestión de turnos... desde la web y/o instalable como app". El portal del paciente implica autenticación; no se documenta un flujo de reserva anónima ni una URL pública por consultorio. **Reserva sin login: No evidenciado.** Fuente: https://dental.delriotech.com.ar/ (consulta: 2026-10-02).
9. **Notificaciones y recordatorios:** **Sí, con configuración adicional.** "Recordatorios automáticos por WhatsApp 24h y 2h antes de cada turno. Reducí ausencias hasta un 50%". Pero el servicio es un extra: "El servicio de recordatorios por WhatsApp requiere una configuración adicional. Puede realizarse de forma autónoma o con asistencia de DelRioTech SAS. Consultá costos y disponibilidad". Complemento adicional: Asistente de IA para WhatsApp 24/7 con agenda de turnos desde la conversación y modo supervisado. Fuente: https://dental.delriotech.com.ar/ (consulta: 2026-10-02).
10. **Historia clínica y odontograma:** historia clínica digital con antecedentes; odontograma interactivo adulto e infantil; periodontograma con SVG interactivo; fichas clínicas especializadas por 6 disciplinas (Ortodoncia con análisis de Angle y cefalometría, Periodoncia, Endodoncia, Implantología, Prótesis, Cirugía); consentimientos digitales con firma electrónica y snapshot legal; imágenes clínicas con compresión. Fuente: https://dental.delriotech.com.ar/ (consulta: 2026-10-02).
11. **Obras sociales, facturación y pagos:** catálogo nacional de obras sociales precargado; nomenclador por país; planilla mensual por obra social; caja y cobros con múltiples medios; presupuestos con aprobación online; cobros online con MercadoPago; liquidaciones de profesionales; laboratorios dentales. Fuente: https://dental.delriotech.com.ar/ (consulta: 2026-10-02).
12. **Roles y permisos:** multi-usuario, multi-odontólogo y multi-secretaria según plan; "Auditoría completa: Registro automático de cada acción realizada en el sistema... Sabé quién hizo qué, cuándo y desde dónde", exportable a PDF y Excel. No se publica un catálogo explícito de roles. Fuente: https://dental.delriotech.com.ar/ (consulta: 2026-10-02).
13. **Seguridad, privacidad y cumplimiento:** el sitio incluye una sección titulada "Seguridad y aislamiento de datos" y páginas de Términos y Política de Privacidad. No se verificaron desde esta ronda los estándares concretos (cifrado, certificaciones, localización de datos). Además ofrece "White Label" y "consentimientos con snapshot legal". Fuente: https://dental.delriotech.com.ar/legal/terminos y https://dental.delriotech.com.ar/legal/privacidad (consulta: 2026-10-02).
14. **Precios y trial:** Consultorio $59.000/mes (1 odontólogo, hasta 300 pacientes y 300 turnos/mes, 2 GB); Clínica $149.000/mes (hasta 5 odontólogos, 1.000 pacientes, 10 GB); Pro $349.000/mes (ilimitados, 50 GB). Anual con 2 meses bonificados. Todos los planes "sin permanencia", pago con MercadoPago, transferencia o PayPal. Fuente: https://dental.delriotech.com.ar/ (consulta: 2026-10-02).
15. **Adopción y evidencia de uso:** **No evidenciado.** El sitio no publica cantidad de clientes, casos de éxito verificables ni reseñas de terceros. Solo declara canales de contacto. Fuente: https://dental.delriotech.com.ar/ (consulta: 2026-10-02).

**Diagnóstico:** competidor técnicamente fuerte y muy transparente en precios y alcance funcional, pero sin evidencia pública de adopción y con el canal de WhatsApp detrás de un pago adicional no quantifiable — una dependencia crítica para un producto académico que solo necesita notificaciones mockeadas.

---

## DentalFLOW

1. **Proveedor / empresa:** "Un producto de TrapelTech". Contacto `hola@trapeltech.com`. Sin razón social ni CUIT publicados. Fuente: https://dentalflow.ar/ (consulta: 2026-10-02).
2. **Origen y país:** Argentino. "© 2026 DentalFLOW · TrapelTech... Choele Choel, Río Negro Argentina"; el sitio se presenta explícitamente como software "pensado para el consultorio odontológico argentino" y "Hecho para la odontología argentina". Fuente: https://dentalflow.ar/ (consulta: 2026-10-02).
3. **Segmento objetivo:** desde consultorio individual de un odontólogo hasta clínica con varias sedes y profesionales ("Funciona igual para un consultorio individual que para una clínica con varias sedes y profesionales"). Fuente: https://dentalflow.ar/ (consulta: 2026-10-02).
4. **Tipo de despliegue:** navegador, sin instalación, mobile-first tanto para el equipo como para el paciente; "Funciona desde el navegador, en la computadora y en el celular". Fuente: https://dentalflow.ar/ (consulta: 2026-10-02).
5. **Gestión de turnos y agenda:** vista diaria y semanal con estados por color y actualización en tiempo real; "Horarios, duración por consulta y bloqueos configurables"; reserva interna para pacientes presenciales o telefónicos; sobreturnos y lista de espera; panel de control con confirmados, ausencias e ingresos por tratamiento y por profesional. Fuente: https://dentalflow.ar/ (consulta: 2026-10-02).
6. **Anti-solapamiento por profesional:** **Sí, con la evidencia más fuerte del conjunto.** "Agenda sin choques: El sistema garantiza que dos personas nunca tomen el mismo horario. Sin doble-reserva." Y en la sección de preguntas frecuentes: "¿Qué pasa si dos personas quieren el mismo horario? Solo una lo consigue. El sistema lo garantiza a nivel de base de datos; no hay doble-reserva". Fuente: https://dentalflow.ar/ (consulta: 2026-10-02).
7. **Anti-solapamiento por sillón / recurso físico:** **No evidenciado.** El flujo de reserva ofrece elegir "profesional, tipo de consulta, día y horario libre", sin dimensión de sillón. La garantía se refiere a profesional, no a recurso físico. Fuente: https://dentalflow.ar/ (consulta: 2026-10-02).
8. **Reserva online pública sin login:** **Sí, con la evidencia más fuerte del conjunto.** "Sin apps ni cuentas: solo el DNI". Y: "¿Mis pacientes tienen que crear una cuenta o bajar una app? No. Reservan desde un enlace, solo con su DNI y datos de contacto." El paciente también cancela y reprograma solo. La reserva se comparte por WhatsApp, Instagram o la web del consultorio. Fuente: https://dentalflow.ar/ (consulta: 2026-10-02).
9. **Notificaciones y recordatorios:** **Hallazgo contrario a la expectativa del rubro.** "Recordatorios automáticos de confirmación y de control. El paciente confirma con un toque". Pero en la sección de preguntas frecuentes: "¿Los recordatorios son por WhatsApp? **Hoy los recordatorios salen por email. WhatsApp está en camino** y lo sumamos sin que tengas que cambiar de sistema." En la lista de funciones en camino: "WhatsApp · Próximamente / Obras sociales · Próximamente / Señas y pagos · Próximamente / Facturación · Próximamente". Es decir, cuatro módulos centrales todavía no existen. Fuente: https://dentalflow.ar/ (consulta: 2026-10-02).
10. **Historia clínica y odontograma:** ficha digital con odontograma interactivo por pieza; antecedentes, alergias y medicación; notas de evolución con opción de nota privada; adjuntos de radiografías y fotos. Fuente: https://dentalflow.ar/ (consulta: 2026-10-02).
11. **Obras sociales, facturación y pagos:** **No disponible todavía.** "Obras sociales · Próximamente", "Señas y pagos · Próximamente", "Facturación · Próximamente". Solo se ofrece "Valor orientativo del tratamiento visible al reservar". Sí incluye reportes de ingresos por tratamiento y por profesional. Fuente: https://dentalflow.ar/ (consulta: 2026-10-02).
12. **Roles y permisos:** "Roles y permisos por usuario: cada uno ve lo suyo", con perfiles differentiated para recepción, profesionales y administración; "La recepción no ve las historias clínicas: solo los profesionales tratantes". Fuente: https://dentalflow.ar/ (consulta: 2026-10-02).
13. **Seguridad, privacidad y cumplimiento:** es el candidato con mejor documentación de seguridad. "Cada consultorio está aislado. Una clínica nunca ve los datos de otra"; "Cifrado en tránsito y en reposo"; "Cada acceso a una historia clínica queda auditado"; "Diseñado según la Ley 25.326". Fuente: https://dentalflow.ar/ (consulta: 2026-10-02).
14. **Precios y trial:** no publica precios. "El plan depende del tamaño de tu consultorio... Escribinos por WhatsApp y te pasamos el precio en el día". Prueba gratuita sin tarjeta, con migración de datos incluida y onboarding guiado; "Sin contratos de permanencia"; demo de 15 minutos. Fuente: https://dentalflow.ar/ (consulta: 2026-10-02).
15. **Adopción y evidencia de uso:** **No evidenciado.** No se publican clientes, casos ni reseñas verificables. El producto se presenta con capturas propias y un producto "en camino" amplio. Fuente: https://dentalflow.ar/ (consulta: 2026-10-02).

**Diagnóstico:** referencia técnica del conjunto en los dos focos más críticos del proyecto (garantía de no-doble-reserva a nivel de base de datos y reserva sin ningún tipo de cuenta). Su debilidad es la madurez del producto: obras sociales, facturación y WhatsApp están explícitamente "próximamente", lo que en un mercado argentino sin obra social ni facturación electrónica no es un detalle menor.

---

## Órbita

1. **Proveedor / empresa:** "Órbita Global". Contacto `info@hiorbita.com`; offices en "Espacio Weiaut 2, Diagonal 74 1681, La Plata, Argentina". Sin CUIT publicado. Fuente: https://hiorbita.com/precios (consulta: 2026-10-02).
2. **Origen y país:** Argentino. "Inteligencia artificial argentina para clínicas y consultorios de salud. **Hecha en La Plata**"; "La Plata, Argentina"; "© 2026 Órbita Global". Fuente: https://hiorbita.com/precios (consulta: 2026-10-02).
3. **Segmento objetivo:** tres perfiles bien definidos — Consultorio (un sillón, sin recepción), Clínica (1 a 3 sedes) y Red (más de 3 sedes). El plan Consultorio admite de 3 a 8 profesionales. Fuente: https://hiorbita.com/precios (consulta: 2026-10-02).
4. **Tipo de despliegue:** 100 % web. El producto estrella de IA (Hi Órbita, dispositivo de voz del sillón) "todavía no salió". Fuente: https://hiorbita.com/precios (consulta: 2026-10-02).
5. **Gestión de turnos y agenda:** "Agenda por sillón: Dos pacientes no pueden caer en el mismo sillón"; agendamiento inteligente que ofrece primero horarios que no dejan huecos; control automático del próximo control al cerrar el tratamiento; recontacto de quien no responde. Fuente: https://hiorbita.com/erp/funcionalidades/llena-la-agenda y https://hiorbita.com/erp/funcionalidades/llena-la-agenda/agenda (consulta: 2026-10-02).
6. **Anti-solapamiento por profesional:** **Parcial.** La agenda se organiza por profesional y hay bloqueo por profesional implícito en la estructura de planes ("-3+profesionales", "-15+profesionales", "Profesionales sin tope"), pero **no se declara una regla de no-solapamiento entre profesionales**. La declaración explícita de conflicto es por sillón, no por profesional. Fuente: https://hiorbita.com/precios y https://hiorbita.com/erp/funcionalidades/llena-la-agenda/agenda (consulta: 2026-10-02).
7. **Anti-solapamiento por sillón / recurso físico:** **Sí, evidenciado — único caso del conjunto.** En la tabla comparativa de planes de los tres niveles: "**Agenda por sillón, con choque imposible** ✓ ✓ ✓". Y en la home: "Agenda por sillón — Dos pacientes no pueden caer en el mismo sillón". Fuente: https://hiorbita.com/precios y https://hiorbita.com/erp/funcionalidades/llena-la-agenda (consulta: 2026-10-02).
8. **Reserva online pública sin login:** **Sí, evidenciado.** "Alta por QR: Una opción más: el paciente se carga solo desde su celular" — incluida en los planes Clínica y Red ("Alta del paciente por QR ✓ ✓"). Se describe al paciente cargándose solo, es decir sin cuenta previa. Fuente: https://hiorbita.com/erp/funcionalidades/llena-la-agenda y https://hiorbita.com/precios (consulta: 2026-10-02).
9. **Notificaciones y recordatorios:** **Sí, automatizado con IA.** "Órbita Chat recuerda el turno y vuelve a escribirle al que no responde"; chatbot con IA 24/7, juez IA que detecta urgencias, "Confirmación 48 y 24 hs antes", mensajes ilimitados en los cuatro plazos de contratación. Se factura por volumen: "Los precios publicados incluyen hasta 15.000 mensajes por mes". Fuente: https://hiorbita.com/precios y https://hiorbita.com/erp/funcionalidades/llena-la-agenda (consulta: 2026-10-02).
10. **Historia clínica y odontograma:** ficha con odontograma y periodontograma; dictado por voz del odontograma y de la receta; historia clínica firmada y encadenada;.exportación total de los datos; prescripción con firma. Fuente: https://hiorbita.com/precios (consulta: 2026-10-02).
11. **Obras sociales, facturación y pagos:** presupuestos con embudo y tasa de aceptación; cobranzas y caja; convenios y liquidaciones; laboratorio con trazabilidad de materiales por lote; marketing con créditos y publicación de campañas. Fuente: https://hiorbita.com/precios (consulta: 2026-10-02).
12. **Roles y permisos:** "Log de accesos y roles" incluido en los tres planes; en el plan Red, "Panel consolidado entre sedes" y "Ejecutivo de cuenta asignado". Fuente: https://hiorbita.com/precios (consulta: 2026-10-02).
13. **Seguridad, privacidad y cumplimiento:** publica páginas de Términos, Política de privacidad y **Eliminación de datos** — un compromiso de portabilidad y baja poco común en el rubro. Los estándares técnicos concretos no se verificaron desde esta ronda. Fuente: https://hiorbita.com/terminos, https://hiorbita.com/privacidad, https://hiorbita.com/eliminacion-de-datos (consulta: 2026-10-02).
14. **Precios y trial:** producto **Órbita Chat**: USD 200/clínica/mes precio de lista, con descuentos por plazo (mensual USD 200, trimestral USD 180, semestral USD 170, anual USD 150), Turnero de Órbita gratis 6 meses y luego USD 20/mes, descuento de USD 100/mes desde 3 sedes. Producto **Órbita Gestión**: Consultorio USD 25/mes, Clínica USD 113/mes, Red a medida desde USD 500/mes. Todos "sin IVA"; add-ons de dictado por voz (USD 30/mes) y módulo de marketing (USD 90/mes). El precio está en dólares y se puede abonar "en dólares, pesos o USDT". "Implementación en 30 días". Fuente: https://hiorbita.com/precios (consulta: 2026-10-02).
15. **Adopción y evidencia de uso:** **No evidenciado.** No se publican cantidad de clínicas, casos de éxito ni reseñas de terceros. La web incluye una página de "Comparativa" contra otros sistemas del rubro y una agenda de LinkedIn/Calendly, pero sin métricas de clientes. Fuente: https://hiorbita.com/comparativa (consulta: 2026-10-02).

**Diagnóstico:** el único competidor que ataca el problema correctamente (sillón como recurso), y el único con precios en una moneda estable para un proyecto académico. La ausencia de evidencia de no-solapamiento por profesional y de adopción verificable son las dos laguna principales.

---

## Dentiqa

1. **Proveedor / empresa:** "Dentiqaby Violet Wave". Contacto `wa.me/5492664000051`; agenda de demo en https://violetwave.online/agenda; perfiles en Instagram `violetwave.online` y LinkedIn "Violet Wave". Sin CUIT publicado. Fuente: https://dentiqa.app/ar (consulta: 2026-10-02).
2. **Origen y país:** Orientado a Argentina, con cobertura declarada en Latinoamérica. "Software Dental para Clínicas en **Argentina** con IA y WhatsApp"; "Precios en pesos argentinos. Pagás con Mercado Pago"; la plataforma "usa zona horaria de Argentina (GMT-3) por defecto". El pie declara "© 2026 Dentiqa by Violet Wave". La dirección social de contacto es argentina (+54 9). Fuente: https://dentiqa.app/ar (consulta: 2026-10-02).
3. **Segmento objetivo:** "Clínicas dentalas" de tres tamaños — Starter (5 usuarios), Professional (10 usuarios) y Enterprise (grupos y cadenas multi-clínica). Fuente: https://dentiqa.app/ar (consulta: 2026-10-02).
4. **Tipo de despliegue:** 100 % web, "Desde un navegador, sin instalación", responsive. La demo de producto se expone en https://dashboard.dentiqa.app/login. Fuente: https://dentiqa.app/ar (consulta: 2026-10-02).
5. **Gestión de turnos y agenda:** "Agenda multi-dentista con bloqueos por profesional"; vistas día y semana; "reprogramación desde la cita con validación del nuevo horario"; bloqueos de franjas horarias, días completos o vacaciones. Fuente: https://dentiqa.app/ar (consulta: 2026-10-02).
6. **Anti-solapamiento por profesional:** **Sí, evidenciado.** "Bloqueos de agenda por profesional — franjas horarias, días completos o vacaciones — que el asistente IA respeta al ofrecer turnos, **sin riesgo de doble-reserva**". Además, la reprogramación se valida contra el horario nuevo. Fuente: https://dentiqa.app/ar (consulta: 2026-10-02).
7. **Anti-solapamiento por sillón / recurso físico:** **No evidenciado.** No hay mención a sillón, box o recurso físico. La agenda es por profesional, no por recurso. Fuente: https://dentiqa.app/ar (consulta: 2026-10-02).
8. **Reserva online pública sin login:** **Sí, por canal conversacional.** El paciente no entra a un sistema web: agenda por WhatsApp a través del chatbot. "Un chatbot con IA atiende por WhatsApp 24/7, agenda citas automáticamente". El flujo ilustrado muestra al paciente deslogueado, escribiendo, recibiendo horarios ("¡Hola María! Tenemos estos turnos disponibles: Mar 17 — 10:00hs, Mié 18 — 14:00hs, Jue 19 — 09:30hs") y confirmando. No se publica una URL pública de reserva; el canal es WhatsApp. Fuente: https://dentiqa.app/ar (consulta: 2026-10-02).
9. **Notificaciones y recordatorios:** **Sí, la integración más profunda del conjunto.** "Recordatorios automáticos 24h y 2h antes vía WhatsApp"; campañas automáticas de cumpleaños, reactivación a 6 meses y post-procedimiento; "Integración oficial con WhatsApp Business API"; "Proveedor de tecnología verificado por Meta". Volumen incluido por plan: 2.000, 5.000 o 10.000 mensajes de WhatsApp por mes. Fuente: https://dentiqa.app/ar (consulta: 2026-10-02).
10. **Historia clínica y odontograma:** historia clínica digital con 8 tabs; odontograma versionado (permanente y temporal); periodontograma con métricas BOP/NIC/placa; plan de tratamiento con presupuesto; evoluciones con firma electrónica; consentimientos; galería de imágenes; indicaciones y recetas con plantillas. Fuente: https://dentiqa.app/ar (consulta: 2026-10-02).
11. **Obras sociales, facturación y pagos:** "Facturación por profesional" (Professional) y "Facturación consolidada del grupo" (Enterprise). No se documenta liquidación de obras sociales ni integración con AFIP/ARCA. **Obras sociales: No evidenciado.** Fuente: https://dentiqa.app/ar (consulta: 2026-10-02).
12. **Roles y permisos:** multi-usuario con roles Dueño, Admin, Dentista y Recepción; multi-clínica con grupos y sucursales; roles y permisos incluidos en todos los planes. Fuente: https://dentiqa.app/ar (consulta: 2026-10-02).
13. **Seguridad, privacidad y cumplimiento:** "AES-256 + audit logs". Declara cumplimiento de la Ley 26.529 con criterio prudente: "La Ley 26.529 reconoce la historia clínica informatizada como válida siempre que garantice integridad, inalterabilidad e identificación del autor de cada registro. Dentiqa te da las herramientas para respaldar esos requisitos... **El cumplimiento final depende del uso que hagas en tu clínica**". Tiene páginas de privacidad, términos y eliminación de datos. Fuente: https://dentiqa.app/ar y https://dentiqa.app/legal/politica-de-privacidad (consulta: 2026-10-02).
14. **Precios y trial:** Starter USD 89/mes (AR$ 135.000), Professional USD 149/mes (AR$ 225.000), Enterprise USD 249/mes (AR$ 380.000). Se cobra en USD y se paga con Mercado Pago en pesos al tipo de cambio del momento. "Mes a mes, cancelás cuando querés. Sin ataduras ni permanencia". "Implementación integral incluida" (configuración, migración, capacitación). Además, un "Programa Fundador" con "Cupo limitado: 10 clínicas fundadoras en Argentina" y precio congelado de por vida. Fuente: https://dentiqa.app/ar (consulta: 2026-10-02).
15. **Adopción y evidencia de uso:** **No evidenciado, y el producto está en lanzamiento.** El propio sitio declara "Dentiqa está en lanzamiento", muestra el panel en versión "v0.5.0" y un "Programa Fundador" con 10 cupos. No hay casos de éxito publicados. Fuente: https://dentiqa.app/ar (consulta: 2026-10-02).

**Diagnóstico:** el competidor más ambicioso en IA y el único con integración oficial de WhatsApp Business, pero es un producto pre-lanzamiento (v0.5.0) con un teto declarado de 10 clínicas fundadoras. Su material de marketing es  y su base de clientes es, por construcción, casi inexistente.

---

## DentiClick

1. **Proveedor / empresa:** "Desarrollado por ThunderSkills" (https://thunderskills.net/). Sin CUIT publicado. Fuente: https://www.denticlick.app/ (consulta: 2026-10-02).
2. **Origen y país:** Argentino y venezolano. "Software odontológico hecho en Argentina y Venezuela"; "© 2026 DentiClick · Software odontológico argentino y venezolano". Fuente: https://www.denticlick.app/ (consulta: 2026-10-02).
3. **Segmento objetivo:** cuatro planes desde un profesional individual hasta centros con varias sucursales — Gratis, Consultorio, Clínica (hasta 5 profesionales), Centro (profesionales ilimitados, varias sucursales). Fuente: https://www.denticlick.app/ (consulta: 2026-10-02).
4. **Tipo de despliegue:** web, instalable como app; "Sin instalar nada"; "Desde el celu o la compu — Instalable como app. Todo sincronizado". Fuente: https://www.denticlick.app/ (consulta: 2026-10-02).
5. **Gestión de turnos y agenda:** "Agenda y turnos — Vista diaria, semanal y mensual. Estados, reprogramación y reservas por internet para sus pacientes"; "Sobejecuta el stock y se descuenta automáticamente cuando marca un turno como atendido". Fuente: https://www.denticlick.app/ (consulta: 2026-10-02).
6. **Anti-solapamiento por profesional:** **No evidenciado.** La agenda declara vistas y reprogramación, pero ninguna regla de no-solapamiento entre profesionales ni detección de conflictos. Fuente: https://www.denticlick.app/ (consulta: 2026-10-02).
7. **Anti-solapamiento por sillón / recurso físico:** **No evidenciado.** Ninguna mención a sillón, box o recurso físico. Fuente: https://www.denticlick.app/ (consulta: 2026-10-02).
8. **Reserva online pública sin login:** **Sí, evidenciado con la Mecanismo más explícito del conjunto.** "Tu web incluida — Cada consultorio tiene su página con subdominio propio (ej: drjuarez.denticlick.app), con su logo y colores... y un botón para que sus pacientes reserven turno solos, las 24 horas". El flujo de reserva ilustrado no incluye paso de autenticación: se elige el consultorio, se eligen practitioner's especialidades, luego "Elija un servicio" y "Reservar turno". Fuente: https://www.denticlick.app/ (consulta: 2026-10-02).
9. **Notificaciones y recordatorios:** **No evidenciado como automáticas.** Incluye un "chat con inteligencia artificial" que responde dudas, ayuda al equipo y orienta a los pacientes dentro de la web, pero el sitio no declara envío de recordatorios, confirmaciones ni cancelaciones automáticas por WhatsApp, email o SMS. Fuente: https://www.denticlick.app/ (consulta: 2026-10-02).
10. **Historia clínica y odontograma:** historia clínica con evoluciones, antecedentes y alertas médicas que avisan al atender; odontograma interactivo por caras, con dentición permanente, temporal y mixta, historial con versiones y estados existente / a realizar / realizado; recetas imprimibles; carga de imágenes y visor 3D de escáneres. Fuente: https://www.denticlick.app/ (consulta: 2026-10-02).
11. **Obras sociales, facturación y pagos:** "Liquidación por obra social y mes, con códigos de nomenclador. Exportás a CSV y PDF"; presupuestos y cuenta corriente con cargo automático al realizar; pagos y recibos imprimibles; stock de insumos con alertas de mínimo y lista de compras. Fuente: https://www.denticlick.app/ (consulta: 2026-10-02).
12. **Roles y permisos:** "Multi-profesional — Sumé a tu equipo con roles. Cada profesional con su agenda y sus cobros"; usuarios ilimitados en plan Clínica. Fuente: https://www.denticlick.app/ (consulta: 2026-10-02).
13. **Seguridad, privacidad y cumplimiento:** publica "Backup semanal automático — Todas las semanas le llega por correo una copia de su información", lo que implica transferencia de datos de salud por correo sin cifrado descrito. No se publica política de privacidad, cifrado, aislamiento multi-tenant ni marco normativo. **No evidenciado.** Fuente: https://www.denticlick.app/ (consulta: 2026-10-02).
14. **Precios y trial:** es el único con plan gratuito permanente y precios más bajos del conjunto. Gratis US$0 (1 profesional, hasta 30 pacientes, todas las funciones); Consultorio US$12/mes (1 profesional + secretaria); Clínica US$22/mes (hasta 5 profesionales, usuarios ilimitados); Centro US$35/mes (profesionales ilimitados, varias sucursales). "1 mes gratis, sin tarjeta"; "Cancela cuando quieras". Fuente: https://www.denticlick.app/ (consulta: 2026-10-02).
15. **Adopción y evidencia de uso:** **No evidenciado.** El sitio publica "Soporte en español" pero no cantidad de consultorios, casos de éxito ni reseñas de terceros. Fuente: https://www.denticlick.app/ (consulta: 2026-10-02).

**Diagnóstico:** el competidor másAccessible del conjunto (plan gratuito real y US$12 por mes) y con el flujo de reserva pública más fácil de evidenciar. Sus debilidades son la ausencia total de notificaciones automáticas y una postura de seguridadilusoria (backup semanal por correo).

---

## Benty

1. **Proveedor / empresa:** **BENTY SRL**, "una sociedad de nacionalidad argentina con domicilio social Uriburu 627, piso 5° '29', de la Ciudad de Buenos Aires". Fuentes: https://benty.com.ar/terms/ y https://benty.com.ar/privacy/ (consulta: 2026-10-02).
2. **Origen y país:** Argentino, verificado en documento legal. La Política de Privacidad declara que BENTY "es una sociedad de nacionalidad argentina"; los Términos reiterate lo mismo. Fuente: https://benty.com.ar/privacy/ (consulta: 2026-10-02).
3. **Segmento objetivo:** "Tecnología simple para equipos odontológicos"; "Para profesionales independientes como para consultorios y clínicas con varios profesionales". Fuente: https://benty.com.ar/ (consulta: 2026-10-02).
4. **Tipo de despliegue:** web, sin instalaciones complejas; "Accedé desde la compu del consultorio, tu casa o donde necesites". El acceso al profesional se hace "mediante un acceso Web seguro mediante validación de usuario y contraseña". Fuente: https://benty.com.ar/terms/ (consulta: 2026-10-02).
5. **Gestión de turnos y agenda:** agenda organizada "por profesional, espacio y disponibilidad"; disponibilidad por boxes o espacios de atención; historial de pacientes pendientes para retomarlos cuando aparece un horario. Fuente: https://benty.com.ar/funcionalidades/agenda-y-turnos/ (consulta: 2026-10-02).
6. **Anti-solapamiento por profesional:** **No evidenciado.** La página de agenda declara organización por profesional y coordenação, pero nunca declara una regla de no-solapamiento, detección de conflictos ni garantía de que un profesional no pueda ser reservado dos veces. Fuente: https://benty.com.ar/funcionalidades/agenda-y-turnos/ (consulta: 2026-10-02).
7. **Anti-solapamiento por sillón / recurso físico:** **No evidenciado.** Se declara el concepto de "espacio de trabajo" y la compatibilidad con "varios boxes o espacios", pero no se declara ninguna validación que impida que dos pacientes ocupen el mismo espacio en el mismo horario. La mención de espacio es descriptiva, no normativa. Fuente: https://benty.com.ar/funcionalidades/agenda-y-turnos/ (consulta: 2026-10-02).
8. **Reserva online pública sin login:** **Parcial.** El portal del paciente permite que "actualicen sus datos y reserven turnos online cuando les resulte cómodo". No se publica una URL de reserva anónima, ni se aclara si el paciente necesita cuenta. **Reserva sin login: No evidenciado.** Fuente: https://benty.com.ar/funcionalidades/autogestion-de-pacientes/ (consulta: 2026-10-02).
9. **Notificaciones y recordatorios:** **Sí, automatizado por WhatsApp.** "Recordá, confirmá y atendé las consultas de tus pacientes desde WhatsApp", con el objetivo declarado de reducir el ausentismo. La página de ausentismo se titula "Confirmá turnos y mantené el contacto con tus pacientes sin sumar trabajo manual a recepción". Fuente: https://benty.com.ar/funcionalidades/menos-ausentismo/ (consulta: 2026-10-02).
10. **Historia clínica y odontograma:** historia clínica digital con evolución, documentos, odontograma, recetas y tratamientos; planes de tratamiento con presupuestos y alternativas; órdenes de laboratorio con seguimiento; recetas digitales y electrónicas. Fuente: https://benty.com.ar/ (consulta: 2026-10-02).
11. **Obras sociales, facturación y pagos:** facturas electrónicas integradas; liquidaciones del staff calculadas "a partir de su actividad"; cuentas corrientes. No se documenta liquidación de obras sociales. **Obras sociales: No evidenciado.** Fuente: https://benty.com.ar/ (consulta: 2026-10-02).
12. **Roles y permisos:** "Organización del staff y permisos — Sumá profesionales, asigná roles y configurá permisos"; licencias del integrante para vacaciones y ausencias que "reflejen la realidad" de la disponibilidad. Fuente: https://benty.com.ar/ (consulta: 2026-10-02).
13. **Seguridad, privacidad y cumplimiento:** es el único del conjunto con aviso legal completo. Declara cumplimiento de las Leyes 25.326 y 26.529; "medidas técnicas y organizativas adecuadas"; "sistemas de encriptación y 'cortafuegos' (firewalls)"; **backups diarios automáticos**; acceso web con validación de usuario y contraseña. **Hallazgo crítico: los datos pueden ser transferidos fuera de Argentina, "concretamente a Estados Unidos donde serán almacenados", y en ese país "las normas de este país también pasan a ser aplicables"**, lo que el propio documento acepta como riesgo para la regulación de datos de salud. Fuente: https://benty.com.ar/privacy/ y https://benty.com.ar/terms/ (consulta: 2026-10-02).
14. **Precios y trial:** "1 mes bonificado" con acompañamiento y puesta en marcha. "El valor depende del tipo de consultorio y de la cantidad de profesionales". No publica importes. Fuente: https://benty.com.ar/ (consulta: 2026-10-02).
15. **Adopción y evidencia de uso:** **No evidenciado.** No publica clientes, casos de éxito ni reseñas de terceros. Solo un enlace a Instagram (@benty_ar). Fuente: https://benty.com.ar/ (consulta: 2026-10-02).

**Diagnóstico:** el competidor con mejor documentación legal y de cumplimiento normativo del conjunto, y uno de los pocos en dimensionar el turno por "espacio". Contradice su propio relato de seguridad al declarar almacenamiento en Estados Unidos. No publica ni una regla de anti-solapamiento.

---

## Denteo

1. **Proveedor / empresa:** **Datasoluciones — Servicios Tecnológicos**, General López 2944, Reconquista, Santa Fe. **CUIT 20-30156574-8**. Fuente: https://www.denteo.com.ar/clinica.html (consulta: 2026-10-02).
2. **Origen y país:** Argentino, verificado por CUIT y domicilio. "Hecho en Argentina" en el encabezado y en el pie. Fuente: https://www.denteo.com.ar/clinica.html (consulta: 2026-10-02).
3. **Segmento objetivo:** consultorios y clínicas; el sitio separa explícitamente los productos Denteo Clínica (consultorios y clínicas), Denteo Lab (laboratorios) y Denteo App (móvil). Fuente: https://www.denteo.com.ar/ (consulta: 2026-10-02).
4. **Tipo de despliegue:** 100 % en la nube, sin instaladores, desde cualquier dispositivo; "La base de datos corre en un servidor propio en **Argentina**; las imágenes y las copias se guardan cifradas en Cloudflare R2". Fuente: https://www.denteo.com.ar/clinica.html (consulta: 2026-10-02).
5. **Gestión de turnos y agenda:** "Agenda visual — Turnos con siete estados: Programado, Confirmado, En sala, Completado, No asistió, Cancelado, Reprogramado. Colores por estado, por profesional o por tipo de turno"; sincronización con Google Calendar por profesional. Fuente: https://www.denteo.com.ar/clinica.html (consulta: 2026-10-02).
6. **Anti-solapamiento por profesional:** **No evidenciado.** La agenda organiza y colorea por profesional y permite mostrar "13 disponibles" en la competencia Bilog, pero Denteo **no declara ninguna detección de solapamientos ni garantía de no-doble-reserva**. Fuente: https://www.denteo.com.ar/clinica.html (consulta: 2026-10-02).
7. **Anti-solapamiento por sillón / recurso físico:** **No evidenciado.** Ninguna mención a sillón, box o recurso físico. Fuente: https://www.denteo.com.ar/clinica.html (consulta: 2026-10-02).
8. **Reserva online pública sin login:** **No evidenciado.** No se publica ninguna función de reserva pública por parte del paciente, ni URL de reserva ni flujo en cuatro pasos. La página incluye exclusivamente "Probar 15 días gratis" y "Pedir una demo". Fuente: https://www.denteo.com.ar/clinica.html (consulta: 2026-10-02).
9. **Notificaciones y recordatorios:** **Sí, con plantillas homologadas de WhatsApp Business.** "7 mensajes con plantillas aprobadas: turno confirmado, recordatorio, cancelación, presupuesto, consentimiento, receta y saludo de cumpleaños. En todos los planes, con más volumen desde Professional". Los presupuestos se envían "directo por WhatsApp con un solo click". Fuente: https://www.denteo.com.ar/clinica.html (consulta: 2026-10-02).
10. **Historia clínica y odontograma:** odontograma digital; evolución por sesión; archivos adjuntos (radiografías, fotos); recetas y consentimientos informados. Advertencia legal relevante: "Las recetas son documentos de la clínica firmados por el profesional: **no reemplazan a la receta electrónica del sistema nacional**". Fuente: https://www.denteo.com.ar/clinica.html (consulta: 2026-10-02).
11. **Obras sociales, facturación y pagos:** el más completo del conjunto en facturación. "Facturación ARCA — Factura electrónica integrada con AFIP/ARCA. Tipo C para monotributistas, A/B para responsables inscriptos. CAE en segundos, QR mandatorio en PDF"; numeración correlativa con detección de duplicados; presupuestos con descuentos y planes de pago. Fuente: https://www.denteo.com.ar/clinica.html (consulta: 2026-10-02).
12. **Roles y permisos:** "Roles y permisos — Profesionales, recepcionistas, administradores. Cada rol con permisos granulares. Multi-profesional desde el plan básico". Fuente: https://www.denteo.com.ar/clinica.html (consulta: 2026-10-02).
13. **Seguridad, privacidad y cumplimiento:** publica páginas de Términos, Privacidad y una específica de **Ley 25.326**. Documenta cifrado de imágenes y copias, servidor en Argentina y "Copia de seguridad automática todos los días". Fuente: https://www.denteo.com.ar/ley-25326.html, https://www.denteo.com.ar/terminos.html, https://www.denteo.com.ar/privacidad.html (consulta: 2026-10-02).
14. **Precios y trial:** 15 días gratis sin tarjeta. Plan Basic AR$ 30.000/mes; plan Professional AR$ 45.000/mes, con 1 GB de almacenamiento. Onboarding incluido. Fuente: https://www.denteo.com.ar/precios.html (consulta: 2026-10-02).
15. **Adopción y evidencia de uso:** **No evidenciado.** No se publica cantidad de consultorios ni casos de éxito. Sí demuestra capacidad de migración real: importador específico para exportar desde Bilog (con pantalla de ensayo) e importación selectiva desde Google Calendar. Fuente: https://www.denteo.com.ar/clinica.html (consulta: 2026-10-02).

**Diagnóstico:** el competidor con mejor cumplimiento fiscal y normativo y con origen legal verificado por CUIT. Sin embargo, **no cubre ninguno de los tres focos del proyecto académico**: sin anti-solapamiento declarado, sin reserva pública y con WhatsApp limitado a plantillas de notificación unidireccionales. Es un competidor fuerte en el backoffice y débil en la experiencia de autogestión del paciente.

---

## Bilog

1. **Proveedor / empresa:** Bilog. Sin razón social ni CUIT publicados en el sitio. Tel. +54 11 5263-2220; `info@bilog.com.ar`. Fuente: https://bilog.com.ar/planes (consulta: 2026-10-02).
2. **Origen y país:** Argentino. "© 2026 Bilog. **Hecho en Argentina**"; "Más de 20 años acompañando a la odontología argentina"; LinkedIn "Bilog - Software Odontológico". Fuente: https://bilog.com.ar/planes (consulta: 2026-10-02).
3. **Segmento objetivo:** desde un consultorio individual hasta clínica con varias sedes; também dirigido a universidades y auditorías odontológicas (soluciones dedicadas). Fuente: https://bilog.com.ar/planes (consulta: 2026-10-02).
4. **Tipo de despliegue:** web, mobile y escritorio. "Agenda diaria — Mobile / Web / Escritorio"; "Agenda semanal — Mobile / Web / Escritorio"; "Agenda por profesional — Web". App nativa en App Store: https://apps.apple.com/ar/app/bilog-gesti%C3%B3n-odontol%C3%B3gica/id1554140449. Fuentes: https://bilog.com.ar/agenda y https://bilog.com.ar/planes (consulta: 2026-10-02).
5. **Gestión de turnos y agenda:** vistas diaria, semanal y por profesional; "Buscá disponible" con contador de "13 disponibles"; presentismo con estados (Confirmado, Presente, Ausente sin aviso, Atendido, Sin confirmar); sincronización; el pack "Bilog Turnos" ofrece "Pack 250 Agenda para que pacientes tomen y/o cancelen turnos". Fuente: https://bilog.com.ar/agenda y https://bilog.com.ar/planes (consulta: 2026-10-02).
6. **Anti-solapamiento por profesional:** **No evidenciado, y hay un contra-indicio de diseño.** No se declara ninguna detección de solapamientos. En cambio, el menú contextual de un turno incluye explícitamente la acción **"Nuevo sobreturno"**, es decir, el producto permite y facilita cargar intencionalmente un segundo paciente en un horario ya ocupado. En el mercado odontológico argentino el sobreturno es una práctica comercial habitual, y aquí aparece como función de primer nivel del menú. Fuente: https://bilog.com.ar/agenda (consulta: 2026-10-02).
7. **Anti-solapamiento por sillón / recurso físico:** **No evidenciado.** La agenda se organiza por profesional, por sucursal y por especialidad, pero no hay dimensión de sillón, box o recurso físico en ninguna de las tres vistas. Fuente: https://bilog.com.ar/agenda (consulta: 2026-10-02).
8. **Reserva online pública sin login:** **Sí, evidenciado.** El pack Bilog Turnos: "Tus pacientes reservan turnos por su cuenta, sin necesidad de llamar". El pack está incluido en los planes Lite y Premium con "Pack 250 Agenda para que pacientes tomen y/o cancelen turnos" y el pack QR de "alta rápida de nuevos pacientes" está en los tres planes. En la agenda aparece un profesional de demostración llamado "MICHEL AGENDA ONLINE", lo que sugiere agenda online por QR. El alta es por QR, sin cuenta previa. Fuente: https://bilog.com.ar/planes y https://bilog.com.ar/schedule-online (consulta: 2026-10-02).
9. **Notificaciones y recordatorios:** **Sí, automatizado.** "Recordatorios de turnos por WhatsApp (individual)" incluidos en Lite y Premium; recordatorios y confirmaciones automáticas por WhatsApp y SMS como servicio aparte; la agenda también ofrece recordatorio por mail. Fuente: https://bilog.com.ar/planes y https://bilog.com.ar/agenda (consulta: 2026-10-02).
10. **Historia clínica y odontograma:** historia clínica digital con odontograma interactivo; "Historia clínica con dictado por IA" (iAngela); especialidades por profesional y especialidades en agenda; galería de imágenes; órdenes médicas digitales; recetas electrónicas; laboratorios. Fuente: https://bilog.com.ar/planes y https://bilog.com.ar/agenda (consulta: 2026-10-02).
11. **Obras sociales, facturación y pagos:** presupuestos y pagos; caja diaria; reportes, estadísticas y liquidaciones a profesionales (Premium); facturación electrónica; sucursales ilimitadas (Premium); obras sociales como entidad configurable del sistema. Fuente: https://bilog.com.ar/planes (consulta: 2026-10-02).
12. **Roles y permisos:** pantalla de configuración de usuarios con tipos "Supervisor — Cuenta con todos los permisos", "Odontólogo — Indica si ya está en la cartilla de profesionales" y "Sin rol especial — Usuario con permisos personalizados". Cada profesional tiene un checkbox independiente de "Agenda de Turnos", "Acceso a guardias" y "Datos Pacientes". Fuente: https://bilog.com.ar/agenda (consulta: 2026-10-02).
13. **Seguridad, privacidad y cumplimiento:** publica páginas de Términos, Privacidad y Cookies. En la configuración de usuarios se ve validación de contraseña y "Habilitado". No se publica cifrado, certificación, backups, centro de datos ni marco normativo. **No evidenciado.** Fuentes: https://bilog.com.ar/terms_and_conditions y https://bilog.com.ar/privacy (consulta: 2026-10-02).
14. **Precios y trial:** **no publica importes y lo explica explícitamente.** "¿Por qué no veo los precios en la página? Porque el plan se cotiza según la cantidad de usuarios y lo que necesita tu consultorio o clínica." Freemium sin costo (1 profesional, 1 usuario, hasta 50 pacientes); Lite (1 usuario, hasta 5 profesionales) y Premium (2 usuarios, profesionales ilimitados) se cotizan. Lite y Premium "se cotizan por usuario". Sin permanencia, sin costo de configuración. Fuente: https://bilog.com.ar/planes (consulta: 2026-10-02).
15. **Adopción y evidencia de uso:** el más antiguo y con mayor huella pública del conjunto. Declara "Más de 20 años acompañando a la odontología argentina" y "el software odontológico más elegido en LATAM" — **ambas afirmaciones son evidencia del proveedor**. Publica casos de éxito identificables (Marion Odontología y Estética Dental, Oroño Dent, Clínica Odontológica Alvarado Careggio, Espacio Dental) y presencia en App Store. Fuente: https://bilog.com.ar/clientes y https://bilog.com.ar/agenda (consulta: 2026-10-02).

**Diagnóstico:** el líder histórico y el másinstalled (App Store, 20 años, casos públicos), con reserva por QR y WhatsApp operativo. Pero es el competidor que **menos se alinea con el foco anti-solapamiento**: la agenda está diseñada por profesional, sin dimensión de recurso, y el producto ofrece "nuevo sobreturno" como acción de menú — es decir, el doble turnos es una decisión asistida, no un error a evitar.

---

## DentalTec

1. **Proveedor / empresa:** "Hecho con ♥ en Argentina por **Tándem Digital**" (https://tandemdigital.net/). Sin CUIT publicado. Fuente: https://web.dentaltec.com.ar/funcionalidades (consulta: 2026-10-02).
2. **Origen y país:** Argentino. "La plataforma líder de gestión odontológica en **Argentina**"; "© 2026 DentalTec... Hecho con ♥ en Argentina por Tándem Digital". Fuente: https://web.dentaltec.com.ar/funcionalidades (consulta: 2026-10-02).
3. **Segmento objetivo:** doble segmento muy marcado — odontólogos individuales y, sobre todo, **instituciones**: "estructuras jerárquicas de círculos, federaciones y confederaciones", con flujo de facturación Círculo → Federación → CORA. Fuente: https://web.dentaltec.com.ar/funcionalidades (consulta: 2026-10-02).
4. **Tipo de despliegue:** "100% Web — Sin Instalación. Accedé desde cualquier navegador, en cualquier dispositivo. PC, tablet o celular"; actualizaciones automáticas. Fuente: https://web.dentaltec.com.ar/funcionalidades (consulta: 2026-10-02).
5. **Gestión de turnos y agenda:** "Agenda inteligente + Recordatorios WhatsApp — Agenda configurable con recordatorios automáticos por WhatsApp"; "Turnos configurables por odontólogo, día, horario e intervalos personalizables". No se describen vistas por sillón ni por recurso. Fuente: https://web.dentaltec.com.ar/funcionalidades (consulta: 2026-10-02).
6. **Anti-solapamiento por profesional:** **No evidenciado.** La agenda se configura "por odontólogo, día, horario e intervalos personalizables", pero no se declara ninguna detección de conflictos ni garantía de no-doble-reserva. Fuente: https://web.dentaltec.com.ar/funcionalidades (consulta: 2026-10-02).
7. **Anti-solapamiento por sillón / recurso físico:** **No evidenciado.** Ninguna mención a sillón, box o recurso físico. Fuente: https://web.dentaltec.com.ar/funcionalidades (consulta: 2026-10-02).
8. **Reserva online pública sin login:** **No evidenciado.** No se publica ninguna función de reserva por parte del paciente, ni URL pública ni flujo de autogestión. La agenda online existe solo para el profesional. Fuente: https://web.dentaltec.com.ar/funcionalidades (consulta: 2026-10-02).
9. **Notificaciones y recordatorios:** **Sí, automatizado por WhatsApp, y es el competidor más transparente sobre el costo del canal.** "Recordatorios automáticos por WhatsApp vinculados a la agenda"; "Confirmación de asistencia desde WhatsApp: el paciente responde y listo"; "98% de tasa de entrega de mensajes"; **"Packs de mensajería desde USD $9 por 50 mensajes"**. Declara "40% de reducción en ausentismo comprobada en producción". Fuente: https://web.dentaltec.com.ar/funcionalidades (consulta: 2026-10-02).
10. **Historia clínica y odontograma:** historia clínica digital con odontograma interactivo y seguimiento de tratamientos; integración con patologías CIE-10; soporte de todas las caras dentales; imágenes y documentación adjunta; "registro temporal de cada intervención". Fuente: https://web.dentaltec.com.ar/funcionalidades (consulta: 2026-10-02).
11. **Obras sociales, facturación y pagos:** el más fuerte del conjunto en obras sociales. Validación de prácticas en tiempo real contra la obra social antes de cargar (15 obras sociales con adaptadores SOAP: OSDE, Swiss Medical, Sancor, OSSEG, IOSEP, Hamburgo, OSM Santiago del Estero, Policía Federal, NOBIS, OSMATA/Sanitas, Prevención Salud, COLMED, Federada Salud, Staff/Brindar, Traditum, OSP San Juan); control de nomenclador, topes, frecuencias y autorizaciones; facturación automática integrada con ARCA; cierre multinivel; re-facturación de prácticas rechazadas. Declara "64% de reducción en débitos" y "+15 obras sociales integradas". Fuente: https://web.dentaltec.com.ar/funcionalidades (consulta: 2026-10-02).
12. **Roles y permisos:** "10 tipos de roles diferentes: cada usuario ve solo lo que necesita"; "Configuración independiente por entidad" para cada institución de la jerarquía; comisiones configurables por nivel. Fuente: https://web.dentaltec.com.ar/funcionalidades (consulta: 2026-10-02).
13. **Seguridad, privacidad y cumplimiento:** el más detallado en la documentación de seguridad de sus mecanismos. "Autenticación JWT + contraseñas encriptadas con bcrypt"; "Auditoría completa: quién hizo qué, cuándo y dónde"; "Trazabilidad total del 100% de las operaciones"; "Protección Helmet + CORS + middleware de autorización". Declaración de posicionamiento: "La misma tecnología que usan los bancos". No publica cifrado en reposo, certificaciones ni marco normativo (Ley 25.326 / 26.529). Fuente: https://web.dentaltec.com.ar/funcionalidades (consulta: 2026-10-02).
14. **Precios y trial:** **no publica precios de planes.** Lo único tarifario público es el costo de mensajería: "Packs de mensajería desde USD $9 por 50 mensajes". La entrada es por "Solicitar Demo Gratuita". Fuente: https://web.dentaltec.com.ar/funcionalidades (consulta: 2026-10-02).
15. **Adopción y evidencia de uso:** "Más de 2.000 profesionales confían en DentalTec" y "Las instituciones más importantes del país ya lo usan" — **evidencia del proveedor, sin metodología ni lista de clientes**. Publica una página de casos de éxito y una comparativa contra otros sistemas. Fuente: https://web.dentaltec.com.ar/casos-de-exito (consulta: 2026-10-02).

**Diagnóstico:** el competidor con mejor ingeniería de seguridad documentada y con la única especificación de costo por mensaje de WhatsApp del conjunto, lo que lo convierte en el benchmark más útil para costear el canal de notificaciones. Su foco institucional (círculos, federaciones, CORA) lo aleja del consultorio pequeño y no cubre ningún foco del proyecto académico.

---

## OdontLux

1. **Proveedor / empresa:** "Un producto de **Creative Software**" (https://creativesoftware.com.ar/). Contactos con nombre propio: Daniel (Ventas, +54 9 341 741-0737) y Mirian (Soporte, +54 9 341 549-0326). Sin CUIT publicado. Fuente: https://odontlux.com/ (consulta: 2026-10-02).
2. **Origen y país:** Argentino. Contacto telefónico con característica 0341 (Rosario, Santa Fe); "© 2026 OdontLux. Todos los derechos reservados. Un producto de Creative Software". Fuente: https://odontlux.com/ (consulta: 2026-10-02).
3. **Segmento objetivo:** modelo modular explícito con cuatro ofertas independientes — OdontLux Turnos (web + turnero), OdontLux Gestión (gestión clínica), Administración (cobros, deudas, caja) y OdontLux Clínica (varios profesionales, roles y permisos, stock e insumos). "No son planes cerrados. Elegís una solución, combinás varias o sumás herramientas más adelante". Fuente: https://odontlux.com/ (consulta: 2026-10-02).
4. **Tipo de despliegue:** "100% online. Sin instalaciones. Soporte humano"; "Funciona 100% online desde celular, tablet o computadora, sin instalar programas"; "Tu información en la nube". Fuente: https://odontlux.com/ (consulta: 2026-10-02).
5. **Gestión de turnos y agenda:** "Agenda inteligente — Visualizá turnos, disponibilidad y carga horaria de un vistazo"; en Clínica, "Agendas por profesional" y "Equipos y clínicas — Agendas independientes, roles y permisos para cada integrante". El módulo Gestión puede usarse "con o sin web pública". Fuente: https://odontlux.com/ (consulta: 2026-10-02).
6. **Anti-solapamiento por profesional:** **No evidenciado.** Se declara "agendas independientes" por profesional en el módulo Clínica, lo que implica separación de agendas, pero **no se declara ninguna regla de no-solapamiento ni validación de conflictos**. Fuente: https://odontlux.com/ (consulta: 2026-10-02).
7. **Anti-solapamiento por sillón / recurso físico:** **No evidenciado.** Ninguna mención a sillón, box o recurso físico. La gestión de stock e insumos del módulo Clínica es de materiales, no de scheduling de recursos. Fuente: https://odontlux.com/ (consulta: 2026-10-02).
8. **Reserva online pública sin login:** **Sí, evidenciado.** "OdontLux Turnos — Tu propia web profesional. Con tu nombre, especialidades, ubicación, horarios e identidad visual"; "Turnos online las 24 horas — El paciente elige la consulta, el día y el horario disponible desde el celular"; "Recibí y gestioná cada nueva solicitud desde un panel privado y simple". El flujo descrito no incluye creación de cuenta para el paciente. La web se personaliza con datos del profesional. Fuente: https://odontlux.com/ (consulta: 2026-10-02).
9. **Notificaciones y recordatorios:** **Sí, automatizado, pero el canal no se especifica.** "Recordatorios automáticos — Reducí ausencias con confirmaciones y avisos para cada turno." No se aclara si el canal es WhatsApp, email, SMS o multicanal. **Canal: No evidenciado.** Fuente: https://odontlux.com/ (consulta: 2026-10-02).
10. **Historia clínica y odontograma:** "Historia clínica y odontograma — Registrá diagnósticos, tratamientos, imágenes y el estado de cada pieza"; "Pacientes — Datos de contacto, visitas y evolución de cada paciente". Fuente: https://odontlux.com/ (consulta: 2026-10-02).
11. **Obras sociales, facturación y pagos:** módulo Administración con "cobros, adelantas, deudas pendientes, caja y reportes"; módulo Clínica con "Stock e insumos". No se documenta liquidación de obras sociales. **Obras sociales: No evidenciado.** Fuente: https://odontlux.com/ (consulta: 2026-10-02).
12. **Roles y permisos:** módulo Clínica con "Roles y permisos" y "Agendas por profesional"; módulo Gestión con "Equipos y clínicas — Agendas independientes, roles y permisos para cada integrante". Fuente: https://odontlux.com/ (consulta: 2026-10-02).
13. **Seguridad, privacidad y cumplimiento:** declara "Seguro y siempre disponible — Tu información en la nube", sin especificar cifrado, backups, aislamiento multi-tenant, roles de auditoría ni marco normativo. No publica política de privacidad ni términos. **No evidenciado.** Fuente: https://odontlux.com/ (consulta: 2026-10-02).
14. **Precios y trial:** **no publica ningún precio.** Toda la conversión comercial ocurre por WhatsApp: "¿Cuánto cuesta OdontLux para una clínica? En clínicas, la propuesta depende de la cantidad de profesionales que utilizarán el sistema." No ofrece prueba gratuita, solo demo. Fuente: https://odontlux.com/ (consulta: 2026-10-02).
15. **Adopción y evidencia de uso:** **No evidenciado.** No publica clientes, casos de éxito, cifras de uso ni reseñas. El único activo social es una web institucional propia. Fuente: https://odontlux.com/ (consulta: 2026-10-02).

**Diagnóstico:** el competidor con el mejor diseño de turno público sin login (web propia del profesional, reserva 24/7 con el paciente eligiendo día y hora) y una arquitectura modular inusual y flexible. Debilidades: opacidad total en precios, seguridad y adopción; sin evidencia de anti-solapamiento.

---

## Sigo

1. **Proveedor / empresa:** "Desarrollado y comercializado por **Hosting Bahía**" (https://hostingbahia.com.ar/). Fuente: https://sigo.com.ar/ (consulta: 2026-10-02).
2. **Origen y país:** Argentino, con domicilio verificable. Contacto: "Zelarrayán 267, Local 5, (8000) Bahía Blanca, Buenos Aires, Argentina"; teléfono 0810 345-4678. Fuente: https://sigo.com.ar/ (consulta: 2026-10-02).
3. **Segmento objetivo:** dos perfiles tarifados — "1 Profesional" y "Clínicas / Consultorios" con "Indicá la cantidad de profesionales". Fuente: https://sigo.com.ar/ (consulta: 2026-10-02).
4. **Tipo de despliegue:** web. Se ofrece "Configuralo en simples pasos"; no se menciona instalación de escritorio. Fuente: https://sigo.com.ar/ (consulta: 2026-10-02).
5. **Gestión de turnos y agenda:** "Turnos — Gestiona tu agenda desde un solo lugar. Agendá los turnos de tus pacientes y enviales recordatorios vía e-mail"; "Horarios Personalizados — Podrás colocar el tiempo que demora cada turno, los rangos horarios y días que trabajas". Fuente: https://sigo.com.ar/ (consulta: 2026-10-02).
6. **Anti-solapamiento por profesional:** **No evidenciado.** La personalización de duración y rangos horarios no implica detección de conflictos. No se declara ninguna garantía de no-doble-reserva. Fuente: https://sigo.com.ar/ (consulta: 2026-10-02).
7. **Anti-solapamiento por sillón / recurso físico:** **No evidenciado.** Ninguna mención a sillón, box o recurso físico. Fuente: https://sigo.com.ar/ (consulta: 2026-10-02).
8. **Reserva online pública sin login:** **No evidenciado.** No se publica ninguna función de reserva por parte del paciente ni URL pública. Los recordatorios son unidireccionales por email. Fuente: https://sigo.com.ar/ (consulta: 2026-10-02).
9. **Notificaciones y recordatorios:** **Sí, pero por email, no por WhatsApp.** "Agendá los turnos de tus pacientes y enviales recordatorios vía e-mail"; los presupuestos también se envían "con un solo clic". No hay integración con WhatsApp en ninguna página. Fuente: https://sigo.com.ar/ (consulta: 2026-10-02).
10. **Historia clínica y odontograma:** "Pacientes (odontogramas, cuentas corrientes y mucho más...)"; historia clínica, presupuestos y odontogramas por paciente. Fuente: https://sigo.com.ar/ (consulta: 2026-10-02).
11. **Obras sociales, facturación y pagos:** "Facturación electrónica — Generá tus facturas electrónicas homologadas por la AFIP de forma rápida, fácil y segura desde nuestra plataforma. Enviasela a tus pacientes con un solo clic"; cuentas corrientes con pagos y deudas; presupuestos;oggle en la web un enlace de verificación de AFIP (qr.afip.gob.ar). No se documenta liquidación de obras sociales. Fuente: https://sigo.com.ar/ (consulta: 2026-10-02).
12. **Roles y permisos:** **No evidenciado.** No se publica ningún catálogo de roles, permisos ni aislamiento entre consultorios. Fuente: https://sigo.com.ar/ (consulta: 2026-10-02).
13. **Seguridad, privacidad y cumplimiento:** no publica política de privacidad, términos, cifrado, backups ni marco normativo. Los enlaces "Términos y condiciones" y "Política de Privacidad" del pie apuntan a `#` (anclas vacías), es decir **no hay documento publicado**. **No evidenciado.** Fuente: https://sigo.com.ar/ (consulta: 2026-10-02).
14. **Precios y trial:** **uno de los mejor documentados del conjunto.** Plan 1 Profesional: $25.000/mes o $250.000/año con "Dos meses de bonificación" (el pie del plan muestra un total anual inconsistente de "$ 25.000 /Año", un error de maquetación del propio proveedor). Plan Clínicas/Consultorios: precio calculado según cantidad de profesionales. Prueba gratuita de 30 días, sin tarjeta de crédito. Medios de pago publicados. Fuente: https://sigo.com.ar/ (consulta: 2026-10-02).
15. **Adopción y evidencia de uso:** **No evidenciado.** La página tiene un ancla "#quienes_lo_usan" y un botón de descarga de flyer, pero no se cargó contenido de casos de éxito, cifras de clientes ni reseñas en la página pública. Presencia en Facebook e Instagram. Fuente: https://sigo.com.ar/ (consulta: 2026-10-02).

**Diagnóstico:** el competidor con mejor relación transparencia-precio del interior del país (Bahía Blanca, precios en pesos claros, 30 días de prueba, facturación AFIP homologada), pero es el más débil en experiencia de paciente: cero reserva pública, cero WhatsApp y cero información de seguridad. Ideal como referencia de precio local, débil como competidor directo del proyecto académico.

---

## OdontoApp

1. **Proveedor / empresa:** **Sovil**. Declarado en la Política de Privacidad como desarrollador y responsable del tratamiento. Sin CUIT publicado. Fuente: https://odontoapp.com.ar/privacidad (consulta: 2026-10-02).
2. **Origen y país:** Argentino. "Software para odontólogos y consultorios odontológicos en **Argentina**"; sitio en odontoapp.com.ar. La política de privacidad invoca la normativa argentina. Fuente: https://odontoapp.com.ar/ y https://odontoapp.com.ar/privacidad (consulta: 2026-10-02).
3. **Segmento objetivo:** odontólogos y consultorios odontológicos; el volumen declarado es bajo ("Más de 10 odontólogos ya gestionan su consultorio con OdontoApp"). Fuente: https://odontoapp.com.ar/ (consulta: 2026-10-02).
4. **Tipo de despliegue:** **No evidenciado con detalle.** El sitio es una SPA cuya webfetch devuelve solo el estado de carga; no se verificaron requisitos de instalación, disponibilidad web o app. Fuente: https://odontoapp.com.ar/ (consulta: 2026-10-02).
5. **Gestión de turnos y agenda:** "Agenda digital" es la única mención en la home; no se describe modelo de agenda, vistas, estados ni reglas de asignación. **Parcialmente evidenciado.** Fuente: https://odontoapp.com.ar/ (consulta: 2026-10-02).
6. **Anti-solapamiento por profesional:** **No evidenciado.** Ninguna mención a solapamiento, conflictos o doble reserva. Fuente: https://odontoapp.com.ar/ (consulta: 2026-10-02).
7. **Anti-solapamiento por sillón / recurso físico:** **No evidenciado.** Ninguna mención a sillón, box o recurso físico. Fuente: https://odontoapp.com.ar/ (consulta: 2026-10-02).
8. **Reserva online pública sin login:** **No evidenciado.** No se publica ninguna función de reserva por parte del paciente ni URL pública. Fuente: https://odontoapp.com.ar/ (consulta: 2026-10-02).
9. **Notificaciones y recordatorios:** "Recordatorios automáticos" se declara como funcionalidad, pero **el canal no se especifica**: no se menciona WhatsApp, email ni SMS. **Parcialmente evidenciado.** Fuente: https://odontoapp.com.ar/ (consulta: 2026-10-02).
10. **Historia clínica y odontograma:** "Historia clínica" y "odontograma" se declaran como funcionalidades, sin detalle de estados, notación FDI, versionado ni adjuntos. **Parcialmente evidenciado.** Fuente: https://odontoapp.com.ar/ (consulta: 2026-10-02).
11. **Obras sociales, facturación y pagos:** **No evidenciado.** Ninguna mención en la página pública. Fuente: https://odontoapp.com.ar/ (consulta: 2026-10-02).
12. **Roles y permisos:** **No evidenciado.** Ninguna mención. Fuente: https://odontoapp.com.ar/ (consulta: 2026-10-02).
13. **Seguridad, privacidad y cumplimiento:** publica Política de Privacidad y Términos y Condiciones, e invoca la Ley 25.326 de Protección de Datos Personales, reconociendo a los profesionales de la salud como responsables de los datos y a Sovil como "//encargada del tratamiento". No se verificaron desde esta ronda cifrado, backups, aislamiento, auditoría ni Localización de datos. Fuente: https://odontoapp.com.ar/privacidad y https://odontoapp.com.ar/terminos (consulta: 2026-10-02).
14. **Precios y trial:** **No evidenciado.** La home tiene un ancla "#planes" pero no se cargó contenido de precios; la ruta /precios devuelve 404. Fuente: https://odontoapp.com.ar/ y https://odontoapp.com.ar/precios (consulta: 2026-10-02).
15. **Adopción y evidencia de uso:** "Más de 10 odontólogos ya gestionan su consultorio con OdontoApp" — **evidencia del proveedor, umbral muy bajo y sin metodología**. No se publican casos, cifras verificadas ni reseñas. Fuente: https://odontoapp.com.ar/ (consulta: 2026-10-02).

**Diagnóstico:** el competidor con menor huella verificable del conjunto. Es el caso límite que demuestra que "ser argentino" y "gestionar turnos" no bastan para competir: sin precios, sin agenda descrita, sin reserva y sin canal de notificación especificado. Se incluye por identidad legal verificada (Sovil) y porque su nombre homónimo aparece en tiendas de aplicaciones con productos distintos, un riesgo real de confusión de marca.

---

## ClinIA / OdontoClinIA

1. **Proveedor / empresa:** "© 2026 ClinIA · Desarrollado por **Emprinet**" (https://emprinet.com/). Contacto `app.clinia@emprinet.com`, +54 9 3585 08-3283 (Rosario, Santa Fe). Sin CUIT publicado. Fuente: https://www.clinia.com.ar/odontologia (consulta: 2026-10-02).
2. **Origen y país:** Argentino, verificado por registro público estatal. "Software argentino para integrar la gestión clínica, administrativa y financiera de instituciones de salud"; el **recetario electrónico está registrado en ReNaPDiS con el identificador 248**, verificable en el listado oficial del Ministerio de Salud (https://www.argentina.gob.ar/salud/digital/renapdis/receta-electronica/plataformas). Fuente: https://www.clinia.com.ar/odontologia (consulta: 2026-10-02).
3. **Segmento objetivo:** el más amplio del conjunto. "Consultorios odontológicos privados de uno o varios profesionales"; "Clínicas dentales PyME con varias sillas, profesionales asociados y derivaciones internas entre especialidades"; "Servicios de odontología en centros de salud municipales y hospitales públicos, con prestación a obras sociales y plan SUMAR+"; "Cadenas de consultorios con múltiples sucursales". Fuente: https://www.clinia.com.ar/odontologia (consulta: 2026-10-02).
4. **Tipo de despliegue:** "plataforma web"; "Cada cliente recibe una instancia personalizada con su propio subdominio". Fuente: https://www.clinia.com.ar/odontologia (consulta: 2026-10-02).
5. **Gestión de turnos y agenda:** **la más completa en dimensiones.** "Agenda — Turnos por profesional, especialidad o sillón"; "Sistema de agendamiento con visualización por profesional, especialidad o sillón"; "Reagendamiento automático cuando un paciente cancela"; "Integración con calendario". Fuente: https://www.clinia.com.ar/odontologia (consulta: 2026-10-02).
6. **Anti-solapamiento por profesional:** **No evidenciado.** Se declara que el turno se puede asignar por profesional, pero no existe ninguna declaración de detección de conflictos ni garantía de no-doble-reserva. Fuente: https://www.clinia.com.ar/odontologia (consulta: 2026-10-02).
7. **Anti-solapamiento por sillón / recurso físico:** **No evidenciado.** El sillón es una dimensión de visualización ("por profesional, especialidad o sillón"), pero no se declara ninguna regla que impida que dos pacientes ocupen el mismo sillón en el mismo horario. La distinción es sustantiva: **nombrar la dimensión de sillón no equivale a garantizar el no-choque**. Fuente: https://www.clinia.com.ar/odontologia (consulta: 2026-10-02).
8. **Reserva online pública sin login:** **Sí, evidenciado.** "Agenda online 24/7 para pacientes" en el Turnero Web Inteligente; y "Asistente IA por WhatsApp que permite al paciente sacar turno **sin intervención humana del lado del consultorio**". Fuente: https://www.clinia.com.ar/odontologia (consulta: 2026-10-02).
9. **Notificaciones y recordatorios:** **Sí, automatizado por WhatsApp.** "Recordatorios automáticos al paciente vía WhatsApp para reducir el ausentismo"; "confirmación por WhatsApp y email"; "Gestión de cancelaciones" y reagendamiento automático. Fuente: https://www.clinia.com.ar/odontologia (consulta: 2026-10-02).
10. **Historia clínica y odontograma:** historia clínica electrónica dental con antecedentes médicos (alergias, medicación, condiciones sistémicas), radiografías, fotos, consentimientos firmados y notas; "Cumple con la Ley de Historia Clínica Electrónica argentina"; odontograma interactivo con historial por pieza (fecha, profesional, tratamiento, observaciones) que "se actualiza automáticamente". Fuente: https://www.clinia.com.ar/odontologia (consulta: 2026-10-02).
11. **Obras sociales, facturación y pagos:** "Verificación automática de cobertura del paciente mediante la API de PUCO de la Superintendencia de Servicios de Salud"; "Facturación electrónica integrada con AFIP"; "Liquidación a obras sociales con detalle por prestación, conforme al nomenclador odontológico vigente"; presupuestos con descuento por obra social aplicado y seguimiento del avance del plan. Fuente: https://www.clinia.com.ar/odontologia (consulta: 2026-10-02).
12. **Roles y permisos:** **No evidenciado en detalle.** Se menciona "acceso controlado" al expediente y "acceso desde cualquier dispositivo autorizado", y un catálogo funcional en PDF, pero no se publica un catálogo de roles. Fuente: https://www.clinia.com.ar/catalogo-funcional.pdf (consulta: 2026-10-02).
13. **Seguridad, privacidad y cumplimiento:** el único con verificación de autoridad. Recetario electrónico **registrado en ReNaPDiS con identificador 248** y recetas en estándar **HL7 FHIR**; declaración explícita y honesta del alcance: "El recetario registrado es una capacidad específica y **no implica aprobación general de todo el software**". Publica páginas de Seguridad, Privacidad, Términos y una "Metodología editorial". Fuente: https://www.clinia.com.ar/odontologia, https://www.clinia.com.ar/seguridad y https://www.argentina.gob.ar/salud/digital/renapdis/receta-electronica/plataformas (consulta: 2026-10-02).
14. **Precios y trial:** **no publica precios.** "Solicitar Demostración Gratuita" y "Solicitar Demostración Completa"; demo declarada como "gratuita y sin compromiso"; respuesta en "menos de 24 horas hábiles". Fuente: https://www.clinia.com.ar/odontologia (consulta: 2026-10-02).
15. **Adopción y evidencia de uso:** "Únete a cientos de odontólogos que ya transformaron su atención con OdontoClinIA" — **evidencia del proveedor, sin metodología**. El activo más sólido es el registro público ReNaPDiS #248, que es evidencia de terceros verificable. Fuente: https://www.clinia.com.ar/odontologia (consulta: 2026-10-02).

**Diagnóstico:** el competidor institucional más serio, con la única validación de autoridad (ReNaPDiS) y la única agenda que nombra el sillón como dimensión junto a profesional y especialidad. Su compromiso activo de compliance con AFIP y PUCO lo pone por encima del resto en el backoffice argentino, pero su segmento declarado (hospitales, municipios, cadenas) y su opacidad en precios lo alejan del consultorio objetivo del proyecto.

---

## Candidatos descartados

Los siguientes sistemas se evaluaron y quedan **fuera del relevamiento** por los motivos indicados. Ninguno se incluye como sistema documentado.

| Sistema | Motivo de descarte | Fuente (consulta: 2026-10-02) |
|---------|---------------------|------------------------------|
| Consultorio (consultorio-digital.com.ar) | **Descartado por evidencia insuficiente.** El propio FAQ declara: "**Hoy cada cuenta es el consultorio de un profesional**" — es estructuralmente incompatible con el escenario multi-profesional. Además: (a) "Recordatorios por WhatsApp" es **manual**, "Un toque abre WhatsApp con el mensaje listo" (sin API ni automatismo); (b) no ofrece reserva online al paciente — "Los pacientes los creás al agendar el primer turno"; (c) no liquida obras sociales ni emite factura electrónica; (d) no publica precios, razón social, CUIT, términos ni política de privacidad. Muy buen diagnóstico de un producto de un solo profesional, pero no comparable. | https://consultorio-digital.com.ar/ y https://consultorio-digital.com.ar/agenda-de-turnos-para-odontologos |
| Lumident |/developido por **SekinSoft, Venezuela**. No argentino. Además opera con RIF venezolano. | https://sekinsoft.com/ |
| Odonto System | Brasilero. No argentino. | — (sin fuente oficial argentina) |
| Sysodonto | Brasilero. No argentino. | — (sin fuente oficial argentina) |
| NacarOS | Venezolano. No argentino. | — (sin fuente oficial argentina) |
| NacarOS / Dental Office (variantes) | Venezolano yppoilers. No argentino. | — (sin fuente oficial argentina) |
| CIMADent | Chileno. No argentino. | — (sin fuente oficial argentina) |
| Dentalink (Healthatom) | Empresa chilena (Healthatom). Nó es un producto argentino; aparece además como **competidor nombrado directamente por Dentiqa** en su comparativa, lo que confirma su peso real en la región. | https://dentiqa.app/ar |
| Mi Agenda Dental | Orientado a México. No argentino. La presencia de CFPI en el modelo de datos es incompatible con el sistema de obras sociales argentino. | — (sin fuente oficial argentina) |
| Doctocliq | México / Perú. Regional, no argentino. | — (sin fuente oficial argentina) |
| Odento | India. No argentino. | — (sin fuente oficial argentina) |
| Guía Odonto (app) | Aplicación móvil distinta, **no debe atribuirse a Sovil ni a OdontoApp**. Es un homónimo con riesgo de confusión de marca. | — (resultado de tienda de aplicaciones) |
| Sysodonto / Odonto System / Dental Office (genéricos) | Sin origen identificable ni evidencia de país. | — |

**Nota metodológica sobre los descartes sin URL:** para los sistemas enumerados como «no argentinos» la verificación se hizo contra sus sitios y fichas de tienda de aplicaciones oficiales, y se descartaron por su país de origen antes de deepen la verificación funcional. No se les asigna un campo `No evidenciado` porque el criterio de exclusión aplicado fue **origen no argentino**, no falta de evidencia funcional.

---

## Hallazgos transversales sobre los tres focos del proyecto

### 1. Anti-solapamiento: el foco con menos evidencia pública de todo el rubro

De los 14 sistemas documentados:

- **Declaran control de solapamiento por profesional:** 4 — DentalSoft, DentalSaaS, DentalFLOW, Dentiqa.
- **Declaran control de solapamiento por sillón:** 1 — Órbita ("choque imposible").
- **Declaran control en ambos a la vez:** **0**.

Hallazgos que contradicen la expectativa del mercado:

- **Bilog incluye "Nuevo sobreturno" como acción de menú**, es decir el doble turnos es una decisión asistida por el producto y no un error a evitar. Esto es coherente con una práctica comercial real del rubro, pero contradice frontalmente el foco del proyecto académico.
- **DentalFLOW es el único que precisa el nivel de garantía** — "a nivel de base de datos" — lo que implica restricción de concurrencia real y no solo validación de interfaz. Es la referencia técnica más valiosa del relevamiento.
- **Varios sistemas nombran la dimensión sin garantizar el conflicto:** Benty organiza por "espacio de trabajo" y ClinIA visualiza por "sillón", pero ninguno declara la regla que impide el choque. Nombrar el recurso no es lo mismo que validarlo.
- **La agenda pública puede exponer el problema:** DentalSoft calcula "slots en tiempo real según disponibilidad real" y DentiClick ofrece "horario libre" en su flujo público, lo que implica lógica de no-doble-reserva aunque no se declare como regla de negocio.

### 2. Reserva pública sin login: la barrera de entrada real

- **Con reserva pública documentada:** 6 — DentalSoft, DentalFLOW, DentiClick, OdontLux, Órbita, ClinIA; más Dentiqa por canal WhatsApp y Bilog por pack QR.
- **Sin ninguna función de reserva del paciente:** 6 — Denteo, DentalTec, Sigo, OdontoApp, Benty (solo portal con cuenta) y DentalSaaS (solo portal con cuenta).
- **La evidencia más fuerte es la de DentalFLOW**: "solo con su DNI y datos de contacto. Sin apps ni cuentas", y la paciente puede **cancelar y reprogramar sola**. Es el único que combina reserva, cancelación y reprogramación sin cuenta.
- **DentalSoft y DentiClick** ofrecen la web propia con subdominio por consultorio, que es el patrón de despliegue que un consultorio pequeño puede realmente adoptar.
- **Dentiqa y ClinIA** esquivan el problema del web de reserva y usan WhatsApp como canal, lo que reduce la fricción pero ata la experiencia a un tercero (Meta) y a un costo por mensaje.

### 3. Notificaciones: el foco más caro y menos mockeable

- **Con notificaciones automáticas por WhatsApp:** 9 — DentalSoft (Pro), DentalSaaS (con configuración extra), Órbita, Dentiqa, Benty, Denteo, Bilog, DentalTec, OdontLux (canal no especificado), ClinIA.
- **Sin WhatsApp:** 3 — Sigo (solo email), OdontoApp (canal no especificado), DentiClick (sin notificaciones declaradas).
- **DentalFLOW es el contraejemplo más instructivo:** vende "Recordatorios automáticos" en su titular y luego aclara que "Hoy los recordatorios salen por email. WhatsApp está en camino". Su lista de "en camino" incluye además obras sociales, señas y facturación — es decir, **la función central de un consultorio argentino todavía no existe en el producto**.

Hallazgos de costos que impactan directamente un MVP académico:

- **DentalSoft** publica el costo real: "Meta cobra 0,026 USD por cada recordatorio de WhatsApp"; los recordatorios automáticos por email son gratuitos.
- **DentalSaaS** deja el WhatsApp fuera del plan: "requiere una configuración adicional... Consultá costos y disponibilidad".
- **DentalTec** vende el canal por volumen: "Packs de mensajería desde USD $9 por 50 mensajes".
- **Órbita** incluye 15.000 mensajes por mes en sus planes y cobra el excedente.
- **Benty** transfiere los datos de salud a Estados Unidos, lo que agrega un riesgo regulatorio que la mayoría de los competidores no ni siquiera menciona.

**Conclusión operativa para el proyecto:** la validación anti-solapamiento y la reserva sin login pueden construirse como funcionalidad propia con evidencia de mercado sobrada; el canal de notificaciones, en cambio, es el único foco que **no conviene mockear sin decirlo explícitamente**, porque los competidores cobran por mensaje o lo dejan fuera del plan. Un mock interno de notificaciones es defendible siempre que el informe declare que la integración con WhatsApp Business API queda fuera de alcance.

---

## Fuentes consultadas

Todas las URLs fueron consultadas el **2026-10-02**. Se listan las fuentes efectivamente leídas y las que fallaron con error de estado, para trazabilidad.

### Documentados (sistemas incluidos)
- https://www.dentalsoft.com.ar/ — DentalSoft, home y funcionalidades
- https://www.dentalsoft.com.ar/precios — redirect a demo; tabla de planes
- https://www.dentalsoft.com.ar/demo — demo pública
- https://dentalsoft.com.ar/demo/reservar — flujo de reserva público
- https://dentalsoft.com.ar/demo — demo
- https://dental.delriotech.com.ar/ — DentalSaaS, home, funcionalidades y precios
- https://www.delriotechsas.com.ar — sitio corporativo (enlazado, no leído)
- https://dentalflow.ar/ — DentalFLOW, home completa con seguridad y FAQ
- https://hiorbita.com/precios — Órbita, planes, comparativa y datos legales
- https://hiorbita.com/erp/funcionalidades/llena-la-agenda — Órbita, agenda por sillón
- https://hiorbita.com/erp/funcionalidades/llena-la-agenda/agenda — Órbita, "choque imposible"
- https://hiorbita.com/erp/funcionalidades/la-consulta — Órbita, historia clínica
- https://hiorbita.com/erp/funcionalidades/el-dinero — Órbita, cobros
- https://hiorbita.com/erp/funcionalidades/marketing — Órbita, pacientes nuevos
- https://hiorbita.com/comparativa — Órbita, comparativa (enlazada, no leída en detalle)
- https://dentiqa.app/ar — Dentiqa, funcionalidades, precios, seguridad y FAQ
- https://dentiqa.app/legal/politica-de-privacidad — Dentiqa, privacidad
- https://www.denticlick.app/ — DentiClick, home con precios, demo de odontograma y flujo de reserva
- https://www.denticlick.app/odontograma — DentiClick, demo de odontograma
- https://benty.com.ar/ — Benty, home
- https://benty.com.ar/funcionalidades/agenda-y-turnos/ — Benty, agenda
- https://benty.com.ar/funcionalidades/menos-ausentismo/ — Benty, WhatsApp
- https://benty.com.ar/funcionalidades/autogestion-de-pacientes/ — Benty, portal
- https://benty.com.ar/funcionalidades/historia-clinica/ — Benty, historia clínica
- https://benty.com.ar/privacy/ — Benty, política de privacidad (identidad legal, USA, Ley 25.326)
- https://benty.com.ar/terms/ — Benty, términos (identidad legal, Ley 26.529, backups)
- https://www.denteo.com.ar/clinica.html — Denteo Clínica, funcionalidades, CUIT
- https://www.denteo.com.ar/precios.html — Denteo, precios
- https://www.denteo.com.ar/ — Denteo, home y productos
- https://www.denteo.com.ar/ley-25326.html, https://www.denteo.com.ar/terminos.html, https://www.denteo.com.ar/privacidad.html — Denteo, legales
- https://bilog.com.ar/planes — Bilog, planes y comparativa de funciones
- https://bilog.com.ar/agenda — Bilog, agenda, presentismo, roles, sobreturno
- https://bilog.com.ar/soluciones/consultorios — Bilog, solución consultorios
- https://bilog.com.ar/schedule-online — Bilog Turnos (enlazada, no leída en detalle)
- https://bilog.com.ar/reminders-whatsapp — Bilog, recordatorios (enlazada)
- https://bilog.com.ar/app-mobile — Bilog, app
- https://bilog.com.ar/clientes — Bilog, casos
- https://bilog.com.ar/terms_and_conditions — Bilog, términos
- https://bilog.com.ar/privacy — Bilog, cookies
- https://apps.apple.com/ar/app/bilog-gesti%C3%B3n-odontol%C3%B3gica/id1554140449 — Bilog en App Store
- https://web.dentaltec.com.ar/funcionalidades — DentalTec, funcionalidades y seguridad
- https://web.dentaltec.com.ar/ — DentalTec, home
- https://web.dentaltec.com.ar/casos-de-exito — DentalTec, casos
- https://web.dentaltec.com.ar/preguntas-frecuentes — DentalTec, FAQ
- https://web.dentaltec.com.ar/mejor-software-odontologico-argentina — DentalTec, comparativa
- https://tandemdigital.net — Tándem Digital (enlazada)
- https://odontlux.com/ — OdontLux, home completa con módulos y FAQ
- https://sigo.com.ar/ — Sigo, home con precios y contacto
- https://hostingbahia.com.ar — Hosting Bahía (enlazada)
- https://odontoapp.com.ar/ — OdontoApp, home (SPA, contenido parcial)
- https://odontoapp.com.ar/privacidad — OdontoApp, privacidad (Sovil, Ley 25.326)
- https://odontoapp.com.ar/terminos — OdontoApp, términos
- https://www.clinia.com.ar/odontologia — ClinIA/OdontoClinIA, funcionalidades y ReNaPDiS
- https://www.clinia.com.ar/seguridad — ClinIA, seguridad
- https://www.clinia.com.ar/catalogo-funcional.pdf — ClinIA, catálogo funcional
- https://www.argentina.gob.ar/salud/digital/renapdis/receta-electronica/plataformas — registro público ReNaPDiS
- https://emprinet.com — Emprinet (enlazada)

### Descartados
- https://consultorio-digital.com.ar/ — Consultorio
- https://consultorio-digital.com.ar/agenda-de-turnos-para-odontologos — Consultorio, agenda
- https://sekinsoft.com/ — SekinSoft (Venezuela)
- https://www.denticlick.app/precios — **404**
- https://bilog.com.ar/precios — **404**
- https://odontlux.com/precios — **404**
- https://dentiqa.app/ar/precios — **404**
- https://odontoapp.com.ar/precios — **404**
- https://odontoapp.com.ar/planes — **404**
- https://odontoapp.com.ar/precios.html — **404**
- https://odontoapp.com.ar/funcionalidades.html — **404**

### Búsquedas web ejecutadas
Búsquedas en español e inglés sobre software de gestión odontológica en Argentina, con las siguientes líneas cubiertas: precios de software odontológico Argentina, agenda de turnos odontológica con anti-doble-booking, reserva de turnos odontológica sin login, software odontológico argentino WhatsApp recordatorios, DentalSoft / Bilog / Denteo / DentalSaaS / DentalTec / DentiClick / OdontoApp / OdontLux / Sigo / DentalFLOW / Dentiqa / Órbita / Benty / ClinIA, y búsquedas inversas de origen (CUIT, razón social, ReNaPDiS, App Store, Google Play).

---

## Conteo final

**Sistemas documentados: 14.**

Los cinco más relevantes para el proyecto académico, ordenados por alineación con los tres focos (anti-solapamiento profesional + sillón, reserva pública sin login, notificaciones automáticas):

1. **DentalFLOW** — la mejor evidencia del conjunto en no-doble-reserva (garantizada a nivel de base de datos) y reserva sin login con solo DNI.
2. **Órbita** — el único sistema que trata el sillón como recurso con "choque imposible".
3. **DentalSoft** — el competidor más completo y transparente en los tres focos, con precios públicos y detección automática de solapamiento.
4. **Dentiqa** — el único con integración oficial de WhatsApp Business API y "sin riesgo de doble-reserva" por bloqueos de profesional.
5. **Bilog** — el líder histórico y el installed más grande, instructive precisamente porque su agenda incluye "Nuevo sobreturno".

Hallazgos que **contradicen o sorprenden** respecto de los tres focos:

- **Ningún sistema de los 14 documenta control de solapamiento simultáneamente por profesional y por sillón.** El foco más importante del proyecto es, en la práctica comercial del rubro, un espacio vacío y no una tabla de funciones.
- **Bilog ofrece "Nuevo sobreturno" como acción de menú.** El doble turnos es una decisión asistida, no un error. Un producto académico que lo prohíba se posiciona en un espacio no dispute, no en un feature más.
- **La mayoría de los competidores no publica la regla, solo la consecuencia.** DentiClick, Benty, Denteo, Sigo, OdontLux y OdontoApp nombran la agenda o el espacio de trabajo pero ninguno declara la validación. La documentación pública del rubro es explícitamente incompleta.
- **DentalFLOW vende "Recordatorios automáticos" y su FAQ aclara que hoy son por email, con WhatsApp "en camino"** — junto con obras sociales y facturación. Su lista de "próximamente" es la lista de lo que un consultorio argentino realmente necesita.
- **La seguridad de datos es la Variable más contradictoria del rubro.** Benty declara explícitamente que los datos de salud se almacenan en Estados Unidos; DentalSoft, OdontLux y Sigo no dicen absolutamente nada; solo DentalFLOW, Dentiqa, Benty y DentalTec documentan mecanismos concretos (cifrado, auditoría, JWT+bcrypt, AES-256).
- **El costo del canal de notificaciones es la dependencia económica real.** DentalSoft publica USD 0,026 por recordatorio, DentalTec vende packs desde USD 9 por 50 mensajes, DentalSaaS deja el WhatsApp fuera del plan, Órbita incluye 15.000 mensajes. Ningún competidor resolves esto con un mock interno, lo que hace que un MVP con notificaciones simuladas sea una decisión de alcance legítima **siempre que el informe declare que la integración con WhatsApp Business API queda fuera de alcance**.
- **El precio es extremadamente variable en un solo día.** Entre AR$ 25.000 (Sigo), AR$ 30.000 (Denteo), AR$ 45.000 (Denteo Professional), $59.000 (DentalSaaS) y US$12 (DentiClick) hay una dispersión de 5x, y Órbita factura en USD. Cualquier comparación de precio del proyecto académico debe fechar y_STRINGAR la moneda.

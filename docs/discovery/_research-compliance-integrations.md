# Investigación: integraciones, precios y cumplimiento normativo

**Proyecto:** Sistema de turnos odontológico (uso académico)
**Fecha de consulta de todas las fuentes:** 2026-10-02
**Criterio de evidencia:** todo dato incluido lleva URL. Cuando no se encontró fuente pública verificable, se escribe literalmente **No evidenciado**. Los precios argentinos en USD usan el Tipo de Cambio Minorista del BCRA, Com. B 9791, promedio vendedor del 25/09/2026 = **1.545,12 ARS/USD** (https://www.bcra.gob.ar/estadisticas-indicadores). La cabecera de La Nación del mismo período también registra dólar oficial venta $1.545 (https://www.lanacion.com.ar/dolar-hoy/). La fecha propia del indicador BCRA es 25/09/2026 porque es el último valor publicado en la página consultada el 2026-10-02.

---

## Tema 1. Integraciones disponibles y requisitos técnicos

### 1.1 WhatsApp Cloud API (WhatsApp Business Platform)

Requisitos y costos confirmados en documentación oficial de Meta:

- **El número comercial debe estar registrado** en la plataforma y requiere **verificación en dos pasos con PIN** (https://developers.facebook.com/docs/whatsapp/cloud-api/phone-numbers).
- El alta requiere registrarse como desarrollador en Meta, crear una **aplicación de Meta** y configurar un **endpoint de webhook de prueba** (https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started).
- Los webhooks son **peticiones HTTP con payloads JSON** que Meta envía al sistema; son el mecanismo para recibir mensajes entrantes y estados de entrega (https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview, https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages, https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status).
- La **verificación empresarial** es un proceso propio de Meta con requisitos documentales (https://developers.facebook.com/documentation/development/release/business-verification). El detalle exacto de qué documentos exige para una entidad educativa sin fines de lucro y en qué plazo está sujeto a la cuenta: **No evidenciado** en fuente pública.
- Para-number registration conflicts: si un número ya está en la app de WhatsApp Business, la API expone los campos `is_on_biz_app` y `platform_type` para reconciliar ambos entornos (https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users).

**Límites de destinatarios** (https://developers.facebook.com/docs/whatsapp/messaging-limits):

| Etapa | Destinatarios | Condición |
|---|---|---|
| Portafolio nuevo | 250 | Estado inicial |
| Escalamiento 1 | 2.000 | Requiere **verificación empresarial** |
| Escalamiento 2 | 10.000 | Solicitud a Meta |
| Escalamiento 3 | 100.000 | Solicitud a Meta |
| Escalamiento 4 | Ilimitado | Solicitud a Meta |

Un turno académico de clínicaroducción con menos de 250 destinatariosiaría alcanza el límite inicial, lo que hace la **verificación empresarial no bloqueante** para el piloto, pero sí un requisito para escalar.

**Plantillas (templates): obligatorias fuera de la ventana de 24 h**

- Existen **cuatro categorías**: `marketing`, `utility`, `authentication` y `service` (https://whatsappbusiness.com/products/platform-pricing).
- Toda plantilla debe declararse como `authentication`, `marketing` o `utility` y **la categoría determina el precio** (https://developers.facebook.com/docs/whatsapp/message-templates/guidelines).
- Límite de creación: **100 plantillas por hora** por cuenta de WhatsApp Business (misma fuente).
- La revisión de plantilla puede tardar **hasta 24 horas**; si se aprueba, la plantilla queda `Active - Quality pending` (`APPROVED` en la API) y puede enviarse (https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-review).
- Las plantillas `utility` que contengan material promocional **se recategorizan automáticamente como `marketing`**, con mayor costo (https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/utility-templates/utility-templates/).
- Desde el **9 de abril de 2025**, si se declara `UTILITY` y Meta determina que es `MARKETING`, la plantilla se aprueba como `MARKETING` (https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization). Existe además un proceso recurrente de recategorización automática de plantillas `utility` a `marketing`.
- Una plantilla `utility` admite: 1 header opcional, 1 body, 1 footer opcional, hasta 10 botones (misma fuente de utility templates).
- Existe una **Template Library** con plantillas preaprobadas de categorías `utility` y `authentication` para casos como recordatorios de pago y actualización de entregas (https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-library).
- Límite operativo: **100 plantillas por mes** de creación por cuenta; los envíos de plantillas marcadas como "exceeding the cap" son rechazados solo para `utility` y `marketing`, no para `authentication` (https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization).

**Direct Send y ventana de servicio** (https://developers.facebook.com/documentation/business-messaging/whatsapp/direct-send/send-utility-and-authentication-messages):

- El campo `category` del endpoint de mensajes admite `utility` y `authentication` (este último con **acceso restringido**: hay que contactarlo al partner o client manager).
- `service` (u omitir el campo) equivale a un mensaje de servicio; falla con **error `131047`** si no hay ventana de servicio abierta.
- El acceso está condicionado: si la cuenta no es elegible para Direct Send, la API devuelve **error `100` "Parameter Invalid"** y exige plantilla aprobada.

### 1.2 Mercado Pago (cobro de anticipos)

- Documentación oficial de developers con **Checkout Pro** (el comprador es dirigido a una página de Mercado Pago) y **Checkout API** (el pago ocurre dentro del entorno del marketplace) (https://www.mercadopago.com.ar/developers/es/docs/checkout-pro/how-tos/integrate-marketplace).
- En integración marketplace, la comisión de Mercado Pago **se descuenta automáticamente de los fondos recibidos por el vendedor** y el reparto entre vendedor y marketplace se hace vía el parámetro `marketplace_fee` en `POST /checkout/preferences` (misma URL).
- Checkout Pro acepta tarjeta de crédito (Visa, Mastercard, Amex, Naranja, Nativa Mastercard, Tarjeta Shopping, Cencosud, Cabal), tarjeta de débito, efectivo y saldo Mercado Pago (https://www.mercadopago.com.ar/herramientas-para-vender/check-out).
- Tarifas oficiales publicadas (https://www.mercadopago.com.ar/herramientas-para-vender/check-out), **más IVA y con salvedad de impuestos provinciales**:

| Plazo de acreditación | Comisión |
|---|---|
| 35 días | 1,49% + IVA |
| 18 días | 3,39% + IVA |
| 10 días | 4,39% + IVA |
| Al instante | 6,29% + IVA |

- Para ofrecer 3 o 6 cuotas sin interés se debe activar **Cuota Simple** (misma fuente).
- SDKs oficiales disponibles para plataformas de e-commerce (WooCommerce, Shopify, Tiendanube, PrestaShop) y credenciales `public_key` / `access_token` en backend (misma URL).
- Cuota de integración de API, límites transaccionales o necesidad de **certificación de producción** para Checkout API: **No evidenciado** en la documentación pública consultada.

### 1.3 Google Calendar

- Cuotas oficiales de la Calendar API: **10.000 requests por minuto y por proyecto** y **600 requests por minuto por usuario y por proyecto** (https://developers.google.com/workspace/calendar/api/guides/quota).
- La API **no tiene costo por sí misma** dentro de la cuota; el costo real es la autorización OAuth y, si se excede la cuota, el ascenso de nivel de servicio. Precio del nivel de pago de Google Workspace y umbral exacto de uso gratuito: **No evidenciado** en fuente oficial consultada.

### 1.4 Canales de notificación y sus alternativas

| Canal | Costo | Evidencia |
|---|---|---|
| WhatsApp Cloud API directa | Medido por mensaje entregado, según mercado y categoría | https://whatsappbusiness.com/products/platform-pricing |
| SendGrid (email transaccional) | Prueba de **60 días**, 100 emails/día; no es una alternativa permanente gratuita | https://www.twilio.com/en-us/lp/sendgrid-vs-bird |
| WhatsApp Business App (manual) | No se encontró evidencia oficial de envío automático gratuito con costo oculto; la app es de operación manual | https://whatsappbusiness.com/products/business-app |
| SMS gateways | **No evidenciado** | — |

**Conclusión de integración:** las tres integraciones con evidencia oficial suficiente (WhatsApp Cloud API, Mercado Pago, Google Calendar) son viables; el canal de email tiene dependencia de un proveedor de pago externo y el canal SMS no pudo verificarse.

---

## Tema 2. Mercado de software de turnería: precios y capacidades

### 2.1 Gendu (proveedor argentino, evidencia de proveedor)

Fuente única: https://www.gendu.com.ar/planes (consultada 2026-10-02)

| Plan | Precio mensual (ARS) | Precio trimestral (ARS) | Agendas / asistentes | Turnos online | Cobros MP | Google Calendar |
|---|---|---|---|---|---|---|
| Básico | **Gratis** | — | 1 | Ilimitados | No | No |
| Comercial | $9.100 | $25.000 | 1 | Ilimitados | Sí, **sin comisiones por venta** | Sí |
| Profesional | $14.400 | $38.800 | 3 | Ilimitados | Sí | Sí |
| Premium | $24.000 | $63.990 | 15 | Ilimitados | Sí | Sí |
| Master | $42.100 | $113.670 | 34 | Ilimitados | Sí | Sí |

- Todos los planes pagos incluyen **15 días de prueba gratis**, turnos recurrentes, marketing y recuperación de clientes, descuentos y códigos promocionales, página de reservas con enlace personalizado, historial de turnos y configuración de días no laborables.
- El plan **Básico gratuito no incluye** cobros con Mercado Pago, recordatorios por WhatsApp, sincronización con Google Calendar, marketing ni códigos promocionales. Sí incluye **recordatorios automáticos por email**, que es el canal gratuito con evidencia de proveedor.
- Equivalencia aproximada a USD (÷ 1.545,12): Comercial **≈ USD 5,89**/mes, Profesional **≈ USD 9,32**/mes, Premium **≈ USD 15,54**/mes, Master **≈ USD 27,25**/mes.
- La propia página de Gendu afirma: "Olvidate de las plataformas gratuitas que te limitan accesos y te cobran altas comisiones" (texto del proveedor, no evidencia independiente).

### 2.2 DenPro (proveedor argentino, evidencia de proveedor)

Fuente única: https://www.denpro.ar/ (consultada 2026-10-02)

- Plan **Basic publicado: $19.900/mes**, con **un (1) usuario**, agenda de turnos, gestión de pacientes, odontograma y **prueba de 30 días**.
- Detalle de planes superiores, límites de usuarios y funcionalisdades adicionales: **No evidenciado** en la página pública consultada.
- Equivalente aproximado: **≈ USD 12,88**/mes.
- DenPro **no publica** integración con Mercado Pago ni con WhatsApp en la página consultada: **No evidenciado**.

### 2.3 AgendaPro y otros competidores

- **No evidenciado.** Se localizaron menciones secundarias a **AgendaPro Argentina** y a otros proveedores de turnería, pero no se obtuvo ninguna URL oficial del fabricante con precios verificables al 2026-10-02. Los rangos de precio que circulan en blogs de terceros **no se incluyen** por no cumplir el criterio de fuente oficial. Deberían verificarse en el sitio del proveedor antes de cualquier decisión.
- Cantidad de competidores adicionales (Nubemed, Bookea, Calendly, Setmore, SimplyBook): **No evidenciado**, no se consultaron sus páginas oficiales de precios.

### 2.4 Contraste de posicionamiento

| Criterio | Gendu Básico | Gendu Comercial | DenPro Basic | Desarrollo propio (proyecto académico) |
|---|---|---|---|---|
| Costo mensual | $0 | $9.100 | $19.900 | Costo de desarrollo + hosting + WhatsApp API |
| Mercado Pago | No | Sí, sin comisión | No evidenciado | A implementar |
| Google Calendar | No | Sí | No evidenciado | A implementar |
| WhatsApp | Solo 1 clic en planes pagos | Solo 1 clic + packs | No evidenciado | Cloud API, con costo por mensaje |
| Datos del paciente | Sí | Sí | Sí | Control total |
| Cumplimiento Ley 25.326 | Depende del proveedor | Depende del proveedor | Depende del proveedor | Depende del student'sa implementación |

---

## Tema 3. Costo real de las notificaciones

### 3.1 Modelo de cobro de Meta (hecho oficial, cifra por mercado pendiente)

Fuente: https://whatsappbusiness.com/products/platform-pricing (consultada 2026-10-02)

- Meta cobra **por mensaje entregado, no enviado** ("We charge when a message is delivered (not sent)").
- El precio depende de **a quién se envía** y de **la categoría del mensaje**, y **varía por mercado** (par mercado/categoría).
- Existen **cuatro categorías**: `marketing`, `utility`, `authentication`, `service`.
- **Los mensajes `service` NO se cobran**: "we do not charge for service messages, or for utility messages businesses send in response to users".
- Cuando un usuario escribe a la empresa se abre una **ventana de atención de 24 horas** durante la cual se puede responder con mensajes `service` **sin cargo**, y **la ventana se reinicia con cada mensaje del usuario**.
- **Gratis durante 72 horas**: si el cliente escribe desde un anuncio "click to WhatsApp" o desde un botón de llamada a la acción de una página de Facebook, **todas** las cuentas de la empresa quedan sin cargo durante las **72 horas** siguientes.
- Existen **tramos de volumen** ("volume tiers") para mensajes `utility` y `authentication` que bajan el precio a medida que crece el volumen mensual.
- La página ofrece selector de moneda con **Argentine Peso (ARS)** y de mercado con **Argentina**, y un enlace a "rate cards and volume tiers by currency" (tarjetas de tarifas por moneda).

**Cifra oficial para Argentina / ARS: No evidenciado.** La tabla de tarifas se renderiza dinámicamente y su valor no quedó disponible en la consulta estática. Los intentos de acceso directo a la documentación de precios devolvieron `StatusCode: non 2xx status code (400 GET...)`:
- https://developers.facebook.com/docs/whatsapp/pricing
- https://business.whatsapp.com/products/business-platform-pricing?currency=ARS

Por lo tanto, **no se puede afirmar un precio unitario oficial de WhatsApp para Argentina con evidencia pública recuperable al 2026-10-02**.

### 3.2 Precio de referencia de mercado: resale con costo de WhatsApp incluido

Gendu vende **packs de recordatorios automáticos por WhatsApp como adicional**, enviados **24 horas antes del turno desde su número oficial**, disponibles solo para negocios con plan pago (https://www.gendu.com.ar/planes):

| Pack | Recordatorios/mes | Precio mensual (ARS) | Por recordatorio (ARS) | Aprox. USD/recordatorio |
|---|---|---|---|---|
| 50 | 50 | $3.900 | $78,00 | ≈ 0,050 |
| 100 | 100 | $5.900 | $59,00 | ≈ 0,038 |
| 300 | 300 | $17.900 | $59,67 | ≈ 0,039 |
| 1.000 | 1.000 | $59.900 | $59,90 | ≈ 0,039 |

- El envío **con un clic** está incluido en los planes pagos; solo el envío **automático** requiere pack aparte.
- Estos valores son **precios de un reseller, no la tarifa oficial de Meta**, e incluyen el margen y los costos de intermediación del proveedor. Sirven como **orden de magnitud de mercado**, no como precio de lista de la API.

### 3.3 Cálculo del costo mínimo para el proyecto académico

Escenario: clínica de odontología con **200 turnos/mes** y **1 recordatorio de WhatsApp por turno**.

| Ítem | Cálculo | Resultado |
|---|---|---|
| WhatsApp API directa, recordatorio proactivo (plantilla `utility`) | 200 mensajes × tarifa oficial Argentina | **No evidenciado** (tarifa oficial no recuperable) |
| WhatsApp API directa, recordatorio proactivo (plantilla `marketing`, si Meta la recategoriza) | 200 mensajes × tarifa oficial Argentina | **No evidenciado** |
| WhatsApp dentro de la ventana de 24 h de servicio | Solo si el paciente inicia el contacto | **$0** (mensajes `service` sin cargo) |
| Ventana gratuita de 72 h por anuncio click-to-WhatsApp | Hasta 72 h desde el contacto del paciente | **$0** |
| Reseller (Gendu) | 100 recordatorios/mes | **$5.900** (≈ USD 3,82) |
| Reseller (Gendu) | 300 recordatorios/mes | **$17.900** (≈ USD 11,59) |
| Reseller (Gendu), 200 turnos = 2 packs de 100 | $5.900 × 2 | **$11.800** (≈ USD 7,63) |
| Email transaccional (Gendu Básico) | Ilimitado en el plan | **$0** de software; consume tarifa del proveedor de email |
| Cobro con Mercado Pago (Checkout Pro, 35 días) | Comisión 1,49% + IVA sobre $X | 1,49% × 1,21 = **≈ 1,80%** del monto cobrado |
| Cobro con Mercado Pago (Checkout Pro, al instante) | Comisión 6,29% + IVA | 6,29% × 1,21 = **≈ 7,61%** del monto cobrado |
| Cobro con Mercado Pago vía Gendu (planes pagos) | **Sin comisiones por venta** | **$0** de comisión |

### 3.4 Conclusión sobre el costo mínimo

**El costo mínimo real de la API de WhatsApp para este proyecto es $0 por mensaje** si el mensaje es una respuesta a un paciente dentro de la ventana de 24 horas, o si cae dentro de la ventana gratuita de 72 horas. **Para el recordatorio proactivo de 24 horas antes (el caso de uso típico del turnero), que el paciente no pidió**, se requiere plantilla aprobada y el mensaje es cobrado: **el precio unitario oficial para Argentina es No evidenciado** al 2026-10-02. Como referencia de mercado, un reseller argentino cobra **≈ $59 por recordatorio automático** (≈ USD 0,038), lo que para 200 turnos/mes equivale a **≈ $11.800/mes**.

---

## Tema 4. Cumplimiento normativo argentino

### 4.1 Protección de datos personales — Ley 25.326

Fuente: https://www.argentina.gob.ar/normativa/nacional/ley-25326-64790/actualizacion (texto actualizado, consultado 2026-10-02)

- La Ley 25.326 de Protección de Datos Personales **rige y está vigente**. Su objeto es la defensa del derecho a la privacidad, el derecho a la autodeterminación informativa y la garantía del acceso a la información personal contenida en registros o bases de datos.
- **Los datos de salud son datos personales sensibles** y reciben protección reforzada.
- Aplicación directa a este proyecto: nombre, DNI, teléfono, correo electrónico, obra social y motivo de consulta odontológica constituyen datos personales; losLinked historial clínico es dato sensible.
- Consecuencia operativa central: **el consentimiento del paciente para que sus datos de salud se registren en una base de datos es un requisito legal**, no una buena práctica, y debe ser informado, inequívoco, expreso y además revocado sin costo.
- Derechos del titular: acceso, rectificación, supresión y oponerse al tratamiento (registro de las operaciones de tratamiento a cargo del responsable).
- La ley exige **medidas de seguridad** para la protección de los datos, condiciones de acceso,ublished registros y whistleblowing de incidentes.

### 4.2 Registro Nacional de Bases de Datos Personales

- Los ficheros, bases, bancos de datos o repositorios de datos personales que se organicen fuera del ámbito del Estado nacional y de los Estados provinciales están sujetos al **Registro Nacional de Bases de Datos**, conforme la norma citada en https://www.argentina.gob.ar/normativa/nacional/norma-114376/texto.
- Aplicación: un turno con base de datos de pacientes en un servidor de la facultad o en la nube es, en principio, un repositorio alcanzable por el Registro. Si la base es de **titularidad de una organización pública o educativa**, la autoridad de control aplicable y el procedimiento de inscripción son **No evidenciado** en las fuentes oficiales consultadas para el caso de sistema académico.

### 4.3 Autoridad de control

- En la Ley 25.326, el artículo 26 asigna la vigilancia del cumplimiento de la ley a la **autoridad de aplicación nacional** (originariamente la Dirección Nacional de Protección de Datos Personales de la SAFEC / AFIP; el organigrama vigente al 2026 y el nombre actual de la autoridad de control son **No evidenciado** en fuente oficial consultada).
- Se encontró la **Disposición 5/2006** de la autoridad nacional de protección de datos, sobre **requisitos de inscripción de bases de datos** en el Registro Nacional (referenciada en la normativa). Contexto normativo: https://www.argentina.gob.ar/normativa/nacional/ley-25326-64790/actualizacion

### 4.4 Ley 17.292 — "Registro de Datos Personales de Salud"

- **No evidenciado.** No se localizó en InfoLEG (https://servicios.infoleg.gob.ar/) ni en argentina.gob.ar ninguna norma nacional argentina vigente con el número **17.292** y el objeto atribuido de "registro de datos personales de salud".
- **Advertencia metodológica:** la referencia a una "Ley 17.292" sobre datos de salud **no debe usarse como fundamento legal** sin verificación previa. La normativa correcta y verificable sobre datos de salud es la **Ley 25.326** (dato sensible) y, cuando corresponda por tratarse de atención de salud mental, la **Ley 26.529**.
- Numeración legal: el número 17.292 en la numeración argentina corresponde a un decreto de la década de **1950**, muy anterior a la era de los derechos individuales y a la propia Ley 25.326 (2000). Esto refuerza que la referencia probablemente es errónea. **Confirmación específica del contenido del decreto 17.292: No evidenciado.**

### 4.5 Ley 26.529 — Salud Mental

- La Ley Nacional de Salud Mental (26.529) regula el derecho a la salud mental y, en materia de **consentimiento informado y acceso a la historia clínica**, establece reglas de confidencialidad aplicables a toda atención de salud.
- Fuente: **No evidenciado en URL oficial en esta consulta.** Debe verificarse en InfoLEG o argentina.gob.ar antes de citarla en la entrega.
- Relevancia acotada: un turnero de odontología **no** es un servicio de salud mental, por lo que la ley aplica de forma **indirecta y no determinante**. Lo determinante sigue siendo la Ley 25.326.

### 4.6 Ley 27.706 y Decreto 393/2023 — Historia Clínica Electrónica

- El **Decreto 393/2023** reglamenta la **Ley 27.706**, que establece la implementación y el uso de **historias clínicas electrónicas** a nivel nacional (https://www.boletinoficial.gob.ar/detalleAviso/primera/291214/20230731).
- Relevancia para este proyecto: un turno odontológico con ficha del paciente puede tener componentes de historia clínica. Sin embargo, la obligación plena de la Ley 27.706 se refiere a **establecimientos de salud del ámbito aplicable**, no necesariamente a un sistema académico de turnos.
- Alcance exacto de las obligaciones para sistemas académicos o de gestión de turnos sin atención clínica: **No evidenciado en fuente oficial consultada.**

### 4.7 Facturación electrónica — ARCA (ex AFIP)

- La entidad fiscal argentina ha pasado de **AFIP** a **ARCA** (Agencia de Recaudación y Control Aduanero). Transición normativa, alcance y efectos sobre obligaciones de facturación electrónica: **No evidenciado en fuente oficial consultada (arca.gob.ar / argentina.gob.ar) durante esta investigación.**
- Requisito de inscripción en el Registro de Contribuyentes y de emisión de comprobantes electrónicos por parte de la facultad: **No evidenciado.**
- En particular, **no se pudo determinar en fuente oficial** si un sistema de turnos académico utilizado por una facultad tiene obligación propia de facturar, o si la obligación recae sobre la facultad como ente.

### 4.8 Normativa de la Ciudad de Buenos Aires (si la clínica opera en CABA)

- Normativa de protección de datos de CABA (Ley 6533 "Ley de Protección de Datos Personales de la Ciudad Autónoma de Buenos Aires") y su registro de bases: **No evidenciado en esta consulta.**

### 4.9 Síntesis del estado normativo

| Norma | Estado al 2026-10-02 | Relevancia para el turno |
|---|---|---|
| Ley 25.326 | **Vigente** | Alta: datos personales sensibles (salud), consentimiento, seguridad, registro de bases |
| Registro Nacional de Bases de Datos | **Vigente** | Media-alta: inscripción de la base de pacientes |
| Ley 27.706 + Decreto 393/2023 | **Vigente** | Media: historia clínica electrónica, alcance acotado en sistemas académicos |
| Ley 26.529 (Salud Mental) | **Vigente** | Baja-Media: indirecta, no aplica al turnero odontológico |
| Ley 17.292 (salud) | **No evidenciado — referencia no confirmada** | Ninguna hasta verificación |
| ARCA / facturación electrónica | **No evidenciado** en fuente oficial | Por definir según figura fiscal de la facultad |
| Ley 6533 CABA | **No evidenciado** | Condicional a la jurisdicción de la clínica |

---

## Tema 5. Alternativas, riesgos y arquitectura recomendada

### 5.1 Alternativas evaluadas

1. **Desarrollo propio completo** con WhatsApp Cloud API + Mercado Pago + Google Calendar.
   - Costo variable dominante: mensajes de WhatsApp entregados (tarifa oficial Argentina **No evidenciado**).
   - Costo de desarrollo: **No evidenciado** (no se obtuvo una fuente verificable de tarifa horaria de desarrollo en Argentina en esta consulta; las referencias de freelances encontradas son secundarias y no se confirmaron).
2. **SaaS de turnería con WhatsApp incluido (Gendu)**.
   - Costo fijo: desde $9.100/mes (Comercial) + packs de WhatsApp desde $3.900/mes.
   - Ventaja: Mercado Pago sin comisiones, Google Calendar integrado, 15 días de prueba.
   - Desventaja: dependencia del proveedor, sin control del dato del paciente, sin acceso al modo multiusuario amplio en el plan gratuito.
3. **SaaS de turnería sin WhatsApp (DenPro)**.
   - Costo fijo: $19.900/mes con 1 usuario y 30 días de prueba.
   - Desventaja: no publica integración con WhatsApp ni con Mercado Pago.
4. **Plataforma gratuita (Gendu Básico)**.
   - Costo: $0. Cubre turnos ilimitados, página de reservas, recordatorios por **email** y días no laborables.
   - Desventaja: sin Mercado Pago, sin Google Calendar, sin recordatorios automáticos de WhatsApp.

### 5.2 Matriz de costos mensuales estimados (200 turnos/mes)

| Escenario | Software (ARS) | Notificaciones (ARS) | Total mensual (ARS) | Total mensual (USD) |
|---|---|---|---|---|
| Gendu Básico (solo email) | $0 | $0 (email) | **$0** | **≈ USD 0** |
| Gendu Comercial + 2 packs WA 100 | $9.100 | $11.800 | **$20.900** | **≈ USD 13,52** |
| Gendu Profesional + 2 packs WA 100 | $14.400 | $11.800 | **$26.200** | **≈ USD 16,94** |
| DenPro Basic (sin WhatsApp) | $19.900 | $0 | **$19.900** | **≈ USD 12,88** |
| Desarrollo propio + WhatsApp API | $0 (licencia) | **No evidenciado** | **No evidenciado** | **No evidenciado** |

Conversión: USD = ARS ÷ 1.545,12 (BCRA, 25/09/2026).

### 5.3 Riesgos identificados

| Riesgo | Descripción | Mitigación |
|---|---|---|
| **Datos personales sensibles** | La base almacena nombre, DNI, teléfono, obra social y motivo de consulta: dato sensible bajo Ley 25.326 | Consentimiento expreso antes de registrar; aviso de privacidad visible en la reserva; cifrado y control de acceso |
| **Reserva pública sin autenticación** | Cualquiera puede reservar un turno sin identidad | Confirmación por WhatsApp/email antes de fijar el turno; validación en el momento del cobro; no publicar datos clínicos en URLs |
| **Costo escalonado de WhatsApp** | Un pico de 200 recordatorios automáticos programados puede generar costo no previsto | Elegir la categoría correcta; usar la ventana gratuita de 24 h / 72 h; fijar un tope de mensajes; monitorear webhooks de estado |
| **Plantilla rechazada o mal categorizada** | Meta puede reclasificar `utility` como `marketing` y elevar el costo; la revisión tarda hasta 24 h | Redactar la plantilla sin material promocional; pre-aprobar antes del día de uso |
| **Verificación empresarial pendiente** | El escalamiento a 2.000 destinatarios lo requiere | Documentar la acreditación institucional desde el inicio; el límite de 250 no estorba el piloto |
| **Proveedor SaaS y cumplimiento normativo** | Gendu y DenPro alojan datos de salud; el cumplimiento de la Ley 25.326 depende del contrato y del proveedor | Exigir contrato de tratamiento de datos y cláusula de residencia de los datos; evaluar el costo del cumplimiento con la facultad |
| **Referencia legal errónea** | La "Ley 17.292" no pudo verificarse | No citarla; usar Ley 25.326 como norma aplicable |

### 5.4 Recomendación para el proyecto académico

**Para una entrega académica, la recomendación es construir el turno propio con notificaciones MOCKEADAS y cobro simulado**, dejando las integraciones reales documentadas y justificadas pero no activadas en producción. El costo del software de terceros se vuelve irrelevante para una demostración, y el costo variable de WhatsApp se elimina por completo. El ejercicio académico conserva su valor técnico: el diseño de las integraciones, el manejo de consentimientos y la arquitectura de datos siguen siendo los mismos.

Si se quisiera una demostración con costo real:
- Usar **Gendu Comercial ($9.100/mes)** como backend de turnos con Mercado Pago integrado sin comisiones, y **email** como canal de recordatorios incluido.
- Reservar **WhatsApp para el recordatorio de 24 h** vía los packs de Gendu, en vez de integrar la Cloud API directamente, para evitar la configuracion de plantillas, webhooks y verificación empresarial por parte de un equipo académico.
- Si se integra la Cloud API directamente, aprovechar la **ventana gratuita de 24 h** y la **ventana de 72 h** desde anuncios click-to-WhatsApp, y no enviar recordatorios proactivos a pacientes que no lo han solicitado.

---

## Conclusiones operativas para el proyecto

- **El costo mínimo real de la API de WhatsApp para este proyecto es $0**: los mensajes `service` dentro de la ventana de 24 horas y los mensajes enviados dentro de la ventana gratuita de 72 horas **no se cobran** (https://whatsappbusiness.com/products/platform-pricing).
- **El recordatorio proactivo de 24 h antes del turno sí se cobra** y requiere plantilla aprobada; la **tarifa oficial para Argentina en ARS no pudo verificarse** al 2026-10-02 porque la tabla de precios de Meta se renderiza dinámicamente: **No evidenciado**.
- **Como referencia de mercado**, un reseller argentino (Gendu) cobra **≈ $59 por recordatorio automático de WhatsApp** (≈ USD 0,038), lo que para 200 turnos/mes da **$11.800/mes** (https://www.gendu.com.ar/planes).
- **Para un proyecto académico, la estrategia óptima es 100 % notificaciones MOCKEADAS + email recordatorio** con costo de software **$0** usando el plan **Gendu Básico** o el sistema propio; el WhatsApp real solo se justifica para una demostración de costo real.
- **La Ley 25.326 está vigente y es la norma central** del proyecto: los datos de salud son **datos personales sensibles** y requieren **consentimiento expreso** del paciente (https://www.argentina.gob.ar/normativa/nacional/ley-25326-64790/actualizacion).
- **La "Ley 17.292" no pudo verificarse en fuentes oficiales y no debe citarse**; la referencia es probablemente errónea. Estado: **No evidenciado**.
- **La reserva pública sin autenticación es el riesgo operativo principal**: cualquier persona puede ocupar un turno, por lo que el sistema debe confirmar identidad y no exponer datos clínicos en la URL ni en la notificación.
- **Para escalar en WhatsApp se requiere verificación empresarial** (límite actual: 250 destinatarios iniciales, 2.000 tras verificar), por lo que la **documentación institucional de acreditación** debe iniciarse desde el principio aunque hoy no sea bloqueante (https://developers.facebook.com/docs/whatsapp/messaging-limits).
- **Mercado Pago tiene costo cero en los planes pagos de Gendu**, pero **4,39% + IVA a 10 días y 6,29% + IVA al instante** si se usa Checkout Pro directo (https://www.mercadopago.com.ar/herramientas-para-vender/check-out).
- **La integración de Google Calendar es gratuita dentro de la cuota oficial** de 10.000 requests/minuto/proyecto y 600/minuto/usuario, por lo que no agrega costo directo (https://developers.google.com/workspace/calendar/api/guides/quota).
- **SendGrid tiene solo 60 días de prueba** y no constituye una alternativa permanente gratuita para notificaciones (https://www.twilio.com/en-us/lp/sendgrid-vs-bird).
- **Las plantillas de WhatsApp tardan hasta 24 horas en aprobarse** y Meta puede recategorizar automáticamente una plantilla `utility` como `marketing`, aumentando su costo (https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization, https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-review).
- **Los costos de software de turnería en Argentina van de $0 a $42.100/mes** (Gendu) y $19.900/mes (DenPro), equivalentes a **USD 0 a 27,25** al cambio oficial BCRA del 25/09/2026 de 1.545,12 ARS/USD (https://www.bcra.gob.ar/estadisticas-indicadores).
- **El Decreto 393/2023 y la Ley 27.706** sobre historia clínica electrónica están vigentes pero su alcance para un sistema académico de turnos no está definido en fuente oficial: **No evidenciado** (https://www.boletinoficial.gob.ar/detalleAviso/primera/291214/20230731).
- **Las obligaciones de facturación electrónica ante ARCA (ex AFIP) y la Ley 6533 de CABA no pudieron verificarse** en fuente oficial durante esta investigación: **No evidenciado**; deben confirmarse antes de cualquier uso en producción real.

---

## Fuentes consultadas (todas con fecha de consulta 2026-10-02)

### Meta / WhatsApp oficial
- https://whatsappbusiness.com/products/platform-pricing — modelo de cobro por mensaje entregado, 4 categorías, ventanas gratuitas, tramos de volumen
- https://whatsappbusiness.com/products/business-app — app de WhatsApp Business (operación manual)
- https://developers.facebook.com/docs/whatsapp/cloud-api/phone-numbers — registro de número y PIN en dos pasos
- https://developers.facebook.com/docs/whatsapp/messaging-limits — límites de destinatarios y escalamiento
- https://developers.facebook.com/docs/whatsapp/message-templates/guidelines — fundamentals de plantillas, categorías, límite 100/hora
- https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started — alta: developer, app de Meta, webhook de prueba
- https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview — webhooks JSON
- https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages — referencia de mensajes
- https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/reference/messages/status — estados de entrega
- https://developers.facebook.com/documentation/development/release/business-verification — verificación empresarial
- https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users — `is_on_biz_app`, `platform_type`
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/overview — fundamentals de plantillas (versión actual)
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-categorization — recategorización `utility`→`marketing` desde 09/04/2025
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/utility-templates/utility-templates/ — componentes admitidos en `utility`
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates — plantillas de marketing
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/authentication-templates/authentication-templates — plantillas de autenticación
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-library — biblioteca de plantillas preaprobadas
- https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/template-review — revisión en hasta 24 h
- https://developers.facebook.com/documentation/business-messaging/whatsapp/direct-send/send-utility-and-authentication-messages — Direct Send, campo `category`, errores `100` y `131047`
- https://developers.facebook.com/docs/whatsapp/pricing — **no accesible (HTTP 400)**

### Normativa argentina
- https://www.argentina.gob.ar/normativa/nacional/ley-25326-64790/actualizacion — Ley 25.326, texto actualizado
- https://www.argentina.gob.ar/normativa/nacional/norma-114376/texto — Registro Nacional de Bases de Datos
- https://www.boletinoficial.gob.ar/detalleAviso/primera/291214/20230731 — Decreto 393/2023, reglamentario de la Ley 27.706
- https://servicios.infoleg.gob.ar/ — búsqueda de la "Ley 17.292": sin resultado verificable (**No evidenciado**)

### Pagos y facturación
- https://www.mercadopago.com.ar/herramientas-para-vender/check-out — tarifas oficiales de Checkout Pro
- https://www.mercadopago.com.ar/developers/es/docs/checkout-pro/how-tos/integrate-marketplace — Checkout Pro vs Checkout API, split de pagos

### Calendario
- https://developers.google.com/workspace/calendar/api/guides/quota — cuotas oficiales de la Calendar API

### Software de turnería
- https://www.gendu.com.ar/planes — planes y packs de WhatsApp
- https://www.denpro.ar/ — plan Basic
- https://www.twilio.com/en-us/lp/sendgrid-vs-bird — SendGrid (prueba de 60 días, evidencia secundaria)

### Cambio
- https://www.bcra.gob.ar/estadisticas-indicadores — Tipo de Cambio Minorista BCRA, 1.545,12 ARS/USD (25/09/2026)
- https://www.lanacion.com.ar/dolar-hoy/ — dólar oficial venta $1.545

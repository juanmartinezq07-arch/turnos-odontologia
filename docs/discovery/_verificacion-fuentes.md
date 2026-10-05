# Verificación de fuentes — Discovery competitivo (turnero odontológico AR)

**Fecha de consulta:** 2026-10-02
**Método:** fetch directo (HTTP GET) de cada URL, sin caché de terceros. Cita textual literal.
**Criterio:** CONFIRMADO = la página dice lo que se afirma, con cita. PARCIAL = parte se confirma, parte no. REFUTADO = la página contradice o no existe el contenido. NO CONFIRMABLE = sin cita textual en la URL indicada (el dato no está en esa URL).

---

### V1 — dentalsoft.com.ar/precios

- **URL accesible:** Parcial. `https://www.dentalsoft.com.ar/precios` **no es una página de precios**: devuelve el sitio público de la clínica de demostración (`https://www.dentalsoft.com.ar/demo/`, título "Clínica Dental Demo", footer "Powered by **DentalSoft**"). Sin HTTP de error visible, pero el contenido NO es un pricing.
- **Estado:** CONFIRMADO (los datos) / **REFUTADO (la URL)
- **Evidencia textual** (de la home `https://www.dentalsoft.com.ar/`, sección "Planes que se adaptan a tu clínica"):
  - a) ¿Publica precios? → **Sí, en la home, no en `/precios`.**
  - b) Precios mensuales: **Gratis `$0/mes`**, **Gestión `$30.000/mes`**, **Pro `$60.000/mes`** (ambos planes pagos: "`+$10.000/mes por cada profesional adicional`"; "`Para más de 4 profesionales armamos un plan a medida`").
  - c) Pro automático vs. Gestión manual → confirmado literalmente:
    - Plan Gestión: "**Envío manual de recordatorios por WhatsApp** *Se abre WhatsApp con el mensaje de confirmación, recordatorio o pedido de reseña ya redactado, para que el equipo de la clínica lo revise y lo envíe con un clic. **No se manda nada de forma automática. Cada envío es gratuito.***"
    - Plan Pro: "**Recordatorios automáticos** *Meta cobra 0,026 USD por cada recordatorio de WhatsApp. Los recordatorios automáticos por Email son gratuitos.*"
  - d) Costo por recordatorio de WhatsApp en USD → **0,026 USD por recordatorio** (atribuido a Meta, no a DentalSoft). No aparece ningún otro monto en USD.
- **Corrección necesaria:** cambiar la URL citada de `https://www.dentalsoft.com.ar/precios` a `https://www.dentalsoft.com.ar/` (ancla de la sección "Planes"). `/precios` no publica precios: redirige al demo. Ojo con el demo: la landing `/demo` **sí** muestra "recordatorios automáticos" en un testimonio ("los recordatorios automáticos nos redujeron muchísimo las ausencias"), lo que puede inducir a error al leer esa página como evidencia de precios.

---

### V2 — agendapro.com/ar

- **URL accesible:** Sí (HTTP 200, contenido renderizado).
- **Estado:** PARCIAL
- **Evidencia textual:**
  - a) Página específica para Argentina → **Sí**. `<title>`: "**AgendaPro: Software & App para Agendar Turnos #1 en Argentina**"; nav con `NegociosFuncionalidadesAgentes IA[Precios](/ar/planes)` y `App Store` /id/ar/.
  - b) Teléfono local argentino → **Sí, pero sin prefijo +54**: "**Argentina** [11 5032 6351](tel:11 5032 6351)". Aparece como `11 5032 6351` (CABA), **no** como "+54 11".
  - c) "+20.000 negocios" → **Sí, en la home**: "**Más de 20.000 negocios como el tuyo ya confían en AgendaPro**" y en el bloque de métricas "**+20.000** negocios". **Ojo:** en `/ar/planes` la cifra es otra y distinta: "**+30.000 negocios en Latinoamérica están creciendo con AgendaPro**". No son la misma métrica ni la misma URL.
  - d) Recordatorios por WhatsApp → **Sí**: "**Recordatorios por WhatsApp y email**" (home, bloque "Gestión de turnos") y, en `/ar/planes`, add-on "**Envía recordatorios automáticos de citas por Whatsapp a tus clientes o pacientes. Desde $ 7.900 / mes ARS IVA incluido — 50 mensajes mensuales.**"
  - e) Reserva **sin crear cuenta / sin login / sin registro** → **NO APARECE**. No se encontró "sin login", "sin registro", "sin cuenta" ni equivalente en `/ar` ni en `/ar/planes`. Lo único cercano es la Push de Mercado Pago (otra empresa): "**No, no es necesario que tus clientes tengan cuenta en Mercado Pago para comprar en tu sitio.**" — no atribuible a AgendaPro.
- **Corrección necesaria:** (i) no escribir "teléfono +54 11": la página publica "11 5032 6351"; (ii) eliminar cualquier afirmación de "el paciente reserva sin crear cuenta" salvo que se cite otra URL de AgendaPro (help/academia); (iii) al citar "+20.000 negocios" dejar explícito que es de la home `/ar`, y que `/ar/planes` declara "+30.000 negocios en Latinoamérica".

---

### V3 — Ley 25.326 (Infoleg, texto actualizado)

- **URL accesible:** Sí (HTTP 200).
- **Estado:** CONFIRMADO
- **Evidencia textual:**
  - Vigencia: `<title>` = "**TEXTO ACTUALIZADO - Ley 25326 - HABEAS DATA | Argentina.gob.ar**"; encabezado "**Texto actualizado de la norma**"; JSON-LD `"description":"Texto de la norma con actualizaciones"`, `"legislationDate":"2000-10-04"`, `"datePublished":"2000-11-02"`. Ley sancionada 04-10-2000, Boletín Oficial 29517 del 02-11-2000. **Matiz:** la URL no usa literalmente la palabra "vigente"; el rótulo institucional es "TEXTO ACTUALIZADO".
  - Art. 2, dato sensible: "— **Datos sensibles: Datos personales que revelan origen racial y étnico, opiniones políticas, convicciones religiosas, filosóficas o morales, afiliación sindical e información referente a la salud o a la vida sexual.**" **Matiz:** la ley define la categoría "Datos sensibles"; la expresión literal "datos personales sensibles" NO aparece en la norma.
  - Consentimiento (Art. 5.1): "**El tratamiento de datos personales es ilícito cuando el titular no hubiere prestado su consentimiento libre, expreso e informado, el que deberá constar por escrito**, o por otro medio que permita se le equipare, de acuerdo a las circunstancias."
  - Excepciones al consentimiento (Art. 5.2): "a) …fuentes de acceso público irrestricto; b) …funciones propias de los poderes del Estado…; c) …listados cuyos datos se limiten a nombre, documento nacional de identidad, identificación tributaria o previsional, ocupación, fecha de nacimiento y domicilio; d) **Deriven de una relación contractual, científica o profesional del titular de los datos, y resulten necesarios para su desarrollo o cumplimiento**; e) …entidades financieras…"
  - Datos de salud (Art. 8): "**Los establecimientos sanitarios públicos o privados y los profesionales vinculados a las ciencias de la salud pueden recolectar y tratar los datos personales relativos a la salud física o mental de los pacientes** … respetando los principios del secreto profesional."
  - Art. 7.3: "**Queda prohibida la formación de archivos, bancos o registros que almacenen información que directa o indirectamente revele datos sensibles.**"
  - Art. 12.1: "**Es prohibida la transferencia de datos personales de cualquier tipo con países u organismos internacionales o supranacionales, que no propocionen niveles de protección adecuados.**"
- **Corrección necesaria:** usar la definición literal "Datos sensibles" del Art. 2 (no "datos personales sensibles" como si fuera texto de la ley). Si el informe afirma que el turno odontológico "cae en el supuesto d) del Art. 5.2" (relación profesional), esa exclusión es **interpretación**, no texto explícito de la ley para el caso odontológico: marcala como análisis. Agregar Art. 8 (secreto profesional) y Art. 12 (transferencia internacional) si el informe trata datos de salud o proveedores en el exterior.

---

### V4 — WhatsApp Business Platform Pricing

- **URL accesible:** Sí (HTTP 200).
- **Estado:** CONFIRMADO (modelo de cobro y categorías) / **NO CONFIRMABLE (precios concretos)**
- **Evidencia textual:**
  - Cobro por mensaje **entregado**: "**Businesses using our platform are charged on a per-message basis for each message we deliver to users**"; "**We charge when a message is delivered (not sent).**"; "**We charge based on who the message is sent to and the category of the message.**"
  - **Cuatro** categorías: "**There are four message categories on the WhatsApp Business Platform: marketing, utility, authentication, and service.**"
  - Ventana de 24 h / service sin cargo: "**When users message a business, this opens a 24-hour customer service window during which businesses can respond with service messages, at no charge. This window resets with each user message.**" y "**we do not charge for service messages**, or for utility messages businesses send in response to users."
  - Otras exenciones: "**for the following 3 days (72 hours), all of your messages are not charged**" (anuncio que hace clic a WhatsApp o botón de CTA de Facebook Page).
  - Precios: la sección "Message rates" es una **tabla interactiva** con selectores "Select the market, currency and message category" (Mercado: **Argentina** entre las opciones; Moneda: **Argentine Peso (ARS)** entre las opciones; Categoría: Authentication / Marketing / Utility / Service). En el HTML descargado **no hay ningún valor numérico de tarifa**: solo los títulos "Message rate:", "### Messages per month", "### What we charge". Los precios reales están en `https://developers.facebook.com/docs/whatsapp/pricing#rate-cards`.
- **Corrección necesaria:** no atribuir ningún precio por mensaje a esta URL; citar la rate card dedevelopers.facebook.com y fechar la consulta (las tarifas cambian por mercado/categoría y tienen volume tiers solo para **utility** y **authentication**). Si el informe afirma que "todo recordatorio automático por WhatsApp se cobra", corregir: los `service` dentro de la ventana de 24 h son gratuitos, y hay una ventana gratuita de 72 h tras un anuncio.

---

### V5 — gendu.com.ar/planes

- **URL accesible:** Sí (HTTP 200).
- **Estado:** CONFIRMADO
- **Evidencia textual:**
  - Precios en ARS, periodicidad mensual (con alternativa trimestral): "**Plan Básico — Gratis — Sin costo de suscripción**"; "**Plan Comercial — $9.100 — Por mes · Pesos argentinos**" (trimestral "$25.000 Total por 3 meses"); "**Plan Profesional — $14.400 — Por mes**" ("$38.800" trimestral); "**Plan Premium — $24.000 — Por mes**" ("$63.990" trimestral); "**Plan Master — $42.100 — Por mes · Pesos argentinos**" ("$113.670" trimestral).
  - Máximo: **$42.100/mes (Master)** → **confirmado**. Es el plan de mayor valor de los 5 listados.
  - Plan de costo $0: **sí, Plan Básico "Gratis"**. Todos los pagos tienen "**15 días de prueba gratis**".
  - Packs de WhatsApp (servicio adicional, **fuera** de la suscripción): "**50 recordatorios — $3.900 Por mes**"; "**100 recordatorios — $5.900 Por mes**"; "**300 recordatorios — $17.900 Por mes**"; "**1.000 recordatorios — $59.900 Por mes**", todos "**Adicional al precio de tu plan**". Envío: "**Gendu les recuerda el turno a tus clientes automáticamente, 24 horas antes, desde su número oficial.**"
  - Matiz crítico: en los planes pagos el envío por WhatsApp incluido es **manual de un clic**: "**Recordatorios por WhatsApp con un click** — Envío con un clic incluido en tu plan. ¿Preferís que se envíen solos? Sumá un pack de recordatorios automáticos, con costo adicional." Y: "**Los packs de recordatorios se contratan y se pagan por separado de la suscripción. Están disponibles para negocios con un plan pago.**"
- **Corrección necesaria:** los importes son correctos. Aclarar en el informe que (i) el pack de 1.000 recordatorios cuesta **$59.900/mes adicionales** (no $59.900 total), y (ii) el plan Básico gratis **no** incluye WhatsApp (solo "Recordatorios automáticos por email"), por lo que un odontólogo chico no tiene recordatorio por WhatsApp sin pagar.

---

### V6 — Mercado Pago Checkout (comisiones)

- **URL accesible:** Sí (HTTP 200).
- **Estado:** PARCIAL
- **Evidencia textual** (sección "Elegí como cobrar el dinero de tus ventas"):
  - "**En 35 días — Pagás 1,49% +IVA**"
  - "**En 18 días — Pagás 3,39% +IVA**"
  - "**En 10 días — Pagás 4,39%+IVA**"
  - "**Al instante — 6,29%+IVA**"
  - Complemento: "**Podés recibir tu dinero cuando quieras.** / **Vos elegís cuánto pagar.** / **Solo pagás por venta aprobada.**" y "**Los costos pueden variar de acuerdo a los impuestos provinciales.**"
  - FAQ: "**¿Cuánto cuesta recibir pagos? Los costos varían de acuerdo a: La provincia en donde esté registrado tu domicilio. El medio de pago que elija tu cliente. El plazo que definas para recibir tu dinero.**"
- **Corrección necesaria:** los dos porcentajes afirmados **se confirman** (4,39% + IVA a 10 días; 6,29% + IVA al instante), pero la afirmación es **incompleta**: la página publica **cuatro** tramos, no dos —falta "**1,49% + IVA a 35 días**" y "**3,39% + IVA a 18 días**". Ambigüedad adicional: la tabla **no está rotulada "Checkout Pro"**; está en la landing genérica de Checkout, después de la comparación Pro / Bricks / API, y la propia página advierte que el costo depende de provincia, medio de pago y plazo. Si el informe necesita atribuirlo a Checkout Pro específicamente, citar `mercadopago.com.ar/ayuda/33399` y fechar la consulta.

---

### V7 — bcra.gob.ar/estadisticas-indicadores

- **URL accesible:** Sí (HTTP 200).
- **Estado:** **NO CONFIRMABLE**
- **Evidencia textual:** la página es un **buscador/índice**, no un visor de valor. Incluye el link "**Tipo de Cambio Minorista ($ por USD) Comunicación B 9791 - Promedio vendedor**" → `/principales-variables-datos/?serie=7927`, con columnas "**Indicador | Fecha | Valor**", pero en el HTML recuperado **la celda Fecha y la celda Valor del tipo de cambio minorista vienen vacías** (se inyectan por JavaScript). No aparece "1.545,12" ni "25/09/2026" en ninguna parte de la página.
- **Corrección necesaria:** el valor **1.545,12 ARS/USD con fecha 25/09/2026 no puede sostenerse con esta URL**. Para confirmarlo hay que consultar la serie 7927 en `/principales-variables-datos/?serie=7927` o la página "**Tipo de cambio minorista (B 9791)**" (`/tipo-de-cambio-minorista/`), y citar el valor con la fecha de lectura, marcando que es un valor puntual y volátil (el informe no debe presentarlo como un tipo de cambio estable del proyecto).

---

### V8 — denpro.ar (precio plan Basic)

- **URL accesible:** Sí (HTTP 200).
- **Estado:** CONFIRMADO
- **Evidencia textual:**
  - Plan **Basic**: "**Basic — Para odontólogos independientes — $ 19.900/mes** — 1 usuario / Turnos y Calendario / Pacientes y Odontograma / Recetas / Comunicación / Análisis".
  - Plan **Team**: "**$ 29.900/mes** — **Usuarios ilimitados** …". Selector: "**Mensual Anual -15%**".
  - FAQ: "**DenPro ofrece dos planes: Basic a $ 19.900/mes para dentistas individuales y Team a $ 29.900/mes para clínicas con personal y usuarios ilimitados. Ahorre un 15 % con facturación anual. Sin costes ocultos, sin contratos a largo plazo. Comience con una prueba gratuita de 30 días — sin tarjeta de crédito.**"
  - Prueba: "**Prueba gratis durante 30 días**", "**no se requiere tarjeta de crédito**".
  - Dato adicional relevante para el informe (no verificado antes): "**Utilizamos cifrado AES-256, almacenamos todos los datos en centros de datos certificados ISO 27001 en la UE y cumplimos totalmente con el GDPR.**" Teléfonos del sitio: **+34 672 182 743** y WhatsApp **+421 944 063 272**. Razón social: "**DENPRO® is a registered EU trade mark of Elite Digital Services, LLC**". Cliente Count: "**Más de 50+ consultorios odontológicos confían en nosotros**".
- **Corrección necesaria:** el precio está confirmado, pero **hay que cambiar el encuadre del competidor**: DenPro no es una empresa argentina (soporte +34 España, marca de la UE, datos en la **UE**), y su página destaca **GDPR**, no Ley 25.326. Para un proyecto que almacena historia clínica en Argentina eso es un argumento competitivo (y un riesgo de Art. 12 Ley 25.326 sobre transferencia internacional). Si el informe lo describe como "competidor argentino local", corregir.

---

## Resumen de estado

| # | URL | Estado |
|---|-----|--------|
| V1 | dentalsoft.com.ar/precios | CONFIRMADO (datos) / REFUTADO (URL) |
| V2 | agendapro.com/ar | PARCIAL |
| V3 | Ley 25.326 (Infoleg) | CONFIRMADO |
| V4 | WhatsApp platform pricing | CONFIRMADO (modelo) / NO CONFIRMABLE (precios) |
| V5 | gendu.com.ar/planes | CONFIRMADO |
| V6 | mercadopago.com.ar/.../check-out | PARCIAL |
| V7 | bcra.gob.ar/estadisticas-indicadores | NO CONFIRMABLE |
| V8 | denpro.ar | CONFIRMADO |

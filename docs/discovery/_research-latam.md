# Investigación de sistemas de gestión y turnos odontológicos

**Proyecto:** Sistema de turnos odontológicos (agenda online, validación doble anti-solapamiento, notificaciones mockeadas)
**Fecha de consulta de todas las fuentes:** 2026-10-02
**Autor del documento:** Investigación de Discovery — Metodología I
**Versión:** 1.0

---

## 1. Alcance, método y criterios de evidencia

### 1.1 Objeto del estudio

Relevar los sistemas de software utilizados por consultorios y clínicas odontológicas de Latinoamérica y de internacionales, priorizando los que tienen presencia real y demostrable en Brasil, México, Colombia, Chile, Uruguay, Perú y Argentina, con foco especial en tres capacidades del proyecto:

1. **Reserva pública sin login** del paciente.
2. **Validación doble anti-solapamiento**: por profesional **y** por sillón / box.
3. **Notificaciones al paciente** (WhatsApp, correo, SMS) — en este proyecto mockeadas.

### 1.2 Criterios de evidencia aplicados

| Criterio | Regla aplicada |
|---|---|
| Fuente primaria | Solo páginas del proveedor (sitios oficiales, páginas de producto, páginas de precios, documentación). |
| Fuente secundaria | Directorios de reseñas (Capterra, GetApp, Software Advice) y prensa sectorial. Se marcan explícitamente como **fuente de terceros**. |
| Marketing del proveedor | Las cifras de adopción declaradas por el proveedor se rotulan como **"declarado por el proveedor"** y no se presentan como dato verificado. |
| Ausencia de evidencia | Cuando no se encuentra declaración explícita en fuente pública, se escribe literalmente **"No evidenciado"**. No se infiere la funcionalidad. |
| Deduplicación | Las variantes regionales de un mismo producto (por ejemplo, la edición argentina y la mexicana de un mismo software) se cuentan **una sola vez** como sistema. |
| Fechas | Toda fuente se cita con su URL y la fecha de consulta `2026-10-02`. |

### 1.3 Campos relevados por sistema

Se relevaron los siguientes 15 campos, más adopción, precios y strengths/limitaciones:

1. Nombre del producto
2. Proveedor / empresa
3. País de origen
4. Despliegue (nube / local / híbrido)
5. Vertical (odontológico puro / generalista con vertical odontológica)
6. Mercado declarado
7. Presencia en Argentina
8. Presencia en Brasil
9. Presencia en México
10. Presencia en Colombia
11. Presencia en Chile
12. Presencia en Uruguay
13. Presencia en Perú
14. Reserva pública sin login
15. Anti-solapamiento por profesional
16. Anti-solapamiento por sillón / box
17. Notificaciones WhatsApp
18. API / integraciones
19. App móvil
20. Seguridad y cumplimiento normativo
21. Precios públicos
22. Adopción declarada
23. Fortalezas
24. Limitaciones

---

## 2. Resumen comparativo

Leyenda: **Sí** = declarado explícitamente por el proveedor · **No** = el proveedor declara que no lo ofrece · **No evidenciado** = no se encontró declaración pública · **Parcial** = declarado con alcance distinto al del proyecto

| # | Sistema | Origen | Despliegue | Vertical | AR | BR | MX | CO | CL | UY | PE | Reserva sin login | Anti-solap. profesional | Anti-solap. sillón | WhatsApp | Precio público |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | AgendaPro | Argentina | Nube | Generalista (tiene vertical dental) | Sí | No evidenciado | Sí | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Sí | Sí (USD) |
| 2 | Doctoralia PRO | España | Nube | Generalista (servicios de salud) | Sí | No evidenciado | Sí | No evidenciado | Sí | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado |
| 3 | Dentalink | Chile | No evidenciado | Odontológico | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Sí | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No (cotización) |
| 4 | Clinicorp | Brasil | Nube | Odontológico | No evidenciado | Sí | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Sí (agendamiento online) | No evidenciado | No evidenciado | Sí | Sí (BRL) |
| 5 | Simples Dental | Brasil | Nube | Odontológico | No evidenciado | Sí | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Sí | No evidenciado | No evidenciado | Sí | No evidenciado |
| 6 | Prontuário Verde | Brasil | Nube | Odontológico + estética | No evidenciado | Sí | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Sí | No evidenciado | No evidenciado | Sí | No evidenciado |
| 7 | Dentalis | Brasil | Nube | Odontológico | No evidenciado | Sí | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Sí | No evidenciado |
| 8 | Sistema ClínicaPro | Brasil | Nube | Odontológico | No evidenciado | Sí | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Sí | No evidenciado |
| 9 | SimpleTurno | Argentina / Río de la Plata | Nube | Odontológico (rubro) | Sí | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Sí | Sí (plan gratuito) |
| 10 | Reservo | Argentina | Nube | Generalista (vertical odontología) | Sí | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Parcial | No evidenciado | No evidenciado | Sí | No evidenciado |
| 11 | UDENTIVA | Uruguay | Nube | Odontológico | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Sí | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado |
| 12 | DentalCitas (prototipo) | No evidenciado | Nube / autoalojable | Odontológico | No evidenciado | No evidenciado | Sí (indicio) | No evidenciado | No evidenciado | No evidenciado | No evidenciado | **Sí (declarado)** | **Sí (declarado)** | **Sí (declarado)** | No evidenciado | Sí (MXN) |
| 13 | Open Dental | EE. UU. | Local (servidor propio) | Odontológico | No evidenciado | Sí (usuarios) | No evidenciado | No evidenciado | No evidenciado | **Sí (usuarios + versión en español)** | **Sí (usuarios + versión en español)** | Parcial | No evidenciado | No evidenciado | No evidenciado | Sí (USD, variable) |
| 14 | Curve Dental | EE. UU. | Nube | Odontológico | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado |
| 15 | CareStack | EE. UU. | Nube | Odontológico | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Sí (tercero, USD) |
| 16 | NexHealth | EE. UU. | Nube (capa de experiencia) | Odontológico | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado |
| 17 | Weave | EE. UU. | Nube | Odontológico (telecomunicaciones) | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Sí (USD) |
| 18 | Oryx Dental | EE. UU. | Nube (Google Cloud) | Odontológico | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | Sí (USD/CAD) |
| 19 | Dentally | Reino Unido (Henry Schein One) | Nube | Odontológico | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado |
| 20 | Dentrix | EE. UU. | No evidenciado | Odontológico | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado | No evidenciado |

> **Nota sobre columnas de presencia por país:** la ausencia de marca se registra como **"No evidenciado"** y no como "no está". Solo se afirma presencia cuando existe una página del proveedor o un documento del proveedor que lo nombre explícitamente para ese país.

---

## 3. Sistemas de Latinoamérica — detalle

### 3.1 AgendaPro

- **Nombre:** AgendaPro
- **Proveedor:** AgendaPro Inc. (empresa con respaldidores visibles en su web: Y Combinator, Kayyak Ventures, Riverwood) — fuente: https://agendapro.com/ar (consulta: 2026-10-02)
- **País de origen:** Argentina. La portada argentina se titula "AgendaPro: Software & App para Agendar Turnos **#1 en Argentina**" y muestra teléfono local `11 5032 6351` bajo el bloque "Contacto — Argentina" — fuente: https://agendapro.com/ar (consulta: 2026-10-02)
- **Despliegue:** Nube. La sección de funcionalidades incluye el ícono "En la Nube" y la web declara "Una gestión que funciona en la nube" — fuente: https://agendapro.com/ar (consulta: 2026-10-02)
- **Vertical:** Generalista de servicios (estética, spa, salones, peluquerías, barberos,olen…) **con vertical odontológica**. Existe una página vertical propia: https://agendapro.com/es/dental/software-odontologico (consulta: 2026-10-02). La portada argentina lista el rubro "Clinicas" pero **no** odontología entre los rubros destacados — fuente: https://agendapro.com/ar (consulta: 2026-10-02)
- **Presencia:**
  - Argentina: **Sí** — https://agendapro.com/ar (consulta: 2026-10-02)
  - México: **Sí** — https://agendapro.com/mx/agenda-medica (consulta: 2026-10-02)
  - Brasil: **No evidenciado**
  - Colombia: **No evidenciado**
  - Chile: **No evidenciado**
  - Uruguay: **No evidenciado**
  - Perú: **No evidenciado**
- **Funciones declaradas (portada argentina):** turnos online, agenda digital, reservas 24/7, recordatorios por WhatsApp y email, IA para agendar ("Sofia"), base de datos de clientes, historial de turnos, ficha del cliente, promociones personalizadas, control de sesiones y tratamientos, control de stock, alertas de stock bajo, comisiones, integración con Google Reserve en Google My Business, LinkPro (tarjeta de presentación para redes), email marketing, Marketplace, IA de ventas ("Julia"), programas de lealtad y giftcards, pagos en línea, pago por link, cierres de caja, control de múltiples sucursales, reportes con IA, estadísticas, reporte de comisiones, rentabilidad — fuente: https://agendapro.com/ar (consulta: 2026-10-02)
- **Reserva pública sin login:** **No evidenciado.** La portada declara "Reservas 24/7" y ofrece un módulo denominado "Sitio de Reservas" con enlace `/ar/signup`, pero **en ningún punto de la página consultada se declara que el paciente pueda reservar sin crear una cuenta ni sin autenticarse** — fuente: https://agendapro.com/ar (consulta: 2026-10-02)
- **Anti-solapamiento por profesional:** **No evidenciado.** No se encontró ninguna mención textual a bloqueo de horarios duplicados, ni a validación de conflictos — fuente: https://agendapro.com/ar (consulta: 2026-10-02)
- **Anti-solapamiento por sillón / box:** **No evidenciado.** Ninguna mención a sillones, boxes, gabinetes o gabinetes/sillones como recurso de la agenda — fuente: https://agendapro.com/ar (consulta: 2026-10-02)
- **Notificaciones WhatsApp:** **Sí.** "Recordatorios por WhatsApp y email" — fuente: https://agendapro.com/ar (consulta: 2026-10-02). La edición mexicana también declara recordatorios por WhatsApp — fuente: https://agendapro.com/mx/agenda-medica (consulta: 2026-10-02)
- **API / integraciones:** **No evidenciado** para API pública. Se declara integración con Google Reserve / Google My Business — fuente: https://agendapro.com/ar (consulta: 2026-10-02)
- **App móvil:** **Sí.** Enlaces a App Store (ID 1218956898) y Google Play — fuente: https://agendapro.com/ar (consulta: 2026-10-02)
- **Seguridad / cumplimiento:** **No evidenciado.** La portada argentina no declara certificaciones ni alineación con normativa de datos personales (por ejemplo, Ley 25.326 de Protección de Datos Personales de Argentina)
- **Precios públicos:** **Sí.** La página regional de planes publica precio individual **USD 9/mes**, plan básico **USD 29/mes** y plan premium **USD 59/mes** — fuente: https://agendapro.com/es/planes (consulta: 2026-10-02). **Los precios específicos para Argentina no fueron verificados**: la portada argentina enlaza a `/ar/planes`, cuyo contenido no fue recuperado en esta consulta
- **Adopción declarada por el proveedor:** "+20.000 profesionales", "+135.000 millones de citas", "+100 países", y "Más de 20.000 negocios como el tuyo ya confían en AgendaPro" — fuente: https://agendapro.com/ar (consulta: 2026-10-02). La página en español para la vertical dental declara "+135.000 profesionales" y "+30.000 negocios" — fuente: https://agendapro.com/es/planes (consulta: 2026-10-02). Ambas cifras son **declaradas por el proveedor** y difieren entre páginas
- **Fortalezas:** Amplitud de presencia regional con páginas dedicate por país; precio público bajo; integración real con WhatsApp y con Google Reserve; control multi-sucursal; aplicación móvil propia; respaldo de inversores identificados
- **Limitaciones:** **No declara** anti-solapamiento por profesional ni por sillón; **no declara** reserva sin login; **no declara** cumplimiento normativo; el producto no es odontológico puro sino un gestor de servicios con vertical dental; los indicadores de ROI publicados en la portada argentina aparecen con valores en cero en el texto recuperado, por lo que no son utilizables como evidencia

### 3.2 Doctoralia PRO

- **Nombre:** Doctoralia PRO (producto de Docplanner)
- **Proveedor:** Docplanner — fuente: https://pro.doctoralia.com/ar (consulta: 2026-10-02)
- **País de origen:** España. Existe un sitio corporativo en español de España y páginas por país — fuente: https://pro.doctoralia.com/ar (consulta: 2026-10-02)
- **Despliegue:** Nube / SaaS — No evidenciado de forma explícita en la página argentina consultada
- **Vertical:** Generalista de servicios de salud. Es simultáneamente un **directorio de profesionales** y un **software de gestión**; el sitio declara integración con el perfil profesional público del directorio — fuente: https://pro.doctoralia.com/ar (consulta: 2026-10-02)
- **Presencia:**
  - Argentina: **Sí** — https://pro.doctoralia.com/ar (consulta: 2026-10-02)
  - Chile: **Sí** — declarada en la sección de agendas inteligentes de la versión española — fuente: https://pro.doctoralia.es/productos/doctoralia-pro-especialistas/mini-video/agenda-inteligente (consulta: 2026-10-02)
  - México: **Sí** — https://www.doctoralia.com.mx/ (consulta: 2026-10-02)
  - Brasil: **No evidenciado**
  - Colombia: **No evidenciado**
  - Uruguay: **No evidenciado**
  - Perú: **No evidenciado**
- **Funciones declaradas:** agenda online, lista de espera, campañas de captación, aplicación para el profesional, integración con el perfil público del directorio, recordatorios automáticos, ficha del paciente — fuentes: https://pro.doctoralia.com/ar y https://pro.doctoralia.es/productos/doctoralia-pro-especialistas/mini-video/agenda-inteligente (consulta: 2026-10-02)
- **Reserva pública sin login:** **No evidenciado.** El producto declara reserva online y gestión de lista de espera, pero no enuncia la ausencia de login para el paciente
- **Anti-solapamiento por profesional:** **No evidenciado**
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **No evidenciado.** El producto declara recordatorios automáticos y campañas, sin especificar canal
- **API / integraciones:** **No evidenciado** para API pública. Integra con el propio directorio de Docplanner
- **App móvil:** **Sí** — aplicación declarada para el profesional — fuente: https://pro.doctoralia.com/ar (consulta: 2026-10-02)
- **Seguridad / cumplimiento:** El proveedor declara "datos protegidos al 100%", cumplimiento de **RGPD** y alojamiento en **AWS** — fuente: https://pro.doctoralia.com/ar (consulta: 2026-10-02). Estas son **declaraciones del proveedor**, no certificaciones verificadas
- **Precios públicos:** **No evidenciado.** El producto ofrece un enlace "Ver precios" pero **no se obtuvo un monto público**. La ruta `https://pro.doctoralia.com/ar/precios` devolvió **HTTP 404** en la consulta del 2026-10-02
- **Adopción declarada por el proveedor:** No se capturó una cifra de clientes en la página argentina consultada — **No evidenciado**
- **Fortalezas:** Marca con alto reconocimiento en el mercado argentino; directorio integrado que aporta de pacientes; presencia en varios países de la región; respaldo europeo con declaración de RGPD
- **Limitaciones:** Producto de salud generalista, no odontológico; el directorio es un elemento diferenciador pero también una dependencia de terceros; **no publica monto de precio** en la página argentina; **no declara** anti-solapamiento ni sillones; **no declara** WhatsApp

### 3.3 Dentalink

- **Nombre:** Dentalink
- **Proveedor:** Dentalink — fuente: http://www.dentalink.net/ (consulta: 2026-10-02)
- **País de origen:** Chile. El sitio opera en español y declara cobertura para Chile y Latinoamérica — fuente: http://www.dentalink.net/ (consulta: 2026-10-02)
- **Despliegue:** **No evidenciado** en la página consultada
- **Vertical:** **Odontológico puro.** Es el único de la lista latinoamericana que declara explícitamente el odontograma y el periodontograma como módulos nativos — fuente: http://www.dentalink.net/ (consulta: 2026-10-02)
- **Presencia:** Chile: **Sí** — http://www.dentalink.net/ (consulta: 2026-10-02). Argentina, Brasil, México, Colombia, Uruguay, Perú: **No evidenciado**
- **Funciones declaradas:** gestión de agenda, ficha clínica, pagos, odontograma, periodontograma, automatización de recordatorios y de tareas administrativas, informes — fuente: http://www.dentalink.net/ (consulta: 2026-10-02)
- **Reserva pública sin login:** **No evidenciado**
- **Anti-solapamiento por profesional:** **No evidenciado**
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **No evidenciado.** Se declara automatización de recordatorios sin especificar canal
- **API / integraciones:** **No evidenciado**
- **App móvil:** **No evidenciado**
- **Seguridad / cumplimiento:** **No evidenciado**
- **Precios públicos:** **No.** El precio es **solo bajo cotización**; no hay lista de precios pública — fuente: http://www.dentalink.net/ (consulta: 2026-10-02)
- **Adopción declarada por el proveedor:** **No evidenciado.** No se capturó ninguna métrica de clientes
- **Fortalezas:** Único sistema con **vertical odontológica completa y explícita** entre los relevados de Latinoamérica; cubre el ciclo clínico (odontograma + periodontograma) y no solo la agenda; fuerte encaje con consultorios de odontología general y especialidades
- **Limitaciones:** Cobertura geográfica no evidenciada fuera de Chile; sin precios públicos; **sin declaración** de anti-solapamiento, reserva sin login, WhatsApp, API, app móvil ni cumplimiento normativo; información pública muy escasa (sitio de una sola página), lo que dificulta la verificación independiente

### 3.4 Clinicorp

- **Nombre:** Clinicorp
- **Proveedor:** Clinicorp — fuente: https://www.clinicorp.com/ (consulta: 2026-10-02)
- **País de origen:** Brasil — fuente: https://www.clinicorp.com/ (consulta: 2026-10-02)
- **Despliegue:** Nube. "Acesse o software Clinicorp direto pelo seu navegador no computador ou pelo aplicativo no celular e gerencie sua clínica mesmo à distância" — fuente: https://www.clinicorp.com/planos (consulta: 2026-10-02)
- **Vertical:** Odontológico puro, con extensiones para clínicas de estética y franquicias — fuente: https://www.clinicorp.com/planos (consulta: 2026-10-02)
- **Presencia:**
  - Brasil: **Sí** — "em todo o Brasil" — fuente: https://www.clinicorp.com/ (consulta: 2026-10-02)
  - Argentina, México, Colombia, Chile, Uruguay, Perú: **No evidenciado**
- **Funciones declaradas:** Agenda Inteligente (encuentra horarios disponibles, alerta de retorno, confirmación de presencia), Agendamento Online, CRM integrado, integração com WhatsApp, WhatsApp Web, envio de SMS, check-in con App do Paciente, app do profissional, app do paciente (Clini.me), múltiplos agendamentos, marcadores, relatórios de faltas y desmarcações, prontuário eletrônico, odontograma, controle protético, harmonização facial, gestão de casos de alinhadores, plataforma financeira, emissão de boletos/recibos/notas fiscais, controle de estoque, Clinicorp IA y Agentes Clinicorp IA, importación gratuita de datos de otro software en hasta 7 días hábiles, usuarios ilimitados — fuentes: https://www.clinicorp.com/, https://www.clinicorp.com/planos, https://www.clinicorp.com/melhor-software-odontologico-forms, https://www.clinicorp.com/post/agenda-personalizada-dentista (consulta: 2026-10-02)
- **Reserva pública sin login:** **Parcial.** El producto declara "Agendamento Online" como módulo del plan Standard y como diferenciador, pero **no enuncia** que el paciente pueda reservar sin cuenta — fuente: https://www.clinicorp.com/planos (consulta: 2026-10-02)
- **Anti-solapamiento por profesional:** **No evidenciado**
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **Sí.** "Integração com Whatsapp" y "WhatsApp Web" en los planes Standard y Premium; confirmación automática de consulta por WhatsApp — fuentes: https://www.clinicorp.com/planos y https://www.clinicorp.com/agenda-cheia-que-converte (consulta: 2026-10-02)
- **API / integraciones:** **No evidenciado** para API pública. Integra con Cloudia — fuente: https://www.clinicorp.com/planos (consulta: 2026-10-02)
- **App móvil:** **Sí** — app del profesional y app del paciente (Clini.me) — fuente: https://www.clinicorp.com/planos (consulta: 2026-10-02)
- **Seguridad / cumplimiento:** **No evidenciado**
- **Precios públicos:** **Sí.**
  - Plan **Standard: R$ 159,90 / mes** — "Para consultórios que querem otimizar processos"
  - Plan **Premium: R$ 369,90 / mes** — "Para clínicas com visão 360º da gestão"
  - Existe además un plan **Enterprise** y combos con IA, ambos **bajo cotización**
  - El proveedor advierte que "os valores de implementação, mensalidade e taxas adicionais… podem ser reajustados com o tempo"
  - Fuente: https://www.clinicorp.com/planos (consulta: 2026-10-02)
- **Adopción declarada por el proveedor:** "+200 mil usuários ativos no sistema Clinicorp", "+R$19 bi faturados dentro da plataforma", "100M de pacientes atendidos", "+30 mil clínicas odontológicas em todo o Brasil", y en una página de blog "presente em mais de 30 mil clínicas" — fuentes: https://www.clinicorp.com/ y https://www.clinicorp.com/post/agenda-personalizada-dentista (consulta: 2026-10-02). Todas son **cifras declaradas por el proveedor**, sin verificación independiente localizada
- **Fortalezas:** Mayor cobertura funcional odontológica de Latinoamérica; **precios públicos y bajos** en reales; integración de WhatsApp de primer nivel (API y WhatsApp Web); apps de paciente y profesional; importación de datos gratuita; suite financiero con emisión de notas fiscales; casos de uso publicados con nombre de clínica y profesional
- **Limitaciones:** Cobertura **exclusiva de Brasil**; **no declara** anti-solapamiento por profesional ni por sillón; **no declara** reserva sin login; **no declara** cumplimiento normativo (por ejemplo, LGPD) ni API pública; cifras de adopción no verificadas; competidor con dueño de la agenda pero sin evidencia de componente clínico de sillón

### 3.5 Simples Dental

- **Nombre:** Simples Dental
- **Proveedor:** Simples Dental — fuente: https://www.simplesdental.com/ (consulta: 2026-10-02)
- **País de origen:** Brasil. "+11 Anos atendendo o mercado odontológico" — fuente: https://www.simplesdental.com/ (consulta: 2026-10-02)
- **Despliegue:** **No evidenciado** explícitamente
- **Vertical:** Odontológico puro — fuente: https://www.simplesdental.com/ (consulta: 2026-10-02)
- **Presencia:** Brasil: **Sí** — fuente: https://www.simplesdental.com/ (consulta: 2026-10-02). Resto de países: **No evidenciado**
- **Funciones declaradas:** Agenda Online con confirmación automática de consulta por WhatsApp, prontuário digital con histórico clínico e imágenes, gestión financiera con boletos y Pix, marketing y ventas, IA para dentistas, WhatsApp para clínica, assinatura eletrônica, Secretária IA para agendamiento 24/7 por WhatsApp — fuente: https://www.simplesdental.com/ (consulta: 2026-10-02)
- **Reserva pública sin login:** **No evidenciado.** Declara "agenda online" y "agendamentos 24/7 via WhatsApp", sin specifyar ausencia de login
- **Anti-solapamiento por profesional:** **No evidenciado**
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **Sí** — confirmación automática de consulta por WhatsApp y Secretary IA por WhatsApp — fuente: https://www.simplesdental.com/ (consulta: 2026-10-02)
- **API / integraciones:** **No evidenciado**
- **App móvil:** **No evidenciado** en la página consultada
- **Seguridad / cumplimiento:** **No evidenciado**
- **Precios públicos:** **No evidenciado.** La página ofrece "Teste Grátis por 7 dias" y "Não precisa de cartão de crédito", sin monto público
- **Adopción declarada por el proveedor:** "+100mil Profissionais ativos na plataforma", "+19mil Clínicas atendidas", "+60mi De pacientes cadastrados com atendimentos", "+11 Anos"; valoración declarada en App Store "4.8/5" — fuente: https://www.simplesdental.com/ (consulta: 2026-10-02). El proveedor se autodenomina "el software odontológico número uno en América Latina", **afirmación de marketing sin respaldo verificable** en fuente independiente
- **Fortalezas:** Posicionamiento declarado en toda América Latina (no solo Brasil); integración profunda de WhatsApp como canal de reserva y no solo de recordatorio; Pix como medio de pago local; prueba gratuita sin tarjeta
- **Limitaciones:** Toda la evidencia pública es de **una sola página**; cobertura fuera de Brasil **no evidenciada**; **sin precios públicos**; **sin declaración** de anti-solapamiento, sillones, API, app móvil ni cumplimiento normativo; la afirmación de liderazgo regional no está respaldada

### 3.6 Prontuário Verde

- **Nombre:** Prontuário Verde
- **Proveedor:** Prontuário Verde — fuente: https://www.prontuarioverde.com.br/ (consulta: 2026-10-02)
- **País de origen:** Brasil (dominio `.com.br`) — fuente: https://www.prontuarioverde.com.br/ (consulta: 2026-10-02)
- **Despliegue:** **No evidenciado** explícitamente
- **Vertical:** Odontológico, médico y estético — "Software para clínicas odontológicas, médicas e estéticas" — fuente: https://www.prontuarioverde.com.br/ (consulta: 2026-10-02)
- **Presencia:** Brasil: **Sí** — fuente: https://www.prontuarioverde.com.br/ (consulta: 2026-10-02). Resto: **No evidenciado**
- **Funciones declaradas:** Agenda Online, CRM, Verdesk, Agente de Vendas y Agendamiento (atención 24/7 por voz y texto), Agente de Copiloto del Profissional (comandos de voz por WhatsApp), Agente Financeiro (envío de foto o PDF de nota fiscal), Planejador de Tratamentos IA, prontuário con IA (OVYVA), prescrição digital, teleconsultas, assinatura digital, gestão financeira, convênios, nota fiscal, contratos e termos, estoque, **APIs e integração**, redes e franquias, integração com Google Agenda, **lista de antecipación** (avisa cuando surge una vacante para quien pidió hora más temprana), check-in móvil, aplicación en App Store y Google Play — fuente: https://www.prontuarioverde.com.br/ (consulta: 2026-10-02)
- **Reserva pública sin login:** **No evidenciado**
- **Anti-solapamiento por profesional:** **No evidenciado**
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **Sí** — "Integração com WhatsApp e tudo funcionando de forma automática e sincronizada", y copiloto con comandos de voz por WhatsApp — fuente: https://www.prontuarioverde.com.br/ (consulta: 2026-10-02)
- **API / integraciones:** **Sí.** El producto lista explícitamente **"APIs e integração"** entre sus funcionalidades — fuente: https://www.prontuarioverde.com.br/ (consulta: 2026-10-02)
- **App móvil:** **Sí** — "Baixar na App Store / Disponível no Google Play" — fuente: https://www.prontuarioverde.com.br/ (consulta: 2026-10-02)
- **Seguridad / cumplimiento:** **No evidenciado**
- **Precios públicos:** **No evidenciado.** La web ofrece "Agendar demonstração" sin monto
- **Adopción declarada por el proveedor:** **No evidenciado.** La sección "Nossos números" no exhibe cifras en el texto recuperado
- **Fortalezas:** Es el único/provider con **API explícita** entre los Implementingación Graphs; incorpora IA conversacional como funcional de producto y no como(add-on); lista de anticipación (waitlist) que attacking la ociosidad de agenda; atención 24/7 por voz y texto
- **Limitaciones:** Cobertura solo Brasil; **sin precios**; **sin declaración** de anti-solapamiento, sillones ni reserva sin login; **sin declaración** de cumplimiento normativo; muy poca información pública verificable (página única)

### 3.7 Dentalis

- **Nombre:** Dentalis
- **Proveedor:** Dentalis — fuente: https://www.dentalis.com.br/ (consulta: 2026-10-02)
- **País de origen:** Brasil (dominio `.com.br`) — fuente: https://www.dentalis.com.br/ (consulta: 2026-10-02)
- **Despliegue:** Nube. "100% online, seguro e acessível" — fuente: https://www.dentalis.com.br/ (consulta: 2026-10-02)
- **Vertical:** Odontológico. Incluye el producto **DentalMax** para "redes de clínicas odontológicas" — fuente: https://www.dentalis.com.br/ (consulta: 2026-10-02)
- **Presencia:** Brasil: **Sí** — fuente: https://www.dentalis.com.br/ (consulta: 2026-10-02). Resto: **No evidenciado**
- **Funciones declaradas:** prontuário electrónico disponible en celular y notebook, odontograma digital con funciones señalizadoras, imágenes y anamnesis, agenda integrada con visibilidad de citas por día/semana/quincena/mes, **confirmación de consultas por WhatsApp**, tiempo de espera y de atendimento, control de patients faltantes, gestão financeira con emisión de boletos y pagos, cálculo de comisiones, conta digital para pagos y emissão de boletos, construcción de sitio web con agendamento integrado, DentalFlex (versión de gestión), DentalMax (redes) — fonte: https://www.dentalis.com.br/ (consulta: 2026-10-02)
- **Reserva pública sin login:** **Parcial.** Declara "Construção de site com agendamento integrado junto ao software", es decir un sitio con reserva online; **no enuncia** ausencia de login — fuente: https://www.dentalis.com.br/ (consulta: 2026-10-02)
- **Anti-solapamiento por profesional:** **No evidenciado**
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **Sí** — "Confirme consultas via WhatsApp para reduzir faltas" — fonte: https://www.dentalis.com.br/ (consulta: 2026-10-02)
- **API / integraciones:** **No evidenciado**
- **App móvil:** **Sí** — "prontuário eletrônico… aberto ao mesmo tempo no celular e no notebook" — fonte: https://www.dentalis.com.br/ (consulta: 2026-10-02)
- **Seguridad / cumplimiento:** **No evidenciado**. La web afirma "seguro" en lenguaje publicitario, sin certificación asociada
- **Precios públicos:** **No evidenciado**
- **Adopción declarada por el proveedor:** **No evidenciado.** Los contadores de la sección "Dentalis em números" se recuperaron con valores "0" (marcadores sin renderizar), por lo que **no son utilizables como evidencia**
- **Fortalezas:** Agenda integrada con agenda web del propio consultorio, lo que permite reserva directa desde el sitio del profesional; odontograma digital con imágenes; modelo de producto por tiers (Flex / Max) adapted a consultorios individuales y a redes
- **Limitaciones:** **Sin precios**; **sin declaración** de anti-solapamiento, sillones, API ni cumplimiento; cobertura exclusiva de Brasil; métricas de adopter inaccesibles en la página

### 3.8 Sistema ClínicaPro

- **Nombre:** Sistema ClínicaPro
- **Proveedor:** ClínicaPro — fuente: https://sistemaclinicopro.com.br/ (consulta: 2026-10-02)
- **País de origen:** Brasil (dominio `.com.br`) — fuente: https://sistemaclinicopro.com.br/ (consulta: 2026-10-02)
- **Despliegue:** Nube — **No evidenciado** explícitamente
- **Vertical:** Odontológico — fuente: https://sistemaclinicopro.com.br/ (consulta: 2026-10-02)
- **Presencia:** Brasil: **Sí** — fuente: https://sistemaclinicopro.com.br/ (consulta: 2026-10-02). Resto: **No evidenciado**
- **Funciones declaradas:** gestión de agenda, gestión de pacientes, gestión financiera, recordatorios automáticos por WhatsApp, SMS y correo electrónico, prueba gratuita de 7 días — fuente: https://sistemaclinicopro.com.br/ (consulta: 2026-10-02)
- **Reserva pública sin login:** **No evidenciado**
- **Anti-solapamiento por profesional:** **No evidenciado**
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **Sí** — recordatorios por WhatsApp, SMS y email — fuente: https://sistemaclinicopro.com.br/ (consulta: 2026-10-02)
- **API / integraciones:** **No evidenciado**
- **App móvil:** **No evidenciado**
- **Seguridad / cumplimiento:** **No evidenciado**
- **Precios públicos:** **No evidenciado**. Solo "prueba de 7 días"
- **Adopción declarada por el proveedor:** **No evidenciado**
- **Advertencia de identidad:** existen múltiples productos llamados "ClinicPro" / "ClínicaPro" en el mercadoocumented regionally. El perfil relevado corresponde al dominio `sistemaclinicopro.com.br`. No fue posible descartar homónimos con certeza
- **Fortalezas:** Cobertura de los tres canales de notificación (WhatsApp, SMS, email) en un mismo producto; prueba gratuita de 7 días que reduce la fricción de adopción
- **Limitaciones:** Evidencia pública muy reducida (página única, sin documentación); sin precios; sin declaration de anti-solapamiento, sillones, API, app móvil ni cumplimiento; ambigüedad de identidad con otros productos de nombre similar

### 3.9 SimpleTurno

- **Nombre:** SimpleTurno
- **Proveedor:** SimpleTurno — fuente: https://simpleturno.com/rubros/odontologia (consulta: 2026-10-02)
- **País de origen:** Argentina / Región del Río de la Plata. El sitio está en español rioplatense ("Reservan", "Pedí", "Redují", "avisos") — fuente: https://simpleturno.com/rubros/odontologia (consulta: 2026-10-02)
- **Despliegue:** Nube — implícito en "desde tu link"; **No evidenciado** de forma explícita
- **Vertical:** Producto generalista de turnos con **rubro odontología** comolanding específica — fuente: https://simpleturno.com/rubros/odontologia (consulta: 2026-10-02)
- **Presencia:**
  - Argentina: **Sí** — fuente: https://simpleturno.com/rubros/odontologia (consulta: 2026-10-02)
  - Uruguay, Brasil, México, Colombia, Chile, Perú: **No evidenciado**
- **Funciones declaradas:** Agenda online 24/7 accessible desde un enlace propio, recordatorios automáticos por WhatsApp antes de cada turno, señas cobradas al reservar mediante MercadoPago, agenda separada por profesional con tipos de consulta propios (odontólogo general, ortodoncista, periodoncista) — fuente: https://simpleturno.com/rubros/odontologia (consulta: 2026-10-02)
- **Reserva pública sin login:** **No evidenciado.** Declara que "los pacientes reservan… desde tu link, sin saturar el teléfono", pero no enuncia ausencia de cuenta ni de autenticación
- **Anti-solapamiento por profesional:** **Parcial.** El producto declara agendas separadas y tipos de consulta por profesional, lo que implica un modelo de disponibilidad por profesional; **no enuncia** ninguna validación de conflictos ni bloqueo explícito de doble reserva
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **Sí** — "Recordatorios por WhatsApp / Avisos automáticos antes de cada turno"; el proveedor declara "Reducí el ausentismo hasta un 80%", **afirmación de marketing del proveedor** — fuente: https://simpleturno.com/rubros/odontologia (consulta: 2026-10-02)
- **API / integraciones:** **Parcial** — integración declarada con **MercadoPago**; otras integraciones **No evidenciado** — fuente: https://simpleturno.com/rubros/odontologia (consulta: 2026-10-02)
- **App móvil:** **No evidenciado**
- **Seguridad / cumplimiento:** **No evidenciado**
- **Precios públicos:** **Parcial.** "Gratis para empezar. Plan gratuito sin límite de tiempo. Sin tarjeta de crédito." Los planes pagos **No evidenciado** — fuente: https://simpleturno.com/rubros/odontologia (consulta: 2026-10-02)
- **Adopción declarada por el proveedor:** **No evidenciado**
- **Fortalezas:** **El competidor más cercano al proyecto en el mercado argentino:** precio de entrada gratuito y sin tarjeta, reserva por enlace propio, modelos de agenda por profesional con tipos de consulta diferenciados, señas que reducen el ausentismo, y WhatsApp como canal de recordatorio
- **Limitaciones:** **No declara** anti-solapamiento ni sillones; **no declara** reserva sin login; **sin planes pagos documentados**; sin app móvil, API pública ni declaración de cumplimiento; el producto se presenta como "Sin funciones innecesarias", lo que implica un alcance funcional deliberadamente reducido

### 3.10 Reservo

- **Nombre:** Reservo
- **Proveedor:** Reservo — fuente: https://reservo.com.ar/ (consulta: 2026-10-02)
- **País de origen:** Argentina. Dominio `.com.ar` y contacto local — fuente: https://reservo.com.ar/ (consulta: 2026-10-02)
- **Despliegue:** Nube. "Podrás acceder a tu agenda y gestionar tus citas desde cualquier dispositivo" — fuente: https://reservo.com.ar/ (consulta: 2026-10-02)
- **Vertical:** Generalista de servicios de salud **con vertical de Odontología** que gestiona "fichas clínicas, diagnósticos, presupuestos y odontogramas" — fuente: https://reservo.com.ar/ (consulta: 2026-10-02)
- **Presencia:**
  - Argentina: **Sí** — https://reservo.com.ar/ (consulta: 2026-10-02)
  - Uruguay, Brasil, México, Colombia, Chile, Perú: **No evidenciado**
- **Funciones declaradas:** agenda online 24/7, confirmación automática de citas por correo y WhatsApp, vista en tiempo real de la agenda propia y del equipo, reportaría, control de insumos y finanzas, integración con MercadoPago, WooCommerce, Vambe y agenda externa, vertical de Odontología con ficha clínica, diagnóstico, presupuesto y odontograma, y en el rubro de psicología permite al paciente "reservar y pagar en línea" — fuente: https://reservo.com.ar/ (consulta: 2026-10-02)
- **Reserva pública sin login:** **Parcial.** Para el rubro de psicología el proveedor declara que "Permite a sus pacientes que conozcan su disponibilidad horaria, que reserven y paguen en línea"; para odontología la web describe agenda online 24/7 pero **no enuncia** ausencia de login — fuente: https://reservo.com.ar/ (consulta: 2026-10-02)
- **Anti-solapamiento por profesional:** **No evidenciado**
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **Sí** — "Confirmación por WhatsApp" y "Recibe confirmación automática de las citas por correo y WhatsApp" — fuente: https://reservo.com.ar/ (consulta: 2026-10-02)
- **API / integraciones:** **Sí** — el producto se posiciona explícitamente sobre integraciones: "Optimiza tu práctica médica integrando Reservo con otras aplicaciones" (MercadoPago, WhatsApp, Calendar, WooCommerce, Vambe, Agenda) — fuente: https://reservo.com.ar/ (consulta: 2026-10-02)
- **App móvil:** **No evidenciado**
- **Seguridad / cumplimiento:** **No evidenciado**
- **Precios públicos:** **No evidenciado**. La página invita a solicitar asistencia de un ejecutivo
- **Adopción declarada por el proveedor:** **No evidenciado**
- **Fortalezas:** Vertical odontológica con **odontograma y presupuesto**; integración con **MercadoPago** (medio de pago dominante en la región) y con WooCommerce; agenda compartida con el equipo; arquitectura pensada desde la integración
- **Limitaciones:** Sin precios públicos; **no declara** anti-solapamiento ni sillones; sin app móvil; sin declaración de cumplimiento normativo; cobertura fuera de Argentina no evidenciada; página corporativa sin documentación técnica

### 3.11 UDENTIVA

- **Nombre:** UDENTIVA
- **Proveedor:** UDENTIVA — fuente: https://udentiva.com/pt-uy (consulta: 2026-10-02)
- **País de origen:** Uruguay. La página declara "Uruguay · UYU" y "La plataforma de gestión dental inteligente para clínicas en Uruguay" — fuente: https://udentiva.com/pt-uy (consulta: 2026-10-02)
- **Despliegue:** Nube. "Todo lo que la Sua Clínica Precisa numa Única Plataforma" y "7/24 Suporte" — fuente: https://udentiva.com/pt-uy (consulta: 2026-10-02)
- **Vertical:** Odontológico puro — fuente: https://udentiva.com/pt-uy (consulta: 2026-10-02)
- **Presencia:**
  - Uruguay: **Sí** — https://udentiva.com/pt-uy (consulta: 2026-10-02)
  - Argentina, Brasil, México, Colombia, Chile, Perú: **No evidenciado**
- **Funciones declaradas:** Gestão de Pacientes (historial de tratamientos y documentos), Gestão de Consultas ("Reduza os intervalos com marcações online, lembretes e gestão de calendário"), Finanças e Cobrança, **Turismo de Saúde** (turismo dental internacional con centro de operaciones, plan de tratamiento, alojamiento, transferencias), Panéis de Gestão multi-sucursal con KPIs, Painel de relatórios con análisis por médico y por filial — fuente: https://udentiva.com/pt-uy (consulta: 2026-10-02)
- **Reserva pública sin login:** **No evidenciado**
- **Anti-solapamiento por profesional:** **No evidenciado**
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **No evidenciado.** Se declaran "lembretes" sin especificar canal
- **API / integrações:** **No evidenciado**
- **App móvil:** **No evidenciado**
- **Seguridad / cumplimiento:** **Sí (declarado).** El proveedor declara conformidad con la **Ley N.º 18.331 de Protección de Datos Personales** de Uruguay y "isolamento total de datos por clínica" — fuente: https://udentiva.com/pt-uy (consulta: 2026-10-02). Es una **declaración del proveedor**
- **Precios públicos:** **No evidenciado**. Solo "Comece Grátis" y "Assistir à Apresentação", sin monto
- **Adopción declarada por el proveedor:** "Mais de 10.000 pacientes e mais de 100 clínicas confiam em nós", "10.000+ Registos de Pacientes", "100+ Clínica", "%99,9 Tempo de Atividade do Sistema" — fuente: https://udentiva.com/pt-uy (consulta: 2026-10-02). Cifras **declaradas por el proveedor**
- **Advertencia de verosimilitud:** la página mezcla español y portugués en el mismo texto (por ejemplo, "Registos de Pacientes" con "Clínica" en contexto español) y presenta cifras sin documentación de respaldo. Se clasifica como **evidencia de baja confiabilidad** y no debe usarse para decisiones de arquitectura sin verificación adicional
- **Fortalezas:** Único sistema relevado con declaración explícita de cumplimiento de la **legislación(True)** de datos personales latinoamericana (Ley 18.331 de Uruguay); modelo de **turismo de salud** interesante para el contexto del proyecto académico; aislamiento de datos por clínica
- **Limitaciones:** Evidencia pública inconsistente y de baja confiabilidad; sin precios; **sin declaración** de anti-solapamiento, sillones, WhatsApp, API o app; cobertura limitada a Uruguay

### 3.12 DentalCitas (prototipo open source / autoalojable)

- **Nombre:** DentalCitas
- **Proveedor:** Proyecto independiente — **No evidenciado** (no se identificó entidad legal, equipo ni empresa) — fuente: https://dental.rasalopa.dev/ (consulta: 2026-10-02)
- **País de origen:** **No evidenciado.** El dominio activo es `.dev` y los precios se expresan en **MXN (pesos mexicanos)**, lo que sugiere origen mexicano, pero no hay declaración formal
- **Despliegue:** Nube y autoalojable — **No evidenciado** explícitamente
- **Vertical:** Odontológico — fuente: https://dental.rasalopa.dev/ (consulta: 2026-10-02)
- **Presencia:** México: **indicio** por precios en MXN. Argentina, Brasil, Colombia, Chile, Uruguay, Perú: **No evidenciado**
- **Funciones declaradas:** reserva de citas odontológicas; los tres puntos declarados por el propio producto son **"sin crear cuenta"**, **"Sin citas solapadas"** y **"Cada horario solo puede reservarse una vez"** — fuente: https://dental.rasalopa.dev/ (consulta: 2026-10-02)
- **Reserva pública sin login:** **Sí (declarado).** El proveedor declara explícitamente **"sin crear cuenta"** — fuente: https://dental.rasalopa.dev/ (consulta: 2026-10-02)
- **Anti-solapamiento por profesional:** **Sí (declarado).** "Sin citas solapadas" — fuente: https://dental.rasalopa.dev/ (consulta: 2026-10-02)
- **Anti-solapamiento por sillón / box:** **Parcial.** El proveedor declara "Cada horario solo puede reservarse una vez", lo que garantiza **unicidad de la franja horaria**; **no** enuncia una noción explícita de sillón o box como recurso — fuente: https://dental.rasalopa.dev/ (consulta: 2026-10-02)
- **Notificaciones WhatsApp:** **No evidenciado**
- **API / integraciones:** **No evidenciado**
- **App móvil:** **No evidenciado**
- **Seguridad / cumplimiento:** **No evidenciado**
- **Precios públicos:** **Sí.**
  - Plan **Free**: hasta 30 citas por mes
  - Plan **Pro**: **MXN $299 / mes**
  - Plan **Ultimate**: prueba de 14 días
  - Fuente: https://dental.rasalopa.dev/ (consulta: 2026-10-02)
- **Adopción declarada:** **No evidenciado.** No se declaran usuarios, clínicas ni instalaciones
- **Fortalezas:** **Es el único sistema del universo relevado que declara los tres requisitos centrales del proyecto:** reserva sin cuenta, no solapamiento y exclusividad de la franja horaria. Precios públicos y muy bajos; modelo de entrada gratuito
- **Limitaciones:** Sin entidad identificable, sin documentación técnica pública, sin adopción declarada, sin API, sin app móvil, sin WhatsApp y sin declaración de cumplimiento; el "anti-solapamiento por sillón" es solo implícito (exclusividad de horario, no de recurso físico); su Ronnie Status es de prototipo, por lo que no es un competidor comercial maduro

---

## 4. Sistemas internacionales — detalle

### 4.1 Open Dental

- **Nombre:** Open Dental
- **Proveedor:** Open Dental Software — fuente: https://www.opendental.com/ (consulta: 2026-10-02)
- **País de origen:** Estados Unidos. "Open Dental headquarters is located in the United States" — fuente: https://www.opendental.com/site/countries.html (consulta: 2026-10-02)
- **Despliegue:** **Local con servidor propio** (no cloud). Es la excepción del bloque internacional — fuente: https://www.opendental.com/ (consulta: 2026-10-02)
- **Vertical:** Odontológico puro — fuente: https://www.opendental.com/ (consulta: 2026-10-02)
- **Presencia:**
  - Uruguay: **Sí.** El proveedor publica un contacto de soporte en español para Uruguay: "Uruguay - Gonzalo Rocha" — fuente: https://www.opendental.com/site/countries.html (consulta: 2026-10-02)
  - Perú: **Sí.** El proveedor publica contacto de soporte en español para Perú: "Spanish, Peru - Anatoly Alexei Pedemonte Ku" — fuente: https://www.opendental.com/site/countries.html (consulta: 2026-10-02)
  - Brasil: **Sí (usuarios).** El proveedor publica contacto de soporte en Brasil: "**Brazil ** Nilo Silva, Tel: +55 11 3835-4626" — fuente: https://www.opendental.com/site/countries.html (consulta: 2026-10-02)
  - Argentina, México, Colombia, Chile: **No evidenciado**
- **Funciones declaradas:** gestión de agenda, odontograma, prontuario, portales de pacientes, Web Sched (reserva online), mensajería, y un conjunto amplio de herramientas clínicas y administrativas — fuente: https://www.opendental.com/ (consulta: 2026-10-02)
- **Reserva pública sin login:** **Parcial.** El producto ofrece **Web Sched**, un módulo de reserva online para pacientes; **no se récupitó** en esta consulta una declaración explícita de que la reserva sea sin login — fuente: https://www.opendental.com/ (consulta: 2026-10-02)
- **Anti-solapamiento por profesional:** **No evidenciado** en fuente pública de proveedor
- **Anti-solapamiento por sillón / box:** **No evidenciado** en fuente pública de proveedor. La documentación técnica de Open Dental sí contiene el concepto de "ops"/"sillones" en su modelo de datos interno, pero **no se ha recovering** aquí una declaración pública que lo presente como validación anti-solapamiento
- **Notificaciones WhatsApp:** **No evidenciado**
- **API / integraciones:** **No evidenciado** en esta consulta
- **App móvil:** **No evidenciado**
- **Seguridad / cumplimiento:** **No evidenciado** en esta consulta
- **Precios públicos:** **Sí, aunque variables.** Open Dental publica una tabla de honorarios de soporte y servicios en **USD**; el monto depende del número de ubicaciones y de profesionales. Para clientes fuera de EE. UU. "Fees and support options for countries outside of the United States are reduced because of features, time zones, and/or language differences. All fees are in USD" — fuentes: https://www.opendental.com/site/fees.html y https://www.opendental.com/site/countries.html (consulta: 2026-10-02)
- **Adopción declarada:** **No evidenciado** en esta consulta
- **Fortalezas:** **El único sistema internacional con presencia declarada y documentada en Latinoamérica** (Uruguay, Perú y Brasil), incluyendo **contactos de soporte en español** y **versiones en español**; precios públicos; modelo local permite  operation sin dependencia del proveedor
- **Limitaciones:** Despliegue local implica costos de servidor y de IT (curva de startup de $20K y $500/mes es una cifra declarada por **Curve**, no por Open Dental — ver §4.2); soporte **limitado a usuarios angloparlantes** según el propio proveedor: "Open Dental support is limited to English-speaking users"; **no declara** anti-solapamiento en fuente pública; sin WhatsApp; modelo de licencia local no trasladable a un proyecto web

### 4.2 Curve Dental

- **Nombre:** Curve Dental (producto: Curve Hero / SuperHero)
- **Proveedor:** CD Newco, LLC (sede en Alpharetta, Georgia, EE. UU.;/CD Newco Canada Inc en Calgary; oficinas también en Aberdeen,-Escocia) — fuentes: https://www.curvedental.com/ y http://www.prnewswire.com/news-releases/curve-dental-announces-strategic-integration-partnership-with-dentalhq-setting-new-standard-for-connected-practice-management-302604329.html (consulta: 2026-10-02)
- **País de origen:** Estados Unidos — fuente: https://www.curvedental.com/ (consulta: 2026-10-02)
- **Despliegue:** **Nube.** "AI-Powered, Cloud-Based Dental Practice Management Software"; "20+ years cloud-based since 2004"; "No server to buy, no IT contractor to retain" — fuente: https://www.curvedental.com/ (consulta: 2026-10-02)
- **Vertical:** Odontológico puro — fuente: https://www.curvedental.com/ (consulta: 2026-10-02)
- **Presencia:** Estados Unidos y Canadá. "100,000+ active users in U.S. & Canada" — fuente: https://www.curvedental.com/ (consulta: 2026-10-02). Un tercero (fuente **no oficial**) confirma "Geo Served: [United States]" — fuente: https://platform.tracxn.com/a/d/company/5319473fe4b0f7e165f51191/curve%20dental (consulta: 2026-10-02). **Latinoamérica: No evidenciado**
- **Funciones declaradas:** Scheduling, Curve GRO® Patient Engagement, Smart Forms, Insurance Verification, Insurance Billing, Patient Billing, Curve Pay, Membership Plans, Charting, Imaging, Perio Charting, Treatment Planning, ePrescribe, File and Letter Management, Reporting, Business Analytics, Ambient AI (Curve Care+ / Curve Flo), Curve Mobile; **multi-sucursal** ("Add chairs without adding complexity, and see every location on one record") — fuente: https://www.curvedental.com/ (consulta: 2026-10-02)
- **Reserva pública sin login:** **No evidenciado.** El sitio declara "Online booking, scheduling, reminders, and patient communication" y un portal de paciente, pero **no enuncia** ausencia de login
- **Anti-solapamiento por profesional:** **No evidenciado** en fuente pública
- **Anti-solapamiento por sillón / box:** **No evidenciado** en fuente pública. La web menciona "Add chairs without adding complexity" **en el contexto de múltiples ubicaciones**, no como validación de recurso dentro de una agenda
- **Notificaciones WhatsApp:** **No evidenciado**
- **API / integraciones:** **No evidenciado** en esta consulta. La web declara un programa de "Integration Partners" y migraciones desde Dentrix, Dentrix Ascend, Eaglesoft, Open Dental, Oryx, CareStack, Archy, PracticeWorks y SoftDent — fuente: https://www.curvedental.com/ (consulta: 2026-10-02)
- **App móvil:** **Sí** — Curve Mobile — fuente: https://www.curvedental.com/ (consulta: 2026-10-02)
- **Seguridad / cumplimiento:** **Parcial.** Se declara "Best-in-class cybersecurity protection, including annual 3rd-party intrusion testing" y copias de seguridad en un centro de datos de Amazon Web Services — fuente: https://www.curvedental.com/practice (consulta: 2026-10-02)
- **Precios públicos:** **No evidenciado.** Existe una página de precios (https://www.curvedental.com/pricing) pero el precio se obtiene bajo demostración comercial. El propio proveedor reconoce: "Capabilities and services vary by package and availability. **Select features and services are currently U.S.-only**" — fuente: https://www.curvedental.com/ (consulta: 2026-10-02)
- **Adopción declarada por el proveedor:** "100,000+ active users in U.S. & Canada", "6,000+ practice locations", "4.6/5 across 500+ reviews", "20+ years cloud-based since 2004"; inversión declarada de **USD 200 millones** en I+D — fuentes: https://www.curvedental.com/ y https://www.prnewswire.com/news-releases/curve-dental-announces-200-million-rd-investment-302856409.html (consulta: 2026-10-02). Cifras **declaradas por el proveedor**
- **Fortalezas:** Plataforma cloud madura con el **único conjunto completo de módulos clínicos y financieros** del bloque internacional; soporte 24/7 con personal propio; IA clínica incorporada (Ambient AI, IA de imagen); multi-ubicación con registro único;ecas casos de éxito nombrados
- **Limitaciones:** **Estrictamente Estados Unidos y Canadá** — el propio proveedor declara que ciertas funciones y servicios son "currently U.S.-only"; **sin presencia latinoamericana evidenciada**; **sin precios públicos**; sin WhatsApp; **sin declaración pública** de anti-solapamiento por sillón; fuerte dependencia del sistema de seguros dental estadounidense (Insurance Billing, Insurance Verification), un concepto **no trasladable** a modelos de obra social o planes locales

### 4.3 CareStack

- **Nombre:** CareStack
- **Proveedor:** CareStack — **No evidenciado** (no se accedió al sitio del proveedor en esta consulta)
- **País de origen:** Estados Unidos. Deducido de la integración que Curve declara aceptar ("We Convert From: … CareStack …") — fuente: https://www.curvedental.com/ (consulta: 2026-10-02)
- **Despliegue:** Nube — **No evidenciado** en fuente de proveedor
- **Vertical:** Odontológico — **No evidenciado** en fuente de proveedor
- **Presencia:** **No evidenciado.** La web de Curve la incluye entre los productos de los que migra clientes, lo que confirma existencia comercial en EE. UU. — fuente: https://www.curvedental.com/ (consulta: 2026-10-02)
- **Funciones declaradas:** **No evidenciado** en fuente de proveedor
- **Reserva pública sin login:** **No evidenciado**
- **Anti-solapamiento por profesional:** **No evidenciado**
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **No evidenciado**
- **API / integrações:** **No evidenciado**
- **App móvil:** **No evidenciado**
- **Seguridad / cumplimiento:** **No evidenciado**
- **Precios públicos:** **Sí, pero solo por fuente de terceros.** Un comparador de Capterra reporta un precio de referencia de **USD 698 por mes** — fuente: **tercero**, https://www.capterra.com/compare/153816-176206/Dentally-vs-CareStack (consulta: 2026-10-02). Este monto **no fue confirmado en el sitio del proveedor** y debe tratarse como referencia no verificada
- **Adopción declarada:** **No evidenciado**
- **Fortalezas:** Reconocido por el mercado como competidor de plataforma cloud; aparece en listas de integración de terceros (Curve, OS Dental), lo que confirma que es un PMS cloud relevante
- **Limitaciones:** **Evidencia casi inexistente**: no se accedió a fuente de proveedor, por lo que la ficha queda mayoritariamente en **"No evidenciado"**; el precio proviene de un tercero; **no se evaluó** su relevance para Latinoamérica; debe completarse la investigación antes de cualquier decisión

### 4.4 NexHealth

- **Nombre:** NexHealth
- **Proveedor:** NexHealth, Inc. (sede en San Francisco, California, EE. UU.; fundada 2017) — fuentes: https://www.linkedin.com/company/nexhealth-inc y http://nexhealth.com/ (consulta: 2026-10-02)
- **País de origen:** Estados Unidos — fuente: https://www.linkedin.com/company/nexhealth-inc (consulta: 2026-10-02)
- **Despliegue:** Nube / SaaS — "The Patient Experience Platform"; sincronización en tiempo real vía "NexHealth Synchronizer" — fuente: http://nexhealth.com/ (consulta: 2026-10-02)
- **Vertical:** **No es un PMS odontológico**: es una **capa de experiencia del paciente** que se integra a PMS existentes. "Keep your system. Lose the busywork" — fuente: https://www.nexhealth.com/ (consulta: 2026-10-02)
- **Presencia:** **Estados Unidos únicamente.** LinkedIn declara "25% de las experiencias de atención en EE. UU. se viven a través de prácticas potenciadas por NexHealth" y headquarters en San Francisco — fuente: https://www.linkedin.com/company/nexhealth-inc (consulta: 2026-10-02). Un tercero confirma "Geo Served: [United States]" — fuente: **tercero**, https://platform.tracxn.com/a/d/company/64139ab18477f979aa3a171c/nexhealth (consulta: 2026-10-02). **Latinoamérica: No evidenciado**
- **Funciones declaradas:** Scheduling (reserva online, cancelación automática, llenado de huecos), Forms (formularios digitales que sincronizan con el PMS), Patient Engagement, comunicaciones, Insights dashboard con planes de tratamiento y pagos, API para desarrolladores — fuentes: https://www.nexhealth.com/ y https://docs.nexhealth.com/docs/supported-health-record-systems (consulta: 2026-10-02)
- **PMS soportados (declarados):** Athena, Cloud9, **Curve Hero**, Denticon, **Dentrix** (G6.2+), **Dentrix Ascend**, **Dentrix Enterprise**, Dolphin, Eaglesoft, eClinicalWorks, Modernizing Medicine, **Open Dental** (V17+), OrthoTrac, PracticeWorks, NextGen Office — fuente: https://docs.nexhealth.com/docs/supported-health-record-systems (consulta: 2026-10-02)
- **Reserva pública sin login:** **No evidenciado**
- **Anti-solapamiento por profesional:** **No evidenciado**
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **No evidenciado**
- **API / integraciones:** **Sí.** "Start Building with NexHealth API" y página oficial de integraciones — fuente: https://www.nexhealth.com/ (consulta: 2026-10-02)
- **App móvil:** **No evidenciado**
- **Seguridad / cumplimiento:** **No evidenciado**
- **Precios públicos:** **No evidenciado.** La web publica el enlace "Pricing" pero no se obtuvo un monto; se comunica "Contact" — fuente: http://nexhealth.com/ (consulta: 2026-10-02)
- **Adopción declarada por el proveedor:** casos nombrados: Bastida Dental Group (ahorra USD 2.000/mes en comisiones de Zocdoc), Perfect Smile Dental Care (+35 reservas mensuales de Google, +40% reseñas positivas), Daily Smiles Dental (reducción de cancelaciones), Mid-Atlantic Dental Partners — fuente: https://www.nexhealth.com/integrations (consulta: 2026-10-02)
- **Fortalezas:** **Arquitectura de referencia para el proyecto:** capa de experiencia del paciente desacoplada del PMS, con API pública y sincronización en tiempo real; modelo sin contrato a largo plazo y planes mensuales flexibles; casos de uso con métricas
- **Limitaciones:** **No es un PMS**: requiere un PMS previo, lo que duplica sistemas; **exclusivamente EE. UU.**; sin presencia latinoamericana; **sin precios públicos**; sin WhatsApp; **sin declaración** de anti-solapamiento; el modelo de negocio porASS (tarifa por característica) es、 opacity

### 4.5 Weave

- **Nombre:** Weave
- **Proveedor:** Weave — **No evidenciado** (no se accedió a página corporativa de about en esta consulta)
- **País de origen:** Estados Unidos — inferido de la  currency y del modelo de negocio
- **Despliegue:** Nube / SaaS
- **Vertical:** **No es un PMS odontológico**: es una plataforma de **comunicaciones y para consultorios**, con vertical dental. "Insurance Verification (dental only)", "Eyewear Ready Notifications (opto only)" — fuente: https://getweave.com/plans (consulta: 2026-10-02)
- **Presencia:** **Estados Unidos.** Capterra reporta sede en Utah y 673–692 reseñas — fuente: **tercero**, https://www.capterra.com/p/141842/Weave (consulta: 2026-10-02). **Latinoamérica: No evidenciado**
- **Funciones declaradas:**eskupo de teléfono, mensajería, recordatorios,oncolog verificación de seguros, analítica de consultorio, relationship management, herramientas de marketing y reputación; ofrece hasta 15 teléfonos por plan — fuente: https://getweave.com/plans (consulta: 2026-10-02)
- **Reserva pública sin login:** **No evidenciado**
- **Anti-solapamiento por profesional:** **No evidenciado**
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **No evidenciado.** Weave   SMS y llamadas
- **API / integraciones:** **No evidenciado** en esta consulta
- **App móvil:** **No evidenciado** en esta consulta
- **Seguridad / cumplimiento:** **No evidenciado** en esta consulta
- **Precios públicos:** **Sí, con discrepancia entre fuentes.**
  - **Fuente de proveedor:** "starting from **$249 per month**" en https://getweave.com/plans y "starting from **$199 per month**" en https://www.getweave.com/pricing (consulta: 2026-10-02). La discrepancia interna del propio proveedor (199 vs 249) está documentada
  - **Fuente de tercero:** Capterra reporta "Starting Price $199.00 /month" — fuente: **tercero**, https://www.capterra.com/compare/141842-182271/Weave-vs-NexHealth (consulta: 2026-10-02)
  - Los planes Pro, Elite y Ultimate requieren "Get Pricing" (consulta individual)
- **Adopción declarada por el proveedor:** "How Beaches Dental saves $3,500 a year with Weave", "Smith Dental saw a 28% increase in new patients" — fuente: https://getweave.com/plans (consulta: 2026-10-02). Casos **declarados por el proveedor**
- **Reconocimiento:** "Weave is recognized as a top-rated tool in 2 Capterra Shortlist reports (Appointment Reminder / 2025, 2024)" — fuente: **tercero**, https://www.capterra.com/compare/141842-182271/Weave-vs-NexHealth (consulta: 2026-10-02)
- **Fortalezas:** Especialización fuerte en un problema concreto (comunicación y gestión de), con soporte telefónico propio; verificación de seguros dental integrada; analítica específica de consultorio
- **Limitaciones:** **No es un PMS**: no gestiona agenda, historia clínica ni facturación; **exclusivamente EE. UU.**; sin presencia latinoamericana; **precio inconsistente en la propia web del proveedor**; reseñas de terceros mencionan congelamientos ("It freezes up multiple times a day", "would not rely on this for payment collections") — fuente: **tercero**, https://www.capterra.com/compare/141842-182271/Weave-vs-NexHealth (consulta: 2026-10-02); sin WhatsApp; sin anti-solapamiento

### 4.6 Oryx Dental

- **Nombre:** Oryx (Oryx Dental)
- **Proveedor:** Oryx — "founded by practicing dentist **Dr. Rania Saleh**" — fuentes: https://www.oryxdental.com/demo y https://www.oryxdental.com/pricing (consulta: 2026-10-02)
- **País de origen:** Estados Unidos. "cloud-based dental practice management platform for solo, startup, specialty, and multi-location practices in the United States and Canada" — fuente: https://www.oryxdental.com/demo (consulta: 2026-10-02)
- **Despliegue:** **Nube sobre Google Cloud.** "hosted on Google Cloud Platform" y "Built on Google Cloud infrastructure" — fuentes: https://www.oryxdental.com/demo y https://www.oryxdental.com/features-overview (consulta: 2026-10-02)
- **Vertical:** Odontológico puro — fuente: https://www.oryxdental.com/ (consulta: 2026-10-02)
- **Presencia:** Estados Unidos y Canadá — fuente: https://www.oryxdental.com/demo (consulta: 2026-10-02). El proveedor declara "15,000+ clinicians" y "**2,000 practices across 5 continents**" y "7M+ patients served worldwide" — fuente: https://www.oryxdentalsoftware.com/ (consulta: 2026-10-02). **Esta última cifra sugiere presencia internacional, pero no identifica países: Latinoamérica = No evidenciado**
- **Funciones declaradas:** Online booking, automated reminders, two-way texting, portal seguro de paciente para formularios y pagos, Practice Management, Revenue Cycle Management (RCM) con equipo propio de Oryx, facturación electrónica, text-to-pay, posting automático, tableros de KPI, Memberos, planes de membresía, IA de imágenes con Pearl y Overjet, IA de anotaciones, eScript, conversion de datos e imágenes inicial — fuentes: https://www.oryxdental.com/ y https://www.oryxdental.com/pricing (consulta: 2026-10-02)
- **Reserva pública sin login:** **No evidenciado**
- **Anti-solapamiento por profesional:** **No evidenciado**
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **No evidenciado**. Los canales declarados son **SMS de doble vía** y notificaciones de app
- **API / integraciones:** **No evidenciado** en esta consulta
- **App móvil:** **No evidenciado** en esta consulta (se mencionan notificaciones vía "Oryx Docs app")
- **Seguridad / cumplimiento:** **Sí (declarado).** "Full **HIPAA** and **PIPEDA** compliance with audit trail monitoring", autenticación de dos factores, 99,9% de uptime, permisos por rol, backups automáticos en Google Cloud — fuente: https://www.oryxdental.com/ (consulta: 2026-10-02). Nótese que HIPAA y PIPEDA **no son** los marcos normativos de Latinoamérica
- **Precios públicos:** **Sí, con la estructura más transparente del bloque.**
  - **Oferta de lanzamiento ("Startup Offer")**: **USD 0/mes** durante el período promocional; el precio regular comienza **a partir de 200 pacientes o 12 meses** tras el registro, lo que ocurra primero
  - **Oryx AI: USD 400/mes** (incluye AI Annotations y eScript)
  - **Fee de instalación: USD 1**
  - **Precios también publicados en CAD: USD 0 CAD/mes y CAD 400/mes**
  - Fuente: https://www.oryxdental.com/pricing (consulta: 2026-10-02)
- **Adopción declarada por el proveedor:** "15,000+ Clinicians", "2,000 Practices Across 5 Continents", "7M Patients Served Worldwide", "USD 5B+ in Payments Processed"; "9 out of 10 Dentists and their teams recommend Oryx"; "Save 70% vs. legacy systems" — fuentes: https://www.oryxdentalsoftware.com/ y https://www.oryxdental.com/demo (consulta: 2026-10-02). Cifras **declaradas por el proveedor**. Reconocimiento adicional: primer y único PMS odontológico reconocido por la **Academy of General Dentistry (AGD)**, y cloud PMS más rápido en crecimiento según **Inc. 5000** — fuente: https://www.oryxdental.com/demo (consulta: 2026-10-02)
- **Fortalezas del bloque internacional:** **La estructura de precios más transparente y moderna** (precio de entrada cero, fee de instalación symbolically de USD 1, sin cargos ocultos, sin cobro por asiento); arquitectura cloud moderna sobre Google Cloud; compliance declarado de HIPAA y PIPEDA con 2FA y 99,9% uptime; IA clínica con proveedores de imagen reconocidos (Pearl, Overjet) y certificaciones FDA; onboarding con conversión de datos incluida; modelo escalable de USD 0 → USD 400
- **Limitaciones:** **Estados Unidos y Canadá** — la declaración de "5 continentes" **no identifica** países y no permite afirmar presencia latinoamericana; marcado por **US-first** (HIPAA/PIPEDA, seguros, RCM centinado en claims); **sin WhatsApp**; **sin declaración** de anti-solapamiento por profesional ni por sillón; el "Startup Offer" es una promoción temporal, no un precio sostenible
- **Nota de nomenclatura:** "**Oxygen**", solicitado en el relevamiento original, **no fue encontrado** como producto de gestión odontológica. El sistema relevado en esta ficha es **Oryx**, que es un producto **distinto**. No deben confundirse

### 4.7 Dentally

- **Nombre:** Dentally
- **Proveedor:** **Henry Schein One** — "As part of Henry Schein One, Dentally is uniquely placed to anticipate future trends and challenges in dentistry" — fuente: https://www.dentally.com/en-ca/ (consulta: 2026-10-02)
- **País de origen:** Reino Unido. El sitio publica variantes por país: `en-gb` (Reino Unido), `en-ie` (Irlanda), `en-nz` (Nueva Zelanda), `en-au` (Australia), `en-ca` (Canadá) — fuente: https://www.dentally.com/en-ca/ (consulta: 2026-10-02)
- **Despliegue:** **Nube.** "market leading cloud enabled intelligent dental practice management software" y "Cloud Based Dental Management Software" sin costos de hardware ni mantenimiento de servidor — fuentes: https://www.dentally.com/en-ca/ y https://www.dentally.com/en-ie/cloud-based-dental-software (consulta: 2026-10-02)
- **Vertical:** Odontológico puro — fuente: https://www.dentally.com/en-ca/ (consulta: 2026-10-02)
- **Presencia:** Reino Unido, Irlanda, Nueva Zelanda, Australia y Canadá. **Latinoamérica: No evidenciado** — fuente: https://www.dentally.com/en-ca/ (consulta: 2026-10-02)
- **Funciones declaradas:** Practice management, online appointment booking, digital form filling, seamless arrivals (recepción), insights hub, group visibility and consistency across every location, CDAnet integration para claims y preautorizaciones (__ndadjunctionarias) en Canadá, multi-sucursal — fuente: https://www.dentally.com/en-ca/ (consulta: 2026-10-02)
- **Reserva pública sin login:** **No evidenciado**
- **Anti-solapamiento por profesional:** **No evidenciado**
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **No evidenciado**
- **API / integraciones:** **Parcial** — integración declarada con CDAnet (Canadá) — fuente: https://www.dentally.com/en-ca/ (consulta: 2026-10-02)
- **App móvil:** **No evidenciado** en esta consulta
- **Seguridad / cumplimiento:** **No evidenciado** en esta consulta
- **Precios públicos:** **Parcial.** "Dentally offers **flexible pricing based on practice size**. Unlike traditional dental software, there are **no upfront hardware costs, no server maintenance fees**" — sin monto público en la página consultada — fuente: https://www.dentally.com/en-ie/cloud-based-dental-software (consulta: 2026-10-02)
- **Adopción declarada:** **No evidenciado** en esta consulta
- **Fortalezas:** Pertenece a **Henry Schein One**, el mayor distribuidor dental global, lo que garantiza respaldo financiero y cobertura de la cadena de suministro; arquitectura cloud sin inversión inicial en hardware; modelo multi-país europeo con localización; multi-sucursal con visibilidad de grupo
- **Limitaciones:** **Sin presencia latinoamericana**; sin precios públicos con monto; la página consultada tiene **pesimo enfoque en el mercado canadiense** (CDAnet, claims), lo que sugiere que el producto tiene adaptaciones regionales fuertes; sin WhatsApp; sin declaración de anti-solapamiento

### 4.8 Dentrix

- **Nombre:** Dentrix (variantes: Dentrix Ascend, Dentrix Enterprise)
- **Proveedor:** Henry Schein One — **No evidenciado** directamente (la atribución a Henry Schein One se infiere del ecosistema Dentally/PracticeWorks). No se accedió a la web de Dentrix en esta consulta
- **País de origen:** Estados Unidos — **No evidenciado** en fuente de proveedor
- **Despliegue:** Nube (Ascend) y servidor local (Enterprise) según la documentación de integración de terceros: "Dentrix G6.2+", "Dentrix Ascend — All (cloud)", "Dentrix Enterprise — All (server)" — fuente: **tercero** (documentación de NexHealth), https://docs.nexhealth.com/docs/supported-health-record-systems (consulta: 2026-10-02)
- **Vertical:** Odontológico — **No evidenciado** en fuente de proveedor
- **Presencia:** **No evidenciado.** La documentación de NexHealth confirma que Dentrix existe como producto con tres variantes (G6.2+, Ascend y Enterprise) — fuente: https://docs.nexhealth.com/docs/supported-health-record-systems (consulta: 2026-10-02). Curve también lo incluye entre los productos de los que migra clientes — fuente: https://www.curvedental.com/ (consulta: 2026-10-02). **Latinoamérica: No evidenciado**
- **Funciones declaradas:** **No evidenciado** en fuente de proveedor
- **Reserva pública sin login:** **No evidenciado**
- **Anti-solapamiento por profesional:** **No evidenciado**
- **Anti-solapamiento por sillón / box:** **No evidenciado**
- **Notificaciones WhatsApp:** **No evidenciado**
- **API / integraciones:** **Sí (evidenciado por terceros).** Dentrix es una de las integraciones soportadas por NexHealth y Curve, y aparece como PMS conectado en integraciones de terceros (OS Dental) — fuentes: https://docs.nexhealth.com/docs/supported-health-record-systems y https://osdental.io/platform/features (consulta: 2026-10-02)
- **App móvil:** **No evidenciado**
- **Seguridad / cumplimiento:** **No evidenciado**
- **Precios públicos:** **No evidenciado**
- **Adopción declarada:** **No evidenciado**
- **Fortalezas:** Su condición de estándar de facto queda confirmada por el ecosistema: es integrable por las dos plataformas cloud más relevantes del bloque (NexHealth y Curve), lo que implica una base instalada grande y un riesgo de obsolescencia bajo
- **Limitaciones:** **Investigación incompleta**: no se accedió al sitio del proveedor, por lo que la ficha queda en su mayor parte en **"No evidenciado"**; su al proveedor Henry Schein One es **inferida**, no verificada; sin evidencia de presencia latinoamericana; **no debe usarse** para decisiones hasta completar el relevamiento

---

## 5. Anti-solapamiento: hallazgo transversal

Este es el requisito **más crítico** del proyecto y el peor documentado de todo el mercado relevado.

### 5.1 Resultados

| Sistema | Anti-solapamiento por profesional | Anti-solapamiento por sillón / box | Evidencia |
|---|---|---|---|
| DentalCitas | **Sí (declarado)** | **Parcial** (exclusividad de franja horaria) | https://dental.rasalopa.dev/ (consulta: 2026-10-02) |
| AgendaPro | No evidenciado | No evidenciado | https://agendapro.com/ar (consulta: 2026-10-02) |
| Doctoralia PRO | No evidenciado | No evidenciado | https://pro.doctoralia.com/ar (consulta: 2026-10-02) |
| Dentalink | No evidenciado | No evidenciado | http://www.dentalink.net/ (consulta: 2026-10-02) |
| Clinicorp | No evidenciado | No evidenciado | https://www.clinicorp.com/planos (consulta: 2026-10-02) |
| Simples Dental | No evidenciado | No evidenciado | https://www.simplesdental.com/ (consulta: 2026-10-02) |
| Prontuário Verde | No evidenciado | No evidenciado | https://www.prontuarioverde.com.br/ (consulta: 2026-10-02) |
| Dentalis | No evidenciado | No evidenciado | https://www.dentalis.com.br/ (consulta: 2026-10-02) |
| Sistema ClínicaPro | No evidenciado | No evidenciado | https://sistemaclinicopro.com.br/ (consulta: 2026-10-02) |
| SimpleTurno | Parcial (agenda por profesional) | No evidenciado | https://simpleturno.com/rubros/odontologia (consulta: 2026-10-02) |
| Reservo | No evidenciado | No evidenciado | https://reservo.com.ar/ (consulta: 2026-10-02) |
| UDENTIVA | No evidenciado | No evidenciado | https://udentiva.com/pt-uy (consulta: 2026-10-02) |
| Open Dental | No evidenciado | No evidenciado | https://www.opendental.com/ (consulta: 2026-10-02) |
| Curve Dental | No evidenciado | No evidenciado | https://www.curvedental.com/ (consulta: 2026-10-02) |
| CareStack | No evidenciado | No evidenciado | https://www.capterra.com/compare/153816-176206/Dentally-vs-CareStack (consulta: 2026-10-02) |
| NexHealth | No evidenciado | No evidenciado | https://docs.nexhealth.com/docs/supported-health-record-systems (consulta: 2026-10-02) |
| Weave | No evidenciado | No evidenciado | https://getweave.com/plans (consulta: 2026-10-02) |
| Oryx Dental | No evidenciado | No evidenciado | https://www.oryxdental.com/ (consulta: 2026-10-02) |
| Dentally | No evidenciado | No evidenciado | https://www.dentally.com/en-ca/ (consulta: 2026-10-02) |
| Dentrix | No evidenciado | No evidenciado | https://docs.nexhealth.com/docs/supported-health-record-systems (consulta: 2026-10-02) |

### 5.2 Conclusión

De los **20 sistemas documentados**:

- **19 (95%)** no tienen ninguna declaración pública de anti-solapamiento.
- **1 (5%)** — DentalCitas — declara explícitamente "Sin citas solapadas" y "Cada horario solo puede reservarse una vez".
- **0 (0%)** declara explícitamente validación por **sillón o box** como recurso independiente de la franja horaria.

**Implicación para el proyecto:** la validación doble por profesional y por sillón no está documentada como funcionalidad de mercado en ninguno de los sistemas comerciales relevados. Esto convierte la regla de negocio en un **diferenciador técnico y funcional** y justifica su implementación explícita, con evidencia en la base de datos (transacción y restricciones) y no solo en la capa de interfaz.

---

## 6. Reserva pública sin login: hallazgo transversal

| Sistema | Reserva pública sin login | Evidencia |
|---|---|---|
| DentalCitas | **Sí (declarado: "sin crear cuenta")** | https://dental.rasalopa.dev/ (consulta: 2026-10-02) |
| Clinicorp | Parcial (agendamento online) | https://www.clinicorp.com/planos (consulta: 2026-10-02) |
| Simples Dental | Parcial (agenda online) | https://www.simplesdental.com/ (consulta: 2026-10-02) |
| Reservo | Parcial (reserva y pago en línea, declarado para el rubro psicología) | https://reservo.com.ar/ (consulta: 2026-10-02) |
| Dentalis | Parcial (sitio con agendamento integrado) | https://www.dentalis.com.br/ (consulta: 2026-10-02) |
| Open Dental | Parcial (Web Sched) | https://www.opendental.com/ (consulta: 2026-10-02) |
| AgendaPro | No evidenciado (declara "Reservas 24/7" y "Sitio de Reservas", sin declarar ausencia de login) | https://agendapro.com/ar (consulta: 2026-10-02) |
| Resto (14 sistemas) | No evidenciado | Ver fichas individuales |

**Implicación para el proyecto:** la reserva sin login es una **funcionalidad estándar de facto** en la región (agenda online, portal de reservas, link de reservas), pero **ningún proveedor de software comercial declara explícitamente** que su flujo sea sin autenticación. La diferencia está en la fricción real del flujo, no en lo que la web afirma. El proyecto debe documentar su flujo sin login como **decisión de diseño explícita y medible**, no implícita.

---

## 7. Precios públicos: síntesis

### 7.1 Sistemas con precio público

| Sistema | Plans / precios públicos | Moneda | Condiciones declaradas |
|---|---|---|---|
| AgendaPro | USD 9 (individual), USD 29 (básico), USD 59 (premium) / mes | USD | Precios **regionales**; los de Argentina **No evidenciado** |
| Clinicorp | Standard R$ 159,90/mes · Premium R$ 369,90/mes · Enterprise bajo cotización | BRL | Precios "pueden ser reajustados con el tiempo"; implementación y tasas adicionales no incluidas |
| SimpleTurno | **Plan gratuito sin límite de tiempo, sin tarjeta**; planes pagos No evidenciado | — | Entrada gratuita completa |
| DentalCitas | Free (hasta 30 citas/mes) · Pro MXN 299/mes · Ultimate (prueba 14 días) | MXN | Producto prototipo |
| Open Dental | Tarifa de soporte variable por ubicaciones y profesionales, en USD; **tarifas reducidas para clientes fuera de EE. UU.** | USD | Modelo de licencia local; no hay licencia base pública |
| Weave | Desde USD 199/mes (página de precios) o USD 249/mes (página de planes) | USD | **Discrepancia interna del proveedor**; planes Pro/Elite/Ultimate bajo consulta |
| Oryx Dental | Oferta USD 0/mes; Oryx AI USD 400/mes; fee de instalación USD 1; regular desde 200 pacientes o 12 meses | USD y CAD | Promoción temporal; "no hidden fees, no per-seat" |
| CareStack | USD 698/mes (referencia de tercero, **no verificada**) | USD | Solo fuente secundaria |

### 7.2 Sistemas sin precio público

AgendaPro (Argentina), Doctoralia PRO, Dentalink, Simples Dental, Prontuário Verde, Dentalis, Sistema ClínicaPro, Reservo, UDENTIVA, Curve Dental, NexHealth, Dentally, Dentrix.

**Patrón de mercado observado:** los proveedores con **modelo de agenda + recordatorios Gemini la Ruby netamente scheduling** (SimpleTurno, AgendaPro) publican precios de entrada **gratuitos o muy bajos**. Los **PMS odontológicos completos** (Dentalink, Clinicorp Enterprise, Curve, Dentally, NexHealth, Dentrix) **ocultan el precio bajo demostración comercial**. Los **proveedoresocrats de IA o de capas de experiencia** (NexHealth, Denti.AI) cobran **más caro** que los software de agenda.

---

## 8. Presencia geográfica latinoamericana: síntesis

| País | Sistemas con presencia declarada |
|---|---|
| **Argentina** | AgendaPro, Doctoralia PRO, SimpleTurno, Reservo |
| **Brasil** | Clinicorp, Simples Dental, Prontuário Verde, Dentalis, Sistema ClínicaPro, **Open Dental** (usuarios, soporte en español/portugués) |
| **México** | AgendaPro, Doctoralia PRO, **DentalCitas** (indicio por precios en MXN) |
| **Chile** | Dentalink, Doctoralia PRO, AgendaPro (No evidenciado) |
| **Uruguay** | UDENTIVA, **Open Dental** (contacto de soporte en español y versión en español) |
| **Perú** | **Open Dental** (contacto de soporte en español y versión en español) |
| **Colombia** | **Ningún sistema con presencia declarada.** Solo Doctoralia PRO como directorio con presencia regional (No evidenciado en ficha) |

**Hallazgo:** el mercado latinoamericano de software odontológico está **fragmentado por país**, no regional. Solo AgendaPro y Doctoralia PRO mantienen páginas por país en varios de estos mercados. **Colombia es un hueco de mercado** en toda la muestra. **Open Dental es el puente más interesante**: es el único sistema internacional con presencia documentada en tres países de la región (Brasil, Perú, Uruguay), y su página internacional incluye explícitamente **versiones en español** para Perú y Uruguay y un contacto de soporte en Brasil — fuente: https://www.opendental.com/site/countries.html (consulta: 2026-10-02).

---

## 9. Relevancia para Argentina

### 9.1 Tres sistemas latinoamericanos más relevantes

| Puesto | Sistema | Por qué es relevante para Argentina | Principal Limitación para el contexto argentino |
|---|---|---|---|
| **1** | **AgendaPro** | Único sistema con **operación comercial argentina declarada** (sede, teléfono local, +20.000 negocios), respaldo de inversores internationales, **integración real con WhatsApp**, **integración con Google Reserve / Google My Business** — la vía de descubrimiento que usan los pacientes argentinos-, control multi-sucursal, app iOS/Android, y **precios públicos muy accesibles** (desde USD 9/mes) | **No declara** anti-solapamiento por profesional ni por sillón; **no declara** reserva sin login; **no declara** cumplimiento de la Ley 25.326; el producto es un gestor de servicios de belleza y bienestar generalista, con la odontología como vertical secundaria en el mercado argentino |
| **2** | **SimpleTurno** | **El competidor más cercano al proyecto en el mercado argentino**: español rioplatense nativo, **plan gratuito sin límite de tiempo y sin tarjeta**, reserva mediante **enlace propio**, **agenda separada por profesional con tipos de consulta** (general, ortodoncia, periodología) y **cobro de seña con MercadoPago** — la forma de pago dominante local- además recordatorios por WhatsApp | **No declara** anti-solapamiento ni sillones; **no declara** reserva sin login; sin planes pagos documentados; sin app móvil, API pública ni declaración de cumplimiento normativo; se posiciona explícitamente como "sin funciones innecesarias" |
| **3** | **Reservo** | Vertical odontológica con **ficha clínica, diagnóstico, presupuesto y odontograma** (profundidad clínica que SimpleTurno no tiene), y una **arquitectura centrada en integraciones**: **MercadoPago**, WooCommerce, agenda externa, y **WhatsApp como confirmación automática** de citas | Sin precios públicos; **no declara** anti-solapamiento ni sillones; sin app móvil; sin declaración de cumplimiento normativo; cobertura fuera de Argentina no evidenciada |

**Mención de cuarto:** **Doctoralia PRO** merece consideration por su **directorio integrado** (tráfico de pacientes patients ya segmentados por especialidad y ubicación) y por su presencia simultánea en Argentina, Chile y México. Sin embargo, su evidencia pública argentina es la más débil de los cuatro en cuanto a funciones: **no publica monto de precio** (la ruta de precios devolvió 404) y **no declara** ni anti-solapamiento ni WhatsApp.

### 9.2 Tres sistemas internacionales más relevantes como referencia

Ninguno de los tres tiene presencia latinoamericana declarada, por lo que su valor es **puramente referencial** (arquitectura, modelos de precio, patrones de compliance):

| Puesto | Sistema | Por qué es relevante | Principal Limitación |
|---|---|---|---|
| **1** | **Oryx Dental** | La **estructura de precios más limpia del mercado relevado**: entrada a USD 0, fee de instalación de USD 1, sin cobros por asiento ni cargos ocultos, con una transición transparente a USD 400/mes y a un precio regular definido por un disparador objetivo (200 pacientes o 12 meses). Además ofrece **conversión de datos e imágenes incluida**, compliance declarado (2FA, 99,9% uptime, permisos por rol) e IA clínica con proveedores reconocidos. Es el modelo de referencia más útil para **diseñar el esquema de precios propio** | US-first: HIPAA/PIPEDA y gestión de claims de seguros dental, **no trasladable** a obra social o planes locales; **sin WhatsApp**; sin declaración de anti-solapamiento; la oferta de USD 0 es promocional |
| **2** | **NexHealth** | El **modelo arquitectónico más relevante para el proyecto**: una **capa de experiencia del paciente desacoplada del PMS**, con **API pública**, sincronización en tiempo real, planes mensuales sin contrato a largo plazo y casos de uso con métricas concretas. Demuestra que la reserva online, los formularios y la comunicación pueden vivir **por encima** de un sistema de gestión, no dentro de él | **No es un PMS**: requiere un sistema previo, lo que duplica la arquitectura; **exclusivamente EE. UU.**; **sin precios públicos**; sin WhatsApp; sin anti-solapamiento |
| **3** | **Open Dental** | El **único puente real hacia Latinoamérica**: documenta presencia y **soporte en español** en **Perú y Uruguay**, y soporte en **Brasil**. Publica **precios en USD** y **tarifas reducidas** para clientes fuera de EE. UU., lo que demuestra un modelo comercial que contempla explícitamente a los mercados no estadounidenses. Además ofrece **Web Sched** (reserva online) como módulo del producto | Despliegue **local con servidor propio**, incompatible con la arquitectura web del proyecto; soporte **limitado a usuarios angloparlantes** por declaración del propio proveedor; sin WhatsApp; sin declaración pública de anti-solapamiento |

**Mención de cuarto:** **Dentally** aporta el caso de una **empresa de distribución dental global** (Henry Schein One)redict successfully suficiente para garantizar respaldo, y un modelo cloud sin inversión inicial en hardware — modelo de entrada attractive para un consultorio que no quiere servidores. Sin presencia latinoamericana y sin monto público.

---

## 10. Sistemas solicitados sin evidencia suficiente

Se documentan aquí los nombres solicitados en el relevamiento original que **no pudieron documentarse** conforme a los criterios de evidencia aplicados. Se deja constancia explícita del resultado de la búsqueda, conforme a la instrucción de no inferir.

| Nombre solicitado | Resultado de la búsqueda | Estado |
|---|---|---|
| **Oxygen** (o "Oxygen Dental") | **No se encontró** ningún producto de gestión odontológica con ese nombre. La búsqueda devolvió **Oryx Dental** (documentado en §4.6), que es un producto **distinto**. Likely corresponde a un error de tipeo en el relevamiento original | **No evidenciado.** Documentado el producto efectivamente encontrado (Oryx) por separado |
| **Zenki** | **No se encontró** fuente de proveedor ni tercero confiable que documente un sistema de gestión o turnos odontológicos con ese nombre en Latinoamérica | **No evidenciado** |
| **Dentasis** | **No se encontró** fuente de proveedor ni tercero confiable. El término también designa un término médico (enfermedad periodontal), lo que sugiere un error de tipeo | **No evidenciado** |
| **SOAP** (interpretado como parte de "Dentrix/SOAP") | **No se encontró** relación con software de gestión odontológica. SOAP es un acrónimo deective/intercambio de datos (Simple Object Access Protocol), no un producto odontológico | **No evidenciado** |
| **ClinicPro** (genérico) | **Identidad ambigua.** Existen múltiples productos con nombres similares o idénticos. Se documentó el del dominio `sistemaclinicopro.com.br` (§3.8), y se documentó **Clinicorp** (§3.4) como producto distinto y mucho más grande | Parcialmente documentado, con advertencia de homonimia |
| **Aqamed** | Productoyatistente Located en **https://aqamed.com.br/login** (consulta: 2026-10-02), con agenda por profesional/unidad, prontuario, documentos, finanzas, reportes y trazabilidad. **No se accedió a una página de producto o de precios** que permitiera documentar su ficha con el mismo rigor que el resto | **No evidenciado** como ficha completa; URL registrada como pista |
| **Stratus** | El único Stratus localizado es **https://home.usestratus.com/about** (consulta: 2026-10-02), una plataforma estadounidense de **seguros y reclamaciones de beneficios dentales** para planes dental, no un sistema de gestión ni de turnos para consultorios | **Descartado por categoría.** No es un competidor del proyecto |
| **Cenident / DentOS (como sistema latinoamericano) / Odonto Software** | Se localizaron dominios (**https://cenident.com/**, **https://dent-os.com/**, **https://www.odontosoftware.com/**) pero no seibró evidencia suficiente de proveedor, país de origen, funcionalidad y precios. **DentOS** (https://dent-os.com/, consulta: 2026-10-02) es un **proyecto en early access** estadounidense que declara "conflict detection" y "No more double-bookings" en su tabla comparativa, y precios públicos de USD 199/mes (Starter) y USD 399/mes (Growth) | **No evidenciado** como sistemas latinoamericanos documentados |

### 10.1 Hallazgo lateral relevante: DentOS

Aunque **DentOS** no califica como sistema latinoamericano, su tabla comparativa es la **única fuente pública del universo relevado** que declara explícitamente **detección de conflictos** y **"No more double-bookings"**, con precios públicos. Fuente: https://dent-os.com/ (consulta: 2026-10-02). Se registra aquí porque **refuerza el hallazgo de §5**: incluso en el mercado estadounidense, la detección de conflictos es una característica de un producto nuevo en early access y no un estándar de los PMS maduros.

---

## 11. Algunas observaciones críticas y recomendaciones de diseño

1. **El anti-solapamiento es un territorio vacío de documentación pública.** 19 de 20 sistemas no lo declaran. El proyecto debe implementarlo con **garantía a nivel de base de datos** (restricción `UNIQUE` o transacción con bloqueo pesimista sobre `(profesional, fecha, hora_inicio, hora_fin)` y sobre `(sillon, fecha, hora_inicio, hora_fin)`), y no con validación únicamente en el front-end.

2. **La reserva sin login es estándar de facto pero no declarada.** Ningún proveedor comercial lo enuncia. El proyecto debe medirlo: porcentaje de reservas completadas sin creación de cuenta, y documentarlo como decisión de diseño.

3. **El sillón como recurso es inexistente en la documentación pública.** Ningún sistema documenta agenda por sillón/box como mecanismo de validación. Es la oportunidad de diferenciación más fuerte.

4. **WhatsApp es el estándar de facto regional, pero solo en tres países.** Brasil (Clinicorp, Simples Dental, Dentalis, Prontuário Verde, AgendaPro) y Argentina (AgendaPro, SimpleTurno, Reservo) lo tienen integrado; México, Chile, Colombia y Uruguay **No evidenciado**.

5. **La seguridad normativa es una brecha de documentación.** Solo tres sistemas declaran cumplimiento normativo: **UDENTIVA** (Ley 18.331 de Uruguay), **Oryx** (HIPAA + PIPEDA), **Doctoralia PRO** (RGPD). **Ningún sistema declare cumplimiento de la Ley 25.326 de Argentina ni de la LGPD de Brasil**. Para un proyecto académico esto no es bloqueante, pero para un producto comercial en la región sí lo sería.

6. **Precios de entrada gratuitos son la norma en la agenda; el PMS completo se oculta.** El competidor más cercano (SimpleTurno) ofrece plan gratuito sin tarjeta y sin límite de tiempo. Cualquier propuesta con precio de entrada debeObjsতো ভাবতে হবে

7. **No hay presencia declarada en Colombia en toda la muestra.** Si el proyecto tuviera alcance regional, Colombia sería un mercado desatendido por el software odontológico documentado.

8. **El modelo de capas (NexHealth) es la arquitectura más probed para el proyecto:** un núcleo de agenda con validación estricta, más una capa de experiencia del paciente (reserva pública, formularios, notificaciones) con API pública. Esto permite que el servicio de notificaciones mockeado sea intercambiable por uno real sin rediseñar el núcleo.

---

## 12. Bibliografía completa

### 12.1 Fuentes de proveedor (primarias)

| # | URL | Sistema | Consulta |
|---|---|---|---|
| 1 | https://agendapro.com/ar | AgendaPro (AR) | 2026-10-02 |
| 2 | https://agendapro.com/ar/planes | AgendaPro (AR, precios) | 2026-10-02 |
| 3 | https://agendapro.com/es/planes | AgendaPro (regional, precios) | 2026-10-02 |
| 4 | https://agendapro.com/es/dental/software-odontologico | AgendaPro (vertical dental) | 2026-10-02 |
| 5 | https://agendapro.com/mx/agenda-medica | AgendaPro (MX) | 2026-10-02 |
| 6 | https://pro.doctoralia.com/ar | Doctoralia PRO (AR) | 2026-10-02 |
| 7 | https://pro.doctoralia.es/productos/doctoralia-pro-especialistas/mini-video/agenda-inteligente | Doctoralia PRO (agenda inteligente) | 2026-10-02 |
| 8 | http://www.dentalink.net/ | Dentalink | 2026-10-02 |
| 9 | https://www.clinicorp.com/ | Clinicorp | 2026-10-02 |
| 10 | https://www.clinicorp.com/planos | Clinicorp (precios) | 2026-10-02 |
| 11 | https://www.clinicorp.com/agenda-cheia-que-converte | Clinicorp (agenda) | 2026-10-02 |
| 12 | https://www.clinicorp.com/melhor-software-odontologico-forms | Clinicorp (producto) | 2026-10-02 |
| 13 | https://www.clinicorp.com/post/agenda-personalizada-dentista | Clinicorp (blog) | 2026-10-02 |
| 14 | https://www.simplesdental.com/ | Simples Dental | 2026-10-02 |
| 15 | https://www.prontuarioverde.com.br/ | Prontuário Verde | 2026-10-02 |
| 16 | https://www.dentalis.com.br/ | Dentalis | 2026-10-02 |
| 17 | https://sistemaclinicopro.com.br/ | Sistema ClínicaPro | 2026-10-02 |
| 18 | https://simpleturno.com/rubros/odontologia | SimpleTurno | 2026-10-02 |
| 19 | https://reservo.com.ar/ | Reservo | 2026-10-02 |
| 20 | https://udentiva.com/pt-uy | UDENTIVA | 2026-10-02 |
| 21 | https://dental.rasalopa.dev/ | DentalCitas | 2026-10-02 |
| 22 | https://www.opendental.com/ | Open Dental | 2026-10-02 |
| 23 | https://www.opendental.com/site/fees.html | Open Dental (honorarios) | 2026-10-02 |
| 24 | https://www.opendental.com/site/countries.html | Open Dental (internacional) | 2026-10-02 |
| 25 | https://www.curvedental.com/ | Curve Dental | 2026-10-02 |
| 26 | https://www.curvedental.com/practice | Curve Dental (práctica/seguridad) | 2026-10-02 |
| 27 | https://www.curvedental.com/pricing | Curve Dental (precios) | 2026-10-02 |
| 28 | http://nexhealth.com/ | NexHealth | 2026-10-02 |
| 29 | https://docs.nexhealth.com/docs/supported-health-record-systems | NexHealth (PMS soportados) | 2026-10-02 |
| 30 | https://www.nexhealth.com/ | NexHealth | 2026-10-02 |
| 31 | https://www.nexhealth.com/integrations | NexHealth (integraciones) | 2026-10-02 |
| 32 | https://getweave.com/plans | Weave (planes) | 2026-10-02 |
| 33 | https://www.getweave.com/pricing | Weave (precios) | 2026-10-02 |
| 34 | https://www.oryxdental.com/ | Oryx Dental | 2026-10-02 |
| 35 | https://www.oryxdental.com/pricing | Oryx Dental (precios) | 2026-10-02 |
| 36 | https://www.oryxdental.com/features-overview | Oryx Dental (features) | 2026-10-02 |
| 37 | https://www.oryxdental.com/demo | Oryx Dental (demo) | 2026-10-02 |
| 38 | https://www.oryxdentalsoftware.com/ | Oryx Dental (corporativo) | 2026-10-02 |
| 39 | https://www.dentally.com/en-ca/ | Dentally (CA) | 2026-10-02 |
| 40 | https://www.dentally.com/en-ie/cloud-based-dental-software | Dentally (características) | 2026-10-02 |
| 41 | https://dent-os.com/ | DentOS (early access, US) | 2026-10-02 |
| 42 | https://aqamed.com.br/login | Aqamed (pista) | 2026-10-02 |
| 43 | https://home.usestratus.com/about | Stratus (US, descartado) | 2026-10-02 |
| 44 | https://cenident.com/ | Cenident (pista, no documentada) | 2026-10-02 |
| 45 | https://www.odontosoftware.com/ | Odonto Software (pista, no documentada) | 2026-10-02 |
| 46 | https://www.dentally.com/en-ca/ | Dentally | 2026-10-02 |

### 12.2 Fuentes de terceros (secundarias — marcadas como tales)

| # | URL | Aporta | Consulta |
|---|---|---|---|
| 47 | https://www.capterra.com/compare/153816-176206/Dentally-vs-CareStack | Precio de referencia de CareStack (USD 698/mes) | 2026-10-02 |
| 48 | https://www.capterra.com/compare/141842-182271/Weave-vs-NexHealth | Valoraciones de Weave y NexHealth, precio de Weave | 2026-10-02 |
| 49 | https://www.capterra.com/p/141842/Weave | Perfil de Weave | 2026-10-02 |
| 50 | https://platform.tracxn.com/a/d/company/5319473fe4b0f7e165f51191/curve%20dental | País y sector de Curve Dental | 2026-10-02 |
| 51 | https://platform.tracxn.com/a/d/company/64139ab18477f979aa3a171c/nexhealth | País de NexHealth | 2026-10-02 |
| 52 | https://www.linkedin.com/company/nexhealth-inc | Sede, fundación y alcance de NexHealth | 2026-10-02 |
| 53 | https://linkedin.com/company/curve-dental-inc. | Sede y fundación de Curve Dental | 2026-10-02 |
| 54 | https://osdental.io/platform/features | Integraciones de terceros con CareStack, Curve, Dentrix | 2026-10-02 |
| 55 | http://www.prnewswire.com/news-releases/curve-dental-announces-strategic-integration-partnership-with-dentalhq-setting-new-standard-for-connected-practice-management-302604329.html | Sedes de Curve Dental | 2026-10-02 |
| 56 | https://www.prnewswire.com/news-releases/curve-dental-announces-200-million-rd-investment-302856409.html | Inversión declarada de USD 200 millones en Curve | 2026-10-02 |
| 57 | https://totalmed.lat/blog/alternativas-a-dentalink-chile-2026 | Contexto de mercado en Chile (tercero) | 2026-10-02 |

### 12.3 Fuentes descartadas o no utilizadas

| Fuente | Motivo |
|---|---|
| https://pro.doctoralia.com/ar/precios | **HTTP 404** en la consulta del 2026-10-02. No se pudo obtener el precio de Doctoralia PRO en Argentina |
| https://www.curvedental.com/software | **HTTP 404** en la consulta del 2026-10-02. Se utilizó la raíz del sitio en su lugar |
| Resultado de búsqueda "Nexus Dental Systems / Nexus Integrated Health" (UAE, Arabia Saudita, Egipto, Australia, Corea del Sur, Japón) | Empresa **distinta** de NexHealth; su expansión a no incluye Latinoamérica. No documentada en el informe |
| Páginas de directorios con contenido generado automáticamente sobre "Zenki" y "Dentasis" | Sin verificación de proveedor; no se documentaryó para evitar contaminar el informe con información no confiable |

---

## 13. Limitaciones de este estudio

1. **Cobertura de fuentes públicas.** El estudio se basa exclusivamente en información pública. Varios proveedores (Curve, CareStack, Dentally, Dentally, NexHealth, Dentally) condicionan el detalle funcional a una demostración comercial, lo que deja su ficha en **"No evidenciado"** en campos clave.
2. **Fichas incompletas:** CareStack, Dentrix y, parcialmente, Aqamed, CareStack y Weave no alcanzan el estándar de evidencia de las restantes.
3. **Ausencia de verificación de terceros.** Las cifras de adopción son **declaradas por el proveedor** en su totalidad. No se localizaron auditorías independientes para AgendaPro, Clinicorp, Simples Dental, Oryx, Curve ni NexHealth.
4. **Precios en Argentina incompletos.** Solo AgendaPro publica precios, y los.arc de la página argentina no fueron recuperados. Los precios kilometers expresados en USD, BRL o MXN **no son directamente comparables** con un precio local en pesos argentinos.
5. **Ambigüedad de nombres.** El mercado regional presenta homónimos (ClinicPro/ClínicaPro/Clinicorp) que pueden llevar a conclusiones erróneas si no se verifica el dominio.
6. **Sin pruebas de las funcionalidades.** Ninguna funcionalidad fue verificada mediante prueba de uso. Todas las afirmaciones sobre capacidades son declaraciones de proveedor o de terceros.
7. **Alcance temporal.** Snapshot del mercado al 2026-10-02. Los precios, los planes y la presencia geográfica cambian.

---

*Fin del documento. Elaborado con base en fuentes públicas consultadas el 2026-10-02. Toda afirmación sin URL verificable en este documento está marcada como "No evidenciado".*

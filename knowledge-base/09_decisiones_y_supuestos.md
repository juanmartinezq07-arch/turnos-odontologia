# Decisiones y Supuestos

## Decisiones documentadas

### DD-01 — API / backend puro, sin frontend propio
**Decisión**: P0-sys = (b) API REST pura; la demo se ejerce con Swagger UI + pytest/httpx.
**Contexto**: trabajo individual, una semana, $0; el núcleo evaluado es la invariante RN02, no la UI.
**Alternativas consideradas**: (a) web full-stack con frontend; (e) SaaS multi-tenant.
**Justificación**: el frontend duplica trabajo sin sumar puntos de cátedra (el Change OPSX premia invariante + tests); multi-tenant es sobrediseño para 2–10 profesionales.
**Trade-offs aceptados**: la demo es menos vistosa; se compensa con Swagger prolijo y tests que muestran el 409 en vivo.

### DD-02 — Escala: consultorio chico (2–10 profesionales)
**Decisión**: P0-scale = (a) equipo pequeño; `scale = team`.
**Contexto**: consultorio chico, sin sucursales.
**Alternativas consideradas**: mediana, público masivo, multi-tenant.
**Justificación**: determina que alcanza con un monolito + Postgres local, sin caché, colas ni sharding.
**Trade-offs aceptados**: si el consultorio crece a multi-sucursal, habrá que re-modelar (ya listado en backlog).

### DD-03 — FastAPI + Pydantic v2 + SQLAlchemy 2.0 + Alembic + PostgreSQL 16 en Docker local
**Decisión**: stack (b) verbatim de kb-creator.
**Contexto**: sin restricción de stack desde Discovery; la trampa conocida era inferir stack/scale desde `docs/` poblado (Mode A silencioso). Se fuerza Mode B con respuestas cerradas.
**Alternativas consideradas**: SQLite + serialización procedural; Node/Express + Prisma.
**Justificación**: Python es el stack de la tecnicatura; PostgreSQL es el único que da `EXCLUDE USING gist` declarativo para RN02; Docker Compose deja la demo reproducible con $0.
**Trade-offs aceptados**: exige Docker instalado para correr la demo; a cambio el invariante es una línea de DDL en vez de un lock artesanal.

### DD-04 — RN02 declarativa con doble EXCLUDE
**Decisión**: dos constraints `EXCLUDE USING gist` (profesional y sillón) sobre `tstzrange(inicio, fin)` con `WHERE (estado='activo')` + extensión `btree_gist`.
**Contexto**: R1 (concurrencia) es el riesgo técnico central; DentalFLOW lo vende como "garantía a nivel de base de datos".
**Alternativas consideradas**: validación solo en aplicación; bloqueo pesimista por transacción serializable.
**Justificación**: solo el constraint cierra la ventana entre consulta de disponibilidad y alta bajo concurrencia real.
**Trade-offs aceptados**: el mensaje de error de Postgres es críptico → se traduce a 409 con código de regla en la capa API.

### DD-05 — Notificaciones como interfaz con mock, sin WhatsApp Business API
**Decisión**: `NotificationService` + mock en memoria; nada de Meta/plantillas/costos en el MVP.
**Contexto**: WhatsApp Business API exige verificación empresarial, plantillas con revisión (~24 h) y costo por mensaje — incompatible con $0 y una semana.
**Alternativas consideradas**: integrar WhatsApp real; email transaccional.
**Justificación**: el dominio no depende del canal; el mock deja el seam abierto y la demo declara el costo real con cifras verificadas (argumento, no ocultamiento — mitiga R5).
**Trade-offs aceptados**: la demo "parece ficticia" en notificaciones; se asume explícitamente.

### DD-06 — Guest booking sin auth de paciente, sin ficha clínica en MVP
**Decisión**: reserva pública con datos mínimos + token de cancelación; ningún endpoint acepta dato clínico.
**Contexto**: evita RBAC de paciente y achica el modelo; además reduce el riesgo legal (Ley 25.326 Art. 5.1 consentimiento expreso, Art. 8 datos sensibles, Art. 12.1 transferencia internacional).
**Alternativas consideradas**: registro/login de paciente; ficha clínica básica en el MVP.
**Justificación**: con $0 y una semana, auth + clínica hubieran duplicado alcance y riesgo legal (R3).
**Trade-offs aceptados**: cualquiera puede ocupar un turno (mitigado con confirmación por canal y RN05); la clínica queda para fase siguiente con consentimiento modelado.

### DD-07 — Mantenibilidad con foco en velocidad (P5 = b)
**Decisión**: priorizar código chico y explícito sobre escalabilidad o costo.
**Contexto**: un integrante, entrega próxima; lo que se evalúa es invariante + tests + trazabilidad.
**Alternativas consideradas**: optimizar escalabilidad (caché/colas) o costo (serverless).
**Justificación**: la deuda aceptada (auth mínima, sin panel, rate-limit en memoria) es barata de pagar después; la invariante bien puesta es lo caro de arreglar tarde.
**Trade-offs aceptados**: se acepta deuda deliberada documentada en 10_preguntas_abiertas.

## Supuestos inferidos

### SU-01 — Un turno ocupa un solo sillón y un solo profesional
**Supuesto**: no hay turnos multi-sillón ni multi-profesional en el MVP.
**Origen**: CU01 de Discovery ("asignando profesional, sillón/box y prestación").
**Riesgo si es falso**: habría que modelar turnos compuestos.
**Cómo validar**: preguntar a la cátedra si acepta la simplificación (asumir que sí para el MVP).

### SU-02 — Horario de atención homogéneo basta para la demo
**Supuesto**: un horario global + excepción por profesional alcanza.
**Origen**: RN03 de Discovery.
**Riesgo si es falso**: feriados y licencias complican RN03.
**Cómo validar**: fijar seed lunes–viernes 9–18 + sábado 9–12 y no modelar feriados.

### SU-03 — Teléfono o email identifican al paciente guest para RN05
**Supuesto**: normalizando (minúsculas/trim) alcanza para el límite de un activo por día.
**Origen**: RN05 + decisión guest sin DNI.
**Riesgo si es falso**: un paciente reserva dos veces con variantes del dato.
**Cómo validar**: definir en el change la clave de identidad (teléfono normalizado primero, email fallback) + test.

### SU-04 — Zona horaria única del consultorio
**Supuesto**: todo se evalúa en `America/Argentina/Buenos_Aires`.
**Origen**: restricción $0/local + consultorio chico argentino.
**Riesgo si es falso**: turnos al borde del cambio horario se evalúan mal.
**Cómo validar**: guardar `timestamptz` y testear RN03 con casos al borde del día.

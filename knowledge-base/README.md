# TurnosAR — Base de Conocimiento

Base de conocimiento generada con `kb-creator` en **Mode B interactivo forzado** (respuestas cerradas del proyecto, no inferencia desde `docs/`). Fuente de dominio: `discovery/discovery.md` + sección `discovery` de `.active-orchestrator-state.json`.

Stack cerrado: **FastAPI + Pydantic v2 + SQLAlchemy 2.0 + Alembic + PostgreSQL 16 (Docker local), pytest + httpx**. Invariante central RN02 como doble `EXCLUDE USING gist`.

## Índice de Archivos

| Archivo | Contenido |
|---------|-----------|
| [01_vision_y_objetivos.md](01_vision_y_objetivos.md) | Propósito, objetivos por actor, alcance v1.0, fuera de alcance, métricas |
| [02_descripcion_general.md](02_descripcion_general.md) | Stack, arquitectura API pura, integraciones (mock), mapa de endpoints |
| [03_actores_y_roles.md](03_actores_y_roles.md) | Recepcionista, odontólogo, paciente guest; RBAC; rutas públicas |
| [04_modelo_de_datos.md](04_modelo_de_datos.md) | Entidades, ERD, doble EXCLUDE, seed inicial |
| [05_reglas_de_negocio.md](05_reglas_de_negocio.md) | RN01–RN05 + excepciones globales |
| [06_funcionalidades.md](06_funcionalidades.md) | US-001 a US-006 por épica (CU01–CU04) |
| [07_flujos_principales.md](07_flujos_principales.md) | Reserva guest, alta recepcionista, cancelación/reprogramación, agenda del día |
| [08_arquitectura_propuesta.md](08_arquitectura_propuesta.md) | Patrones, directorios, seguridad, env vars |
| [09_decisiones_y_supuestos.md](09_decisiones_y_supuestos.md) | DD-01 a DD-07 + SU-01 a SU-04 |
| [10_preguntas_abiertas.md](10_preguntas_abiertas.md) | IN-01/IN-02 + preguntas priorizadas (Qy, Qz, RN05, rate-limit) |

## Quick Start para Desarrolladores

1. Entender el dominio → [01](01_vision_y_objetivos.md), [03](03_actores_y_roles.md)
2. Entender los datos → [04](04_modelo_de_datos.md)
3. Entender las reglas → [05](05_reglas_de_negocio.md)
4. Entender la arquitectura → [02](02_descripcion_general.md), [08](08_arquitectura_propuesta.md)
5. Implementar → [07](07_flujos_principales.md), [06](06_funcionalidades.md)
6. Antes de codificar → [10](10_preguntas_abiertas.md)

## Resumen Ejecutivo

TurnosAR es una API de turnos odontológicos donde el solapamiento por profesional y por sillón es imposible por construcción (doble `EXCLUDE` en Postgres). Reserva guest sin auth ni ficha clínica, notificaciones mockeadas, y un solo change chico (CU01+CU02) con test de concurrencia real. Todo local, $0.

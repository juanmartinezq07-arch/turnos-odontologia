# Descripción General

## Stack tecnológico

Decisión cerrada de kb-creator (Mode B, respuesta P4 verbatim): **Python con FastAPI + PostgreSQL via Docker local**.

| Capa | Tecnología | Versión mínima |
|------|-----------|----------------|
| Lenguaje | Python | 3.12 |
| API | FastAPI | 0.110+ |
| Validación / schemas | Pydantic v2 | 2.x |
| ORM | SQLAlchemy 2.0 (modo `mapped_column`, async o sync a definir en el change) | 2.0 |
| Migraciones | Alembic | 1.13+ |
| Base de datos | PostgreSQL 16 (+ extensión `btree_gist`) via Docker Compose local | 16 |
| Tests | pytest + httpx (`TestClient` / `AsyncClient`) | pytest 8, httpx 0.27+ |
| Entorno local | Docker Compose (un servicio `db`, la API corre en host o contenedor) | — |
| Notificaciones | Interfaz propia `NotificationService` + mock en memoria | — |

Sin frontend propio. La API se documenta y se prueba con OpenAPI/Swagger que genera FastAPI.

## Arquitectura general

Monolito modular de **API / backend puro**, sin frontend propio (P0-sys = b):

```
Paciente (enlace público) ─┐
                           ├─→ FastAPI (routers) → Servicios de aplicación → SQLAlchemy → PostgreSQL 16
Recepcionista / Odontólogo ┘        │                                                        │
                                    └─→ NotificationService (interfaz) → Mock ───────────────┘ (sin efecto en DB)
```

- Capa HTTP fina: routers por recurso, schemas Pydantic v2 de entrada/salida.
- Capa de aplicación: casos de uso (agendar, reservar, cancelar, consultar disponibilidad) con validaciones RN01/RN03/RN04/RN05 antes de persistir.
- Capa de persistencia: invariante RN02 como **dos constraints `EXCLUDE USING gist`** — uno por profesional y otro por sillón — sobre rango `tstzrange(inicio, fin)`. La aplicación valida para dar buen error; la base decide.
- Presupuesto $0: todo corre local. Nada de nube, nada pago, nada con verificación empresarial.

**Por qué PostgreSQL y no SQLite:** la invariante central (RN02) necesita chequeo de solapamiento concurrente a nivel de fila/rango. SQLite obligaría a serialización procedural con ventana de carrera; PostgreSQL lo resuelve declarativamente con `EXCLUDE`, que es exactamente lo que la cátedra quiere ver testeado.

## Integraciones externas

| Servicio | Propósito | Tipo | Estado en MVP |
|----------|-----------|------|---------------|
| `NotificationService` (mock) | Confirmar/recordar turnos sin costo | Interfaz interna, mock en memoria | Implementado como mock; registra llamadas, no envía nada |
| WhatsApp Business API (Meta) | Canal real de notificaciones del rubro | REST + plantillas aprobadas | **Excluido**: requiere verificación empresarial, revisión de plantillas (~24 h) y costo por mensaje (DentalSoft declara USD 0,026). Queda en backlog con cifras verificadas en el informe |
| Mercado Pago Checkout | Cobro de señas | SDK/REST + webhooks | Excluido del MVP, backlog |
| ARCA facturación electrónica | Facturación | Web services | Excluido del MVP, backlog |
| Email transaccional | Alternativa de notificación | SMTP/API | Excluido del MVP |

## API REST (resumen por recurso)

Prefijo sugerido `/api/v1`. Detalle de contratos en el change; acá el mapa:

- `GET /profesionales` — listar profesionales activos.
- `GET /sillones` — listar sillones/boxes activos.
- `GET /prestaciones` — listar prestaciones con duración (RN01).
- `GET /disponibilidad?profesional_id=&fecha=&prestacion_id=` — slots reales computados desde turnos activos + horario de atención (RN01, RN03).
- `POST /turnos` — alta por recepcionista (profesional + sillón + prestación + datos paciente guest). 409 si viola RN02/RN05.
- `POST /reservas` — reserva pública guest (mismo efecto que `POST /turnos`, sin auth, con rate-limit básico). 409 si hay conflicto.
- `GET /agenda?profesional_id=&fecha=` — agenda del día del odontólogo (CU04, lectura).
- `POST /turnos/{id}/cancelacion` o `DELETE /turnos/{id}` — cancela y libera slot (RN04).
- `POST /turnos/{id}/reprogramacion` — cancela lógicamente y crea el nuevo turno en una transacción (CU03 mínima).
- Errores: `409 Conflict` para solapamiento (RN02) y límite por paciente (RN05); `422` para validación temporal/horario (RN03).

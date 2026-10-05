# TurnosAR — Instrucciones para Agentes

> Este archivo (y su copia `CLAUDE.md`) es lo PRIMERO que todo agente lee al entrar al repo.
> Generado a partir de `knowledge-base/` y `CHANGES.md` con la skill `agents-md-generator`. No editar a mano sin re-sincronizar ambos archivos (`diff AGENTS.md CLAUDE.md` debe dar vacío).

---

## Stack Tecnológico

Decisión cerrada de kb-creator (Mode B): **Python con FastAPI + PostgreSQL via Docker local**. API/backend puro, sin frontend propio (la API se documenta y prueba con OpenAPI/Swagger de FastAPI).

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

Detalle completo: [knowledge-base/02_descripcion_general.md](knowledge-base/02_descripcion_general.md)

---

## Base de Conocimiento

La fuente de verdad del dominio vive en `knowledge-base/`. **Leé el archivo relevante ANTES de implementar.**

| Archivo | Cuándo leerlo |
|---------|---------------|
| [01_vision_y_objetivos.md](knowledge-base/01_vision_y_objetivos.md) | Entender propósito y alcance |
| [02_descripcion_general.md](knowledge-base/02_descripcion_general.md) | Stack, arquitectura API pura, integraciones (mock), mapa de endpoints |
| [03_actores_y_roles.md](knowledge-base/03_actores_y_roles.md) | Auth, RBAC, permisos (recepcionista / odontólogo / guest) |
| [04_modelo_de_datos.md](knowledge-base/04_modelo_de_datos.md) | Entidades, ERD, doble EXCLUDE, seed inicial |
| [05_reglas_de_negocio.md](knowledge-base/05_reglas_de_negocio.md) | Reglas codificadas (RN01–RN05) + excepciones globales |
| [06_funcionalidades.md](knowledge-base/06_funcionalidades.md) | Historias de usuario por épica (US-001 a US-006, CU01–CU04) |
| [07_flujos_principales.md](knowledge-base/07_flujos_principales.md) | Flujos E2E (reserva guest, alta recepcionista, cancelación/reprogramación, agenda) |
| [08_arquitectura_propuesta.md](knowledge-base/08_arquitectura_propuesta.md) | Patrones, estructura de directorios, seguridad, env vars |
| [09_decisiones_y_supuestos.md](knowledge-base/09_decisiones_y_supuestos.md) | DD-01 a DD-07 + SU-01 a SU-04 |
| [10_preguntas_abiertas.md](knowledge-base/10_preguntas_abiertas.md) | ⚠️ Inconsistencias a resolver ANTES de codear |

> ⚠️ Resolver las preguntas de prioridad **Alta** de `10_preguntas_abiertas.md` antes de arrancar el primer change: RN05 (índice parcial vs validación) y test de concurrencia real. IN-01 (RN05) la cierra C-01.

---

## Skills Disponibles

Fuente de verdad: `.atl/skill-registry.md` (generado por `skill-registry`; 7 skills de dominio + workflow openspec).

| Agente | Rol | Skills que carga |
|--------|-----|------------------|
| **Backend Core** | FastAPI / SQLModel / routers / schemas / andamiaje | `fastapi`, `fastapi-templates` |
| **Backend Concurrencia/DB** | Async, RN02 EXCLUDE, migraciones, disponibilidad | `async-python-patterns`, `supabase-postgres-best-practices` |
| **Calidad / Infra local** | TDD, pytest+httpx, Compose Postgres local | `tdd`, `python-testing-patterns`, `docker-patterns` (⚠️ ver precaución High Risk en Reglas Duras) |
| **Orquestación** | SDD / OPSX / docs | `openspec-propose`, `openspec-explore`, `openspec-apply-change`, `openspec-update-change`, `openspec-sync-specs`, `openspec-archive-change` |

Cargá la skill correspondiente al contexto ANTES de escribir código.

> Los compact rules de cada skill los resuelve el orquestador desde `.atl/skill-registry.md` (generado por `skill-registry`; no versionado — no está en el repo). Esta tabla solo mapea skill→rol.

---

## Roadmap de Changes

El plan de implementación completo está en [CHANGES.md](CHANGES.md). Resumen:

- **Total**: 1 change en 1 fase (FASE 0 — MVP Turnos, única fase).
- **Camino crítico** (1): `C-01`.
- **Primer (= único) change**: `C-01 turnos-mvp` — MVP API puro FastAPI + PostgreSQL 16 con invariante RN02 en persistencia (CU01 + CU02 encadenadas, RN01–RN05 como núcleo, CU03/CU04 en alcance mínimo operable). Governance MEDIO. Sin dependencias, sin paralelismo real (un integrante).
- **Alcance operativo C-01**: `docker-compose.yml` (servicio `db` PG16 + `btree_gist`); Alembic 001 (tablas) + 002 (doble EXCLUDE); modelos `Profesional/Sillon/Prestacion/PacienteGuest/Turno/HorarioAtencion`; `app/domain/rules.py` (RN01/RN03/RN04/RN05 puras); endpoints `POST /turnos`, `GET /disponibilidad`, `POST /reservas` (+ cancelación por token), `GET /agenda`, catálogos, `/docs`; `NotificationService` mock; auth mínima por API keys; seed ficticio; 3 archivos de test (`test_rn02_solapamiento`, `test_rn02_concurrencia`, `test_reserva_guest`).

**Antes de cualquier `/opsx:propose`**: leé [CHANGES.md](CHANGES.md), identificá las dependencias del change y los archivos de "Leer antes" (KB 04 §Turno, 05 §RN02 + excepciones, 06 §US-001/US-003, 07 §Flujo 1/2, 08 §directorios/seguridad).

---

## Reglas Duras

> No existe `~/.claude/CLAUDE.md` global en este entorno: no hay reglas universales heredadas. Las universales van acá hasta que exista el global. Son contrato; romperlas es un defecto. Formato `NUNCA X → hacer Y`.

### Universales (el global no las cubre — van en el proyecto)

- NUNCA buildear, correr migraciones destructivas ni levantar infra sin pedido explícito → proponer el comando y esperar confirmación.
- NUNCA commitear, pushear ni archivar changes sin pedido explícito → dejar los cambios en el working tree y avisar.
- NUNCA commits sin Conventional Commits ni con co-autoría IA → `feat|fix|test|docs|refactor|chore: ...` sin `Co-Authored-By`.

### Restricción INNEGOCIABLE — datos de pacientes (Ley 25.326, fundamento Art. 5.1 consentimiento / Art. 8 datos sensibles / Art. 12.1 cesión)

- NUNCA almacenar datos reales de pacientes en el repo ni en ejemplos → solo datos ficticios/sintéticos en seeds, tests, docs y ejemplos (ej: "Juan Pérez Demo", teléfonos `11-0000-0000`, mails `@example.com`).
- NUNCA extender `PacienteGuest` más allá del contacto mínimo → solo nombre + teléfono/email ficticio; sin DNI, historia clínica ni campos sensibles; todo campo clínico que llegue se rechaza con `422` (Pydantic `extra='forbid'` + rechazo explícito).
- NUNCA commitear secretos reales → `.env.example` solo con placeholders (`DATABASE_URL`, `TZ_CONSULTORIO`, `NOTIF_BACKEND=mock`, `API_KEY_*`, rate-limit); `.gitignore` debe cubrir `.env`, `__pycache__/`, y `.atl/` si corresponde.

### Stack real (Python/FastAPI + PG16 — confirmadas)

- NUNCA schema Pydantic sin `extra='forbid'` → rechazar campos no declarados (el cliente manda `inicio` pero NUNCA `fin`; RN01 calcula `fin = inicio + duración_prestación` en el servidor).
- NUNCA código Python sin `snake_case` + type hints → todo el dominio (`app/domain/rules.py` con RN01/RN03/RN04/RN05 como funciones puras testeables sin DB ni FastAPI).
- NUNCA lógica de dominio en routers ni en `main.py` → routers finos en `app/api/v1/` delegan a `app/application/` (`bookings.py`, `availability.py`); `main.py` solo cablea (app, routers, handlers, middleware). Layout obligatorio KB 08: `app/main.py`, `app/core/{config,security}.py`, `app/domain/{models,rules}.py`, `app/application/{bookings,availability}.py`, `app/notifications/{interface,mock}.py`, `app/api/v1/*`, `app/schemas/`, `alembic/versions/`, `tests/`, `docker-compose.yml`, `.env.example`.
- NUNCA settings fuera de env vars → `core/config.py` solo lee `DATABASE_URL`, `TZ_CONSULTORIO=America/Argentina/Buenos_Aires`, `NOTIF_BACKEND=mock`, `RESERVA_RATE_LIMIT`.
- NUNCA `datetime` naive → todo timezone-aware (`timestamptz`); RN03 compara contra `now()` en `America/Argentina/Buenos_Aires`.
- NUNCA introducir frontend, Celery/Redis ni ficha clínica en C-01 → API pura, notificaciones mock en proceso.

### RN02 declarativa + TDD estricto (núcleo evaluado)

- NUNCA chequear solapamiento solo en Python → la invariante RN02 vive en Postgres como doble `EXCLUDE USING gist` parcial (`profesional_id WITH =` y `sillon_id WITH =` sobre `tstzrange(inicio, fin) WITH &&`, `WHERE (estado='activo')`) + `CHECK (fin > inicio)`; Alembic 001 tablas, 002 los dos EXCLUDE (con `CREATE EXTENSION IF NOT EXISTS btree_gist` primero); nunca editar una migración aplicada. Semántica `[)` (borde que se toca NO choca). La app valida para dar buen error 409; la base decide.
- NUNCA mapear violación EXCLUDE a 500 ni parsear el mensaje → `IntegrityError` → `409` con código por nombre de constraint (`RN02_PROFESIONAL` / `RN02_SILLON` / `RN05`); Pydantic → `422`; forma de error estable `{code, message}`.
- NUNCA TDD salteado → ciclo RED-GREEN-REFACTOR por cada US y cada RN, orden RN01 → RN03 → RN02 secuencial → RN04 → RN05 → RN02 concurrencia → guest → agenda/roles; no avanzar con tests rojos.
- NUNCA mocks de DB para RN02 → tests contra Postgres 16 real (servicio `db`); tres archivos obligatorios: `test_rn02_solapamiento.py` (borde `[)`, doble eje, cancelado libera), `test_rn02_concurrencia.py` (2 POST concurrentes mismo slot → una 201 + otra 409), `test_reserva_guest.py` (e2e guest + cancelación con token + RN05 un activo/día). `GET /disponibilidad` determinista (función pura de horario + activos + duración).
- NUNCA reprogramación no atómica → US-005 en una sola transacción: si el destino choca, rollback total y el original sigue activo.

### Auth mínima, guest público, notify mock

- NUNCA auth real pesada en C-01 → API keys por env (`API_KEY_RECEPCION`, `API_KEY_ODONTOLOGO`) en `app/core/security.py`; `POST /reservas` y `POST /reservas/{token}/cancelacion` públicos (guest sin auth) con rate-limit en memoria `10/min`; odontólogo solo lee su agenda (403 ajena); `sillon_id` opcional con auto-asignación al primero libre.
- NUNCA notificar de forma bloqueante → mock best-effort tras persistir (`NOTIF_BACKEND=mock`, registra sin enviar); si falla, loguea y sigue sin rollback.

### Precaución docker-patterns (Snyk High Risk)

- NUNCA `docker compose up` ni YAML/Dockerfile generado con `docker-patterns` sin revisión humana línea por línea → verificar imagen pineada `postgres:16`, un solo servicio `db` (volumen nombrado + healthcheck `pg_isready`), `POSTGRES_PASSWORD`/`DATABASE_URL` solo por env local nunca commiteado, `5432` no expuesto más allá de `localhost` si no hace falta, e ignorar multistage/registry/healthchecks extra (fuera de alcance $0/demo local). Ejemplo: `postgresql+psycopg://turnos:turnos@localhost:5432/turnos`.

---

## Flujo de Trabajo

```
1. Leer la KB relevante (knowledge-base/)        → entender el dominio
2. Identificar el change en CHANGES.md           → respetar dependencias
3. /opsx:propose C-01-turnos-mvp                 → proposal + design + specs + tasks
4. Implementar las tasks (cargando skills)       → respetando las reglas duras
5. /opsx:archive C-01-turnos-mvp + marcar [x]    → cerrar el change
```

Aplicar TODAS las reglas duras en cada paso. Ante conflicto entre la KB y este archivo, las reglas duras prevalecen. NO crear changes ni código fuera de un change propuesto. NO tocar `step` de `.active-orchestrator-state.json` (lo avanza el orquestador).

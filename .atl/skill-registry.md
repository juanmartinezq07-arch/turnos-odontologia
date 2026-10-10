# Skill Registry

**Delegator use only.** Any agent that launches sub-agents reads this registry to resolve compact rules, then injects them directly into sub-agent prompts. Sub-agents do NOT read this registry or individual SKILL.md files.

Scope: proyecto **turnos-odontologia (TurnosAR)** — API FastAPI + PostgreSQL 16 (Docker local), pytest + httpx, TDD estricto. Change vigente: **C-01 turnos-mvp** (CU01 + CU02, RN01–RN05, ver `CHANGES.md`).

> **Restriccion dura del proyecto:** NUNCA almacenar datos reales de pacientes en el repo ni en ejemplos/seeds/tests. `PacienteGuest` solo lleva contacto ficticio (nombre + telefono/email de ejemplo). Ningun endpoint acepta ni persiste datos clinicos; si llega un campo clinico, rechazar con 422.

> **Precaucion — `docker-patterns` (Snyk High Risk):** sus patrones de Compose/Dockerfile son utiles para C-01 pero la skill esta marcada High Risk. Todo YAML/Dockerfile generado con ella debe revisarse linea por linea antes de ejecutar: nada de secretos en el repo, `POSTGRES_PASSWORD` solo via env local, puerto de `db` no expuesto mas alla de lo necesario, imagen pineada `postgres:16`, y `docker compose up` solo tras revision humana.

## User Skills

| Trigger | Skill | Path |
|---------|-------|------|
| FastAPI endpoints, routers, Pydantic v2, exception handlers | fastapi | `~/.config/opencode/skills/fastapi/SKILL.md` (declarada en find-skill; SKILL.md no presente en disco al generar registry) |
| FastAPI project scaffolding, layout, main factory, settings | fastapi-templates | `~/.config/opencode/skills/fastapi-templates/SKILL.md` (declarada; no presente en disco) |
| async/await, AsyncSession, concurrency, background tasks | async-python-patterns | `~/.config/opencode/skills/async-python-patterns/SKILL.md` (declarada; no presente en disco) |
| pytest, httpx, fixtures, coverage of business rules | python-testing-patterns | `~/.config/opencode/skills/python-testing-patterns/SKILL.md` (declarada; no presente en disco) |
| test-driven development, RED-GREEN-REFACTOR | tdd | `~/.config/opencode/skills/tdd/SKILL.md` (declarada; no presente en disco) |
| Postgres EXCLUDE, gist, RLS, migrations, btree_gist | supabase-postgres-best-practices | `~/.config/opencode/skills/supabase-postgres-best-practices/SKILL.md` (declarada; no presente en disco) |
| Docker Compose, Postgres service, local dev infra | docker-patterns | `~/.config/opencode/skills/docker-patterns/SKILL.md` (declarada; no presente en disco — ver precaucion High Risk arriba) |
| "openspec propose" or "opsx propose" | openspec-propose | `.agents/skills/openspec-propose/SKILL.md` |
| "openspec explore" or "opsx explore" | openspec-explore | `.agents/skills/openspec-explore/SKILL.md` |
| "openspec apply", "opsx apply" or "openspec implement" | openspec-apply-change | `.agents/skills/openspec-apply-change/SKILL.md` |
| "openspec update change" or "opsx update" | openspec-update-change | `.agents/skills/openspec-update-change/SKILL.md` |
| "openspec sync" or "opsx sync" | openspec-sync-specs | `.agents/skills/openspec-sync-specs/SKILL.md` |
| "openspec archive" or "opsx archive" | openspec-archive-change | `.agents/skills/openspec-archive-change/SKILL.md` |

## Compact Rules

Pre-digested rules per skill. Delegators copy matching blocks into sub-agent prompts as `## Project Standards (auto-resolved)`.

### fastapi — matchea C-01: POST /turnos, GET /disponibilidad, POST /reservas, GET /agenda, catalogos
- Routers finos en `app/api/v1/` (turnos, reservas, disponibilidad, agenda); los routers NUNCA tocan la DB directo — delegan a `app/application/` (bookings.py, availability.py).
- Pydantic v2 en el borde: request/response schemas estrictos; el cliente manda `inicio` pero NUNCA `fin` (RN01 lo calcula el servidor como `inicio + duracion_prestacion`); rechazar campos clinicos con 422.
- Exception handlers globales en `app/main.py`: `IntegrityError` por EXCLUDE → 409 con codigo de regla (`RN02_PROFESIONAL` / `RN02_SILLON` / `RN05`), nunca 500; validacion Pydantic → 422.
- Auth minima por rol en `app/core/security.py` via API keys por env (`API_KEY_RECEPCION`, `API_KEY_ODONTOLOGO`); `POST /reservas` y `POST /reservas/{token}/cancelacion` son publicos (guest booking), el resto exige key; odontologo solo lee su agenda (403 ajena).
- `GET /docs` y `/openapi.json` siempre habilitados; respuestas de error con forma estable `{code, message}` donde `code` es el codigo RN.
- Notificacion mock best-effort: se dispara tras persistir, si falla no hace rollback del turno.

### fastapi-templates — matchea C-01: andamiaje del repo
- Layout obligatorio (KB 08): `app/main.py` (factory), `app/core/{config,security}.py`, `app/domain/{models,rules}.py`, `app/application/{bookings,availability}.py`, `app/notifications/{interface,mock}.py`, `app/api/v1/*`, `app/schemas/`, `alembic/versions/`, `tests/`, `docker-compose.yml`, `.env.example`.
- `main.py` solo cablea: crea app, registra routers, handlers y middleware; nada de logica de dominio ahi.
- `core/config.py`: settings solo via env vars (`DATABASE_URL`, `TZ_CONSULTORIO=America/Argentina/Buenos_Aires`, `NOTIF_BACKEND=mock`, `RESERVA_RATE_LIMIT`); `.env.example` con placeholders, NUNCA secretos reales.
- Seed MVP minimo: 2–3 profesionales, 2 sillones, 3 prestaciones (30/45/90 min), horario Lun–Vie 9–18 + Sab 9–12, 1 turno activo + 1 cancelado de ejemplo, todo ficticio.
- No introducir frontend,Celery/Redis ni ficha clinica: C-01 es API pura, notificaciones mock en proceso.

### async-python-patterns — matchea C-01: concurrencia RN02, disponibilidad, notify no bloqueante
- Todo datetimes timezone-aware (`timestamptz`); RN03 compara contra `now()` en `America/Argentina/Buenos_Aires`, nunca naive `datetime.now()`.
- SQLAlchemy 2.0 `AsyncSession` + transacciones explicitas; reprogramacion (US-005) atomica: update-or-insert del destino dentro de la misma transaccion; si el destino choca (EXCLUDE), rollback total y el original sigue activo.
- No bloquear el request en notificaciones: `await notifier.notificar(...)` best-effort con try/except que loguea y sigue; `NOTIF_BACKEND=mock` en MVP.
- `POST /reservas` publico con rate-limit en memoria `10/min` (suficiente MVP); no inventar store distribuido.
- Test de concurrencia real (`test_rn02_concurrencia.py`): 2 coroutines/hilos contra el mismo slot en Postgres real → exactamente una 201 + otra 409; no mockear la DB en ese test.
- Auto-asignacion de sillon: si `POST /reservas` viene sin `sillon_id`, elegir el primer sillon libre del intervalo dentro de la transaccion (SELECT ... FOR UPDATE o relying en EXCLUDE + retry unico).

### python-testing-patterns — matchea C-01: test_rn02_solapamiento, test_rn02_concurrencia, test_reserva_guest
- Tres archivos de test obligatorios: `test_rn02_solapamiento.py` (borde `[)` que se toca NO choca, doble eje profesional/sillon, cancelado libera slot), `test_rn02_concurrencia.py` (2 POST concurrentes mismo slot → 201+409 contra Postgres real), `test_reserva_guest.py` (e2e guest + cancelacion con token + RN05 un activo/dia).
- Tests contra Postgres 16 real (servicio `db` del compose), NUNCA SQLite para RN02 — SQLite no enforcea EXCLUDE y daria falsos verdes.
- Fixtures: profesionales/sillones/prestaciones de prueba con nombres ficticios; limpiar `turno` entre tests (truncate o savepoints); fijar zona horaria del consultorio en fixtures.
- Aserciones por codigo de regla (`RN02_PROFESIONAL`, `RN02_SILLON`, `RN05`), no solo por status: 409 exige `code` correcto; 422 para pasado/fuera-de-horario/campo clinico.
- Determinismo: `GET /disponibilidad` debe ser funcion pura de (horario, turnos activos, duracion RN01) — sin random ni clock implicito salvo `now()` inyectable.

### tdd — matchea C-01: TDD estricto en todo el change
- Ciclo RED-GREEN-REFACTOR obligatorio por cada US y por cada RN: escribir el test que falla primero (`test_rn02_*`, criterios de `06_funcionalidades.md`), luego el minimo codigo que lo hace pasar.
- Orden sugerido: RN01 (calculo `fin`) → RN03 (pasado/horario) → RN02 secuencial → RN04 (cancelar libera) → RN05 (1 activo/dia) → RN02 concurrencia → endpoints guest → agenda/roles.
- `app/domain/rules.py` como funciones puras (RN01/RN03/RN04/RN05) testeables sin DB ni FastAPI; RN02 vive en la DB (EXCLUDE), no duplicar su logica en Python mas alla de la validacion previa amable (409 anticipado).
- Un test por comportamiento, nombres que citan la regla (`test_rn02_borde_que_se_toca_no_choca`); nada de tests que verifiquen implementacion interna (mocks de SQLAlchemy).
- No avanzar al siguiente US con tests rojos; la demo de catedra corre la suite completa antes de presentar.

### supabase-postgres-best-practices — matchea C-01: invariante RN02 en persistencia
- Habilitar `CREATE EXTENSION IF NOT EXISTS btree_gist;` en la migracion antes de crear los constraints (servicio `db` Postgres 16).
- Doble constraint parcial, ambos con `WHERE (estado = 'activo')` para que cancelados no bloqueen (RN04):
  `EXCLUDE USING gist (profesional_id WITH =, tstzrange(inicio, fin) WITH &&)` y `EXCLUDE USING gist (sillon_id WITH =, tstzrange(inicio, fin) WITH &&)`, mas `CHECK (fin > inicio)`.
- Rangos con semantica `[)` (borde que se toca no choca): usar `tstzrange(inicio, fin)` por defecto `'[)'`; testear `inicio_nuevo == fin_existente` como NO conflicto.
- RN05 (max 1 activo por paciente/dia): indice unico parcial sobre (contacto_normalizado, fecha) `WHERE estado='activo'` o validacion + test de carrera — lo cierra el change, pero debe quedar cubierto por test.
- Migraciones Alembic numeradas: 001 tablas (`profesional`, `sillon`, `prestacion`, `paciente_guest`, `turno`, `horario_atencion`), 002 los dos EXCLUDE; nunca editar una migracion ya aplicada, siempre nueva.
- Mapear violacion de EXCLUDE a 409 en la app (`IntegrityError` → `RN02_PROFESIONAL`/`RN02_SILLON`); distinguir que constraint fallo por el nombre del constraint, no por parsear el mensaje.

### docker-patterns — matchea C-01: compose local con Postgres 16 — VER PRECAUCION HIGH RISK ARRIBA
- `docker-compose.yml` minimo: un solo servicio `db` (`image: postgres:16`, extension `btree_gist` habilitada por migracion, volumen nombrado para datos, healthcheck `pg_isready`); la API corre fuera de Docker en el MVP.
- NUNCA commitear secretos: `POSTGRES_PASSWORD` y `DATABASE_URL` solo por env local / `.env` no commiteado; el repo solo lleva `.env.example` con placeholders.
- Antes de `docker compose up`: revisar el YAML generado linea por linea (puertos, volumenes, imagen pineada); no exponer `5432` mas alla de `localhost` si no hace falta.
- `DATABASE_URL` de ejemplo: `postgresql+psycopg://turnos:turnos@localhost:5432/turnos`; `TZ_CONSULTORIO=America/Argentina/Buenos_Aires`.
- Si la skill sugiere Dockefile multistage/registry/healthchecks extra: IGNORAR para C-01 (fuera de alcance, $0 infra, demo local).

### openspec-propose — matchea C-01: propuesta del change turnos-mvp
- Propone el change completo en un paso (diseno + specs + tasks); artefactos en espanol, headings estructurales y keywords SHALL/MUST en ingles (ver `openspec/config.yaml`).
- Leer antes de proponer: `CHANGES.md` (scope C-01), KB `04/05/06/07/08` y `discovery/discovery.md`; no redefinir RN01–RN05 ni renombrar codigos de regla.
- Un solo change chico y demostrable (catedra 25% = 1 change): CU01+CU02 + CU03/CU04 minimo operable; sin pagos, sin ficha clinica, notificaciones mock.
- Incluir Non-goals explicitos: WhatsApp real, Mercado Pago, ARCA, odontograma, multi-sucursal.

### openspec-explore — matchea C-01: thinking partner pre/durante el change
- Usar para aclarar requisitos antes de codificar (ej. RN05 indice vs validacion, auto-asignacion de sillon, ventana de rate-limit).
- No escribe codigo ni artefactos finales; salida = entendimiento compartido que luego consume propose/update.
- Toda decision que cambie RN01–RN05 o el invariante EXCLUDE debe quedar registrada y reflejarse en el change.

### openspec-apply-change — matchea C-01: implementacion de tasks
- Implementa las tasks del change en orden, con TDD estricto y tests contra Postgres real para RN02.
- Si una task revela que el plan choca con RN02/C-01, detener y pedir `opsx update` en vez de improvisar fuera del plan.
- Al terminar cada US, correr su test correspondiente antes de pasar al siguiente.

### openspec-update-change — matchea C-01: revision del plan
- Revisa artefactos existentes manteniendolos coherentes; nunca edita codigo (solo planificacion).
- Usar cuando aparece nueva informacion (ej. decision RN05, ajuste de seed, recorte de alcance por plazo de una semana).
- Mantiene trazabilidad Discovery → KB → CHANGES → change.

### openspec-sync-specs — matchea C-01: sincronizar delta specs
- Sincroniza delta specs del change a las specs principales sin archivar; usar cuando el invariante o endpoints ya estan estables y se quiere consolidar.
- No usar a mitad de C-01 salvo indicacion del orquestador; el flujo normal es propose → apply → archive.

### openspec-archive-change — matchea C-01: cierre del change
- Solo cuando C-01 esta implementado y verificado (suite verde + demo guest booking + concurrencia 201/409).
- Archiva con `openspec archive`, marca `[x]` en `CHANGES.md`, y deja el repo listo para video/reflexion de catedra.

## Project Conventions

| File | Path | Notes |
|------|------|-------|
| CHANGES.md (indice canonico, leer antes de cualquier /opsx:propose) | `CHANGES.md` | Define C-01 turnos-mvp, scope, governance MEDIO, "Leer antes" |
| KB vision | `knowledge-base/01_vision_y_objetivos.md` | — |
| KB descripcion | `knowledge-base/02_descripcion_general.md` | — |
| KB actores y roles | `knowledge-base/03_actores_y_roles.md` | Matriz de autorizacion (recepcionista/odontologo/guest) |
| KB modelo de datos | `knowledge-base/04_modelo_de_datos.md` | §Turno: doble EXCLUDE, btree_gist, borde `[)`, RN05 |
| KB reglas de negocio | `knowledge-base/05_reglas_de_negocio.md` | §RN02 invariante central + excepciones globales 409/422, mock best-effort |
| KB funcionalidades | `knowledge-base/06_funcionalidades.md` | §US-001 + §US-003 criterios de aceptacion del nucleo |
| KB flujos | `knowledge-base/07_flujos_principales.md` | §Flujo 1 + §Flujo 2 (reserva/alta, error concurrente) |
| KB arquitectura | `knowledge-base/08_arquitectura_propuesta.md` | Estructura de directorios, seguridad, env vars |
| KB decisiones | `knowledge-base/09_decisiones_y_supuestos.md` | Stack FastAPI+PG16, guest sin auth, mock notify |
| KB preguntas abiertas | `knowledge-base/10_preguntas_abiertas.md` | IN-01 (RN05) la cierra C-01 |
| KB index | `knowledge-base/README.md` | — |
| Discovery | `discovery/discovery.md` | Fuente: problema, CU01–CU04, RN01–RN05, R1–R5, guest sin auth, mock notify |
| OpenSpec config | `openspec/config.yaml` | Artefactos en es, headings + SHALL/MUST en ingles |
| Orquestador state | `.active-orchestrator-state.json` | v4, step find-skill — no avanzar el step desde este registry |

Read the convention files listed above for project-specific patterns and rules. All referenced paths have been extracted — no need to read index files to discover more.

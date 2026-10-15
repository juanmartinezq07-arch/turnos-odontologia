# CHANGES — Secuencia de Implementación

> Índice canónico de todos los changes de **TurnosAR**. Cada change es atómico: un agente lo implementa en una sesión (~4-6 h).
> **Leer antes de cualquier `/opsx:propose`.** `C-01` fue implementado y archivado (`openspec/changes/archive/2026-10-03-turnos-mvp/`) y es lo que se entrega; `C-20`…`C-35` quedan `[ ]`.

> **Por qué este árbol y no el anterior.** La v1 (7 changes, camino crítico lineal `C-01→C-02→C-03→C-04`) no representaba el árbol de conocimientos: trataba `disponibilidad`, `catálogos` y `agenda` como dependencias sucesivas de la reserva guest —son paralelas— y **ocultaba la rama de persistencia**, que es dependencia dura porque la migración 003 dropeó `token_cancelacion`, `cancelled_at` y `rn05_un_activo_por_dia`. Corregido en § "Roadmap anterior". `C-02`…`C-07` quedan reservados, no reutilizables.

---

## Cómo usar este documento

1. Identificá el change: próximo `[ ]` cuyas dependencias estén todas en `[x]` (usá el árbol y los GATES).
2. Leé la KB: los archivos de "Leer antes", sobre todo las reglas RN-* y los escenarios US-* que cita el Scope.
3. Proponé: `/opsx:propose C-NN-nombre-del-change` (el slug en kebab-case es el título del change).
4. Implementá y archivá: `/opsx:apply` con Strict TDD (todo escenario de la KB tiene un test de pytest) y luego `/opsx:archive`.
5. Marcá el checkbox: `[ ]` → `[x]`. Con Governance **ALTO** o **CRITICO**, frená y esperá revisión antes de escribir código.
6. Convenciones: intervalos semiabiertos `[inicio, fin)`; instantes en UTC (`timestamptz` y `datetime` con zona); hora local `America/Argentina/Buenos_Aires`; `now` inyectado; solo datos ficticios; el dominio es la autoridad de las reglas y no importa FastAPI, SQLAlchemy ni Redis (DD-06, DD-07). Secretos solo en `.env`; en el repo, `.env.example` sin valores.

## Convenciones de lectura del árbol

Sin este contrato el árbol es ambiguo.

| # | Convención | Se lee |
|---|-----------|---------|
| 1 | **Sangría = dependencia dura** | el hijo no arranca hasta que el padre está `[x]` |
| 2 | **`(también requiere X)`** | dependencia obligatoria fuera de la línea del padre (cruza ramas) |
| 3 | **`A + B + C` bajo el `│`** | confluencia: requiere todas las ramas listadas |
| 4 | **Hermanos al mismo nivel** | paralelizables, mismo GATE |
| 5 | **Prefijo = capa** | `persistencia-` / `api-` / `disponibilidad-` / `ui-` / `decision-`: es lo que hace esto un árbol de conocimientos y no una lista |

## Árbol de dependencias

```
C-01 turnos-mvp                                       [x] ARCHIVADO
 │    └── fundacion + dominio + docker PG16 + Alembic 001/002/003
 │         + 6 modelos + POST /turnos + 26 tests
 │
 ├── PERSISTENCIA — el esquema va antes que la API ────────────────────────
 │    ├── C-20 persistencia-cancelacion-rn04      [ ]
 │    └── C-21 persistencia-token-y-rn05          [ ]
 │           └── C-26 rn05-limite-paciente         [ ]
 │
 ├── API DE LECTURA — sin esquema nuevo ───────────────────────────────────
 │    ├── C-24 api-catalogos-publicos            [ ]
 │    ├── C-25 disponibilidad-real               [ ]
 │    └── C-27 api-agenda-odontologo             [ ]
 │
 ├── TRANSVERSAL ─────────────────────────────────────────────────────────
 │    └── C-28 notificaciones-mock               [ ]
 │
 ├── CONFLUENCIAS ────────────────────────────────────────────────────────
 │    C-21 + C-24 + C-25 + C-26
 │    └── C-29 reservas-guest                    [ ]
 │
 │    C-01 + C-26 + C-28
 │    └── ▸ HITO us-001-completa (5/5 criterios) — no es un change
 │
 │    C-01
 │    └── C-30 decision-frontend-alcance         [ ]
 │
 └── C-29 + C-23 + C-27 + C-30
      └── C-31 frontend-base-react-vite           [ ] BLOQUEADO
           ├── C-32 ui-agenda-diaria              [ ] (también C-27)
           ├── C-33 ui-dar-turno-con-errores      [ ] (también C-24, C-25)
           ├── C-34 ui-reprogramar-cancelar-y-estados [ ] (también C-22, C-23)
           └── C-35 ui-reserva-publica            [ ] (también C-24, C-25, C-29)
```

**Por qué estas dependencias.** El esquema va antes que la API: sin `C-20` no existe la cancelación, sin `C-21` no hay token ni invariante RN05. El contrato va antes del consumidor: `KB-07 §Flujo 1` es *descubrir profesional/prestación → ver slots → reservar*, así que sin `C-24` y `C-25` la reserva se desarrolla contra datos inventados. Y la decisión va antes del frontend: `C-31`…`C-35` dependen de contratos que solo existen al final **y** de derogar DD-01, que la KB prohíbe — por eso están BLOQUEADOS, no pendientes. Dos criterios de US-001 (`KB-06` L14 RN05 y L15 notificación) nunca se implementaron; los cubren `C-26` y `C-28` **sin replanificar `POST /turnos`**.

### Gates

```
GATE 0  → C-01                                                       [CERRADO]
GATE 1  → C-20 ‖ C-24 ‖ C-25 ‖ C-27 ‖ C-28 ‖ C-30      (6 en paralelo)
GATE 2  → C-21 ‖ C-22
GATE 3  → C-23 ‖ C-26                                (cierra el HITO us-001)
GATE 4  → C-29
GATE 5  → C-31                                       (bloqueado por C-30)
GATE 6  → C-32 ‖ C-33 ‖ C-34 ‖ C-35                  (4 en paralelo)
```

### Camino crítico

```
A) C-01 → C-20 → C-22 → C-23 → C-31 → C-34
B) C-01 → C-21 → C-26 → C-29 → C-31 → C-35
```

Dos cadenas de 6 nodos: el frontend **no** es el cuello de botella y el trabajo real se reparte en GATE 1. `C-30` es transversal y no está en ninguna.
**Arranque más rápido:** `C-20 → C-22` (cancelación, ~85 líneas, sin tocar la invariante RN02) o `C-24` (catálogos, demostrable en Swagger al instante). **Evitar empezar por** `C-21`/`C-26` sin haber leído el aviso de regresión de `C-26`.

### Plan con agentes

```
 Paso │ Agente A (API)      │ Agente B (Persistencia+Lectura) │ Agente C (Transversal)
 ─────┼─────────────────────┼───────────────────────────────┼─────────────────────────
   1  │ —                   │ C-20 · C-24 · C-25 · C-27     │ C-28 · C-30
   2  │ C-22                │ C-21                          │ verifica GATE 2
   3  │ C-23 · C-26          │ —                            │ —
   4  │ C-29                │ —                            │ HITO us-011
   5  │ C-32…C-35            │ —                            │ trazabilidad final
```

> Un solo integrante: sin paralelismo explotable, la tabla se mantiene por contrato de formato. **Solo `C-01` se entrega.**

### Trazabilidad KB → change

| Requisito | Change | Estado |
|---|---|---|
| RN01 `fin` en servidor | `C-01` | COMPLETADO |
| RN02 doble `EXCLUDE`, borde `[)`, carrera | `C-01` | COMPLETADO |
| RN03 pasado / horario → 422 | `C-01` | COMPLETADO |
| **RN04** cancelación libera slot | `C-20`+`C-22` | PENDIENTE |
| **RN05** 1 activo/paciente/día → 409 | `C-21`+`C-26` | PENDIENTE |
| US-001 (CU01) | `C-01`+`C-26`+`C-28` | COMPLETADO **3/5 CA** |
| US-002 (CU01) | `C-25` | PENDIENTE |
| US-003 (CU02) | `C-29` (+`C-21`,`C-24`,`C-25`,`C-26`) | PENDIENTE |
| US-004 (CU03) | `C-22`+`C-29`+`C-28` | PENDIENTE |
| US-005 (CU03) | `C-23` | PENDIENTE |
| US-006 (CU04) | `C-27` | PENDIENTE |
| KB-03 rutas públicas (5) | `C-24`,`C-25`,`C-29` | PENDIENTE (`/docs` ya existe) |
| KB-03 RBAC odontólogo (403) | `C-27` | PENDIENTE |
| KB-05 notif best-effort | `C-28` | PENDIENTE |
| KB-04 `idx_turno_paciente_fecha` | `C-20` | PENDIENTE |
| KB-08 layout (`notifications/`,`availability.py`,`reservas.py`,`agenda.py`) | `C-28`,`C-25`,`C-29`,`C-27` | PENDIENTE |
| KB-10 §RN05 (pregunta Alta) | `C-21` | PENDIENTE (la cierra) |
| DD-01 / KB-01 §Fuera de alcance | `C-30`→`C-31`…`C-35` | **BLOQUEADO** |

**Sin change, declarado:** consentimiento Ley 25.326 Art. 5.1 (`KB-10` Media: "documentado, no persistido"); notificaciones reales (DD-05: costo + verificación empresarial); pagos, ficha clínica, multi-sucursal, obras sociales (`KB-01 §Fuera de alcance`); **bloqueos de agenda, agenda semanal e historial de transiciones no existen en la KB** — si la cátedra los quiere, se agregan a la KB primero y después entran al roadmap. Ningún change está EN PROGRESO: no hay código a medio escribir.

---

## FASE 1 — Base e invariante (entregado)

### [C-01] `turnos-mvp`
- **Estado**: `[x]` archivado (`openspec/changes/archive/2026-10-03-turnos-mvp/`)
- **Scope**: MVP API puro FastAPI + PostgreSQL 16 con RN02 en persistencia (solo CU01; CU02/CU03/CU04 fuera). `docker-compose.yml` (`db` PG16 + `btree_gist`); Alembic 001 tablas, 002 doble `EXCLUDE USING gist` `WHERE (estado='activo')` + `CHECK (fin > inicio)`, 003 recorte; modelos `Profesional/Sillon/Prestacion/PacienteGuest/Turno/HorarioAtencion`; `rules.py` con RN01 y RN03 puras; `POST /turnos` con API key → 201 con `fin` calculado, 409 `RN02_PROFESIONAL`/`RN02_SILLON`, 422 pasado/fuera de horario; `IntegrityError` → 409 por nombre de constraint, nunca 500; campo clínico → 422; seed ficticio + `.env.example`; 26 tests en 5 archivos contra Postgres real.
- **Dependencias**: ninguna
- **Governance**: MEDIO — invariante de concurrencia RN02, núcleo evaluado
- **Leer antes**: `KB-04 §Turno` · `KB-05 §RN02 + §Excepciones` · `KB-06 §US-001` · `KB-07 §Flujo 2` · `KB-08 §directorios/seguridad`

> **Verificado (2026-10-15):** `26 passed` en 3.38 s contra PostgreSQL 16.15 (Debian, `btree_gist 1.7`), sin SQLite ni mocks.
>
> **Déficit (documentado, no se replanifica `POST /turnos`):** US-001 tiene **5** criterios (`KB-06` L11–L15) y C-01 cumple **3**. Faltan **RN05** (L14) y **notificación mock** (L15) → `C-26` y `C-28`.
>
> **Deuda con fecha:** `tests/conftest.py:8` usa `asyncio.WindowsSelectorEventLoopPolicy()`, eliminada en Python 3.16: con 3.16 la suite deja de colectar. Se corrige en `C-21`.

---

## FASE 2 — Cimientos del resto (GATE 1, sin dependencias entre sí)

### [C-20] `persistencia-cancelacion-rn04`
- **Estado**: `[ ]` pendiente
- **Scope**: Alembic **004** `ADD COLUMN cancelled_at TIMESTAMPTZ` + `idx_turno_paciente_fecha` (el único índice de `KB-04 §Turno` que falta). `downgrade` reversible; test que verifica que `estado`, `fin` y ambos EXCLUDE siguen intactos.
- **Dependencias**: `C-01`
- **Governance**: BAJO — una columna y un índice; no introduce invariante
- **Leer antes**: `KB-04 §Turno` · `KB-05 §RN04` · `KB-07 §Flujo 3` · `KB-10 §IN-02`

### [C-21] `persistencia-token-y-rn05`
- **Estado**: `[ ]` pendiente
- **Scope**: Alembic **005**: `token_cancelacion TEXT UNIQUE` (DDL en el `downgrade` de la 003) + índice único parcial `rn05_un_activo_por_dia (paciente_id, (inicio AT TIME ZONE 'America/Argentina/Buenos_Aires')::date) WHERE estado='activo'`. **Cierra la pregunta de prioridad Alta de `KB-10`**: RN05 como invariante declarativa, igual que RN02. Tests: 2 activos mismo paciente/día → viola el índice; otro día → commit; token repetido → unicidad.
- **Dependencias**: `C-01`
- **Governance**: MEDIO — invariante en persistencia: la base decide, como RN02
- **Leer antes**: `KB-04 §Turno` · `KB-05 §RN05 + §Excepciones` · `KB-09 §DD-06 + §SU-03` · `KB-10 §RN05`

### [C-24] `api-catalogos-publicos`
- **Estado**: `[ ]` pendiente
- **Scope**: `GET /profesionales`, `/sillones`, `/prestaciones` — solo activos, con `duracion_min` visible (RN01). **Públicos** (3 de las 5 rutas de `KB-03`). Tests: 200 sin credencial, solo activos, presentes en `/openapi.json`.
- **Dependencias**: `C-01`
- **Governance**: BAJO — tres endpoints de lectura sobre entidades ya persistidas
- **Leer antes**: `KB-02 §API REST` · `KB-03 §Rutas públicas` · `KB-04 §Profesional/§Sillon/§Prestacion`

### [C-25] `disponibilidad-real`
- **Estado**: `[ ]` pendiente
- **Scope**: `app/application/availability.py` como **función pura** de (HorarioAtencion − turnos activos, duración RN01, `now()` **inyectado**); sin random ni clock implícito. `GET /disponibilidad?profesional_id=&fecha=&prestacion_id=` (público). El bloque `[inicio, fin)` completo debe entrar en el horario (RN03); descarta el pasado. Tests: huecos correctos, bloque que no entra completo, borde `[)` no pisa activos, **determinismo** (dos consultas seguidas devuelven lo mismo).
- **Dependencias**: `C-01`
- **Governance**: BAJO — lógica de lectura pura, sin invariantes nuevas ni escrituras
- **Leer antes**: `KB-06 §US-002` · `KB-07 §Flujo 1` · `KB-05 §Temporalidad` · `KB-04 §HorarioAtencion`

### [C-27] `api-agenda-odontologo`
- **Estado**: `[ ]` pendiente
- **Scope**: `GET /agenda?profesional_id=&fecha=` con activos ordenados por `inicio`, con prestación (y duración RN01), sillón y paciente. `require_odontologo` con `API_KEY_ODONTOLOGO` (hoy solo hay `require_recepcion`); agenda ajena → **403**. `?incluir_cancelados=true` como filtro explícito. Tests: orden, 403, fecha inválida → 422, sin credencial → 401.
- **Dependencias**: `C-01`
- **Governance**: BAJO — endpoint de lectura; agrega el rol odontólogo sin reglas nuevas
- **Leer antes**: `KB-06 §US-006` · `KB-07 §Flujo 4` · `KB-03 §RBAC` · `KB-08 §Seguridad`

### [C-28] `notificaciones-mock`
- **Estado**: `[ ]` pendiente
- **Scope**: `app/notifications/{interface,mock}.py` (la interfaz que `KB-02`/`KB-08`/DD-05 exigen y hoy no existe) + llamada **best-effort post-commit** en toda escritura: si el mock falla se loguea y **el turno igual persiste** con 201 (`KB-05 §Excepciones`). `NOTIF_BACKEND=mock` en config y `.env.example`. Tests: llamada registrada; con mock que lanza, el turno queda persistido.
- **Dependencias**: `C-01`
- **Governance**: BAJO — interfaz + mock en memoria, sin canal externo ni costo
- **Leer antes**: `KB-09 §DD-05` · `KB-05 §Excepciones` · `KB-08 §Patrones` · `KB-02 §Integraciones`

### [C-30] `decision-frontend-alcance`
- **Estado**: `[ ]` pendiente — **bloquea `C-31`…`C-35`**
- **Scope**: resolver por escrito si DD-01 se mantiene o se deroga. **No escribe código de UI**: salida documental en `KB-09 §DD-08` y `KB-01 §Fuera de alcance`. Preguntas: ¿se deroga DD-01?, ¿cómo obtiene credencial el navegador sin exponer la API key (`KB-08 §Seguridad`)?, ¿qué costo/plazo?
- **Dependencias**: `C-01`
- **Governance**: MEDIO — toca una decisión de alcance cerrada
- **Leer antes**: `KB-09 §DD-01` · `KB-01 §Fuera de alcance` · `KB-08 §Seguridad` · `docs/discovery §alcance del change`

---

## FASE 3 — Agenda operable (GATE 2–4)

### [C-22] `api-cancelacion-recepcionista`
- **Estado**: `[ ]` pendiente
- **Scope**: `POST /turnos/{id}/cancelacion` (API key) → `estado='cancelado'` + `cancelled_at=now()`; el `WHERE (estado='activo')` de los EXCLUDE deja de contar el rango → **el slot se libera**. **Idempotente**: no cambia `cancelled_at`. Tests: cancela, idempotencia, 401 sin credencial, 404 `NO_ENCONTRADO` si el id no existe.
- **Dependencias**: `C-01`, `C-20`
- **Governance**: MEDIO — escritura que libera un slot + idempotencia
- **Leer antes**: `KB-06 §US-004` · `KB-07 §Flujo 3` · `KB-05 §RN04` · `KB-04 §Turno`

### [C-23] `api-reprogramacion-atómica`
- **Estado**: `[ ]` pendiente
- **Scope**: `POST /turnos/{id}/reprogramacion` en **una sola transacción**: marca el original `cancelado` e inserta el nuevo. Si el destino viola RN02/RN03/RN05 → **rollback total** y el original sigue `activo`. Tests: destino libre → 200; destino tomado → 409 con el original **intacto** (assert en DB); al pasado → 422 sin tocar el original.
- **Dependencias**: `C-22`, `C-20`
- **Governance**: **ALTO** — atomicidad y ventana de carrera entre cancelar e insertar. **Frenar y esperar revisión**
- **Leer antes**: `KB-06 §US-005` · `KB-07 §Flujo 3` · `KB-05 §RN04` · `KB-04 §Turno`

### [C-26] `rn05-limite-paciente`
- **Estado**: `[ ]` pendiente
- **Scope**: RN05 de punta a punta (criterio L14 de US-001): 1 turno `activo` por paciente y día calendario (identidad = teléfono normalizado, fallback email — SU-03) → **409 `code="RN05"`**. Extender `conflict_code_from_integrity_error`: hoy mapea a `"CONFLICTO"` todo constraint que no sea `rn02_*`, hay que agregarle `rn05_un_activo_por_dia`. Tests: mismo paciente mismo día → 409 `RN05`; distinto → 201; otro día → 201.
  **⚠️ Regresión en la suite**: los fixtures de `C-01` usan **un único paciente** (`11-0000-0001`) para dos turnos activos del mismo día; con el índice de `C-21` hay que **parametrizarlos con pacientes distintos** (criterio: los 26 siguen verdes). Se rompen `test_rn02_solapamiento.py::test_borde_que_se_toca_no_choca` y `test_turnos_api.py::test_borde_201` (fallan directo); `::test_choque_mismo_profesional_distinto_sillon` y `::test_choque_mismo_sillon_distinto_profesional` quedan con assert frágil (RN02 y RN05 chocan a la vez, el assert exige `rn02_profesional` exacto); `test_rn02_concurrencia.py::test_doble_post_concurrente_un_ganador` queda **flaky** (el perdedor puede caer en RN05). `test_choque_profesional_409` y `test_choque_sillon_409` **no** se rompen: el precheck `_precheck_rn02` corre antes del insert.
- **Dependencias**: `C-01`, `C-21`
- **Governance**: MEDIO — invariante de paciente + código de error nuevo
- **Leer antes**: `KB-05 §RN05 + §Excepciones` · `KB-06 §US-001` (L14) · `KB-09 §SU-03` · `KB-10 §RN05`

### [C-29] `reservas-guest`
- **Estado**: `[ ]` pendiente
- **Scope**: `POST /reservas` público (sin API key) con datos mínimos + `profesional_id`, `prestacion_id`, `inicio` y `sillon_id` **opcional con auto-asignación al primero libre dentro de la transacción**. Mismas validaciones que US-001 (RN01–RN05). Devuelve **201 + `token_cancelacion`**; `POST /reservas/{token}/cancelacion` para que el guest cancele solo lo suyo (sin token no toca turnos ajenos). Rate-limit en memoria `10/min` (`RESERVA_RATE_LIMIT`), deuda documentada. Campo clínico → 422, nada persistido. Tests: e2e `disponibilidad → reserva → cancelación con token → slot liberado` + **2 `POST` concurrentes al mismo slot → 201 y 409**.
- **Dependencias**: `C-01`, `C-21`, `C-24`, `C-25`, `C-26`
- **Governance**: **ALTO** — endpoint público sin auth + datos personales + carrera real; es el riesgo R3 de Discovery. **Frenar y esperar revisión**
- **Leer antes**: `KB-06 §US-003 + §US-004` · `KB-07 §Flujo 1` · `KB-03 §Rutas públicas + §RBAC` · `KB-05 §RN05 + §Excepciones` · `KB-09 §DD-06 + §SU-03`

---

## FASE 4 — Interfaz (fuera del alcance de la entrega; todo BLOQUEADO por `C-30`)

### [C-31] `frontend-base-react-vite`
- **Estado**: `[ ]` pendiente — BLOQUEADO por `C-30`
- **Scope**: React + Vite + cliente HTTP tipado que consume el contrato `{code, message}`; manejo centralizado de errores por código de regla (`RN02_*`, `RN05`, `RN03_*`), nunca parsear texto; credencial según decida `C-30` (nunca la API key en el bundle).
- **Dependencias**: `C-29`, `C-23`, `C-27`, `C-30`
- **Governance**: **ALTO** — stack nuevo completo; contradice DD-01. **Frenar y esperar revisión**
- **Leer antes**: `KB-09 §DD-01` · `KB-01 §Fuera de alcance` · `KB-08 §Seguridad`

### [C-32] `ui-agenda-diaria`
- **Estado**: `[ ]` pendiente — BLOQUEADO por `C-30`
- **Scope**: pantalla de agenda del día sobre `GET /agenda` (orden por `inicio`, prestación + duración, sillón, paciente) y el filtro de cancelados; 403 visible si el odontólogo pide agenda ajena.
- **Dependencias**: `C-31` (también requiere `C-27`)
- **Governance**: MEDIO
- **Leer antes**: `KB-06 §US-006` · `KB-07 §Flujo 4` · `KB-03 §RBAC`

### [C-33] `ui-dar-turno-con-errores`
- **Estado**: `[ ]` pendiente — BLOQUEADO por `C-30`
- **Scope**: alta para recepcionista sobre catálogos + `GET /disponibilidad`; `POST /turnos` sin mandar `fin` (RN01 lo calcula el servidor); 409 con código por regla y 422 de validación diferenciados en la UI.
- **Dependencias**: `C-31` (también requiere `C-24`, `C-25`)
- **Governance**: MEDIO
- **Leer antes**: `KB-06 §US-001 + §US-002` · `KB-05 §RN01 + §RN02 + §Excepciones` · `KB-07 §Flujo 2`

### [C-34] `ui-reprogramar-cancelar-y-estados`
- **Estado**: `[ ]` pendiente — BLOQUEADO por `C-30`
- **Scope**: cancelación y reprogramación desde la UI mostrando el resultado de la transacción; si la reprogramación falla, dejar explícito que **el original sigue activo** (rollback total); estados `activo`/`cancelado` con `cancelled_at`.
- **Dependencias**: `C-31` (también requiere `C-22`, `C-23`)
- **Governance**: MEDIO
- **Leer antes**: `KB-06 §US-004 + §US-005` · `KB-07 §Flujo 3` · `KB-05 §RN04`

### [C-35] `ui-reserva-publica`
- **Estado**: `[ ]` pendiente — BLOQUEADO por `C-30`
- **Scope**: flujo público sin autenticación: catálogos → disponibilidad → `POST /reservas` → muestra y guarda el **token de cancelación** → cancelación con token. Solo contacto ficticio; la UI no pide ni muestra dato clínico (Ley 25.326).
- **Dependencias**: `C-31` (también requiere `C-25`, `C-29`)
- **Governance**: **ALTO** — superficie pública sin auth
- **Leer antes**: `KB-06 §US-003 + §US-004` · `KB-07 §Flujo 1` · `KB-03 §Rutas públicas` · `KB-09 §DD-06`

---

## Checklist de validación

- [x] Header "CHANGES — Secuencia de Implementación" y 5 pasos numerados + convenciones.
- [x] Convenciones de lectura del árbol declaradas (5 reglas).
- [x] El árbol separa ramas y no es una lista ordenada por capa.
- [x] Dependencias cruzadas anotadas como `(también requiere X)`.
- [x] Un GATE por cada fork de paralelismo (GATE 1 con 6 changes).
- [x] Camino crítico declarado: 2 cadenas de 6 nodos, el frontend no es cuello de botella.
- [x] Estados explícitos: solo `C-01` `[x]`; `C-31`…`C-35` BLOQUEADOS por decisión.
- [x] Cada change tiene los 5 campos: Estado, Scope, Dependencias, Governance, Leer antes.
- [x] Cada "Leer antes" tiene 3 a 5 archivos KB con sección.
- [x] Scope con bullets operacionales (modelos, endpoints, migraciones, tests).
- [x] Governance con los 4 niveles; los ALTO marcan "frenar y esperar revisión".
- [x] FASES con nombres semánticos alineadas a los GATES.
- [x] Trazabilidad KB → change + requisitos sin change declarados.
- [x] Mapeo de ids v1 → actual; los ids superseded no se reutilizan.
- [x] Déficit de `C-01` documentado y cubierto por changes separados, sin replanificar `POST /turnos`.
- [x] Conteos de US-001 verificados contra `KB-06` L11–L15 (5 criterios, 3 cubiertos).
- [x] Regresión de `C-21`+`C-26` sobre la suite existente anticipada, con los tests nombrados.
- [x] Deprecación de Python 3.16 asignada a `C-21`.
- [x] Versión anterior del roadmap conservada.

---

## Roadmap anterior (superseded)

> La v1 tenía 7 changes y camino crítico lineal. Se conserva porque el error y su corrección son parte del entregable. **No usar para implementar.**

Errores: (1) **`disponibilidad-real`, `agenda-odontologo` y `catalogos-publicos` como dependencias sucesivas de `reserva-guest`** — son paralelas; (2) **sin rama de persistencia**: la reserva y la cancelación dependían de migraciones que la 003 había dropeado, sin declararlo; (3) `C-07 frontend` sin la decisión DD-01 que lo habilita, así que parecía próximo; (4) declaraba a `C-01` como CU01+CU02 con RN01–RN05 "como núcleo", cuando el código real es solo `POST /turnos` con RN02/RN03 de soporte.

```
C-01 turnos-mvp                                  [x] entregado
 ├─ C-02 disponibilidad-real
 ├─ C-03 reserva-guest                           (también C-02)
 │   └─ C-04 cancelacion-y-reprogramacion
 ├─ C-05 agenda-odontologo
 └─ C-06 catalogos-publicos
Fase 3 — C-07 frontend-react-vite  (también C-03, C-04, C-05, C-06)
```

Gates v1: G0 `C-01` [cerrado] · G1 `C-02`‖`C-05`‖`C-06` · G2 `C-03` · G3 `C-04` · G4 `C-07`. **Camino crítico v1:** `C-01 → C-02 → C-03 → C-04`.

| v1 | Actual | Por qué cambió |
|---|---|---|
| `C-02 disponibilidad-real` | `C-25` | rama paralela, no paso previo |
| `C-03 reserva-guest` | `C-21`+`C-26`+`C-29` | partida en esquema, regla y endpoint |
| `C-04 cancelacion-y-reprogramacion` | `C-20`+`C-22`+`C-23` | esquema separado de API |
| `C-05 agenda-odontologo` | `C-27` | mismo alcance |
| `C-06 catalogos-publicos` | `C-24` | mismo alcance |
| `C-07 frontend-react-vite` | `C-30`+`C-31`…`C-35` | se le antepone la decisión de alcance |

Scopes de la v1, para trazabilidad: `C-02` disponibilidad como función pura + `GET /disponibilidad` + determinismo · `C-03` `POST /reservas` + rate-limit + token + índice RN05 + cancelación por token · `C-04` `cancelled_at` + `POST /turnos/{id}/cancelacion` + reprogramación transaccional · `C-05` `GET /agenda` + `API_KEY_ODONTOLOGO` + 403 + filtro · `C-06` tres catálogos · `C-07` interfaz web sobre las APIs cerradas.
# CHANGES — Secuencia de Implementación

> Índice canónico de todos los changes del proyecto **TurnosAR (turnos-odontologia)**.
> Cada change es atómico: un agente puede implementarlo en una sesión (~4-6 horas).
> **Leer este archivo antes de ejecutar cualquier `/opsx:propose`.**

> **Nota de alcance (cátedra):** este roadmap documenta el **árbol completo** de changes
> del proyecto, no solo lo entregado. `C-01 turnos-mvp` fue implementado y archivado
> (`openspec/changes/archive/2026-10-03-turnos-mvp/`) y es el change que se entrega.
> `C-20` a `C-35` quedan `[ ]`: existen para que el camino restante sea visible,
> trazable y priorizado según dependencias **reales**, no ordenadas por capa.

> **Revisión 2026-10 — corrección del árbol (observación de la cátedra).** La primera
> versión de este roadmap tenía 7 changes y un camino crítico lineal
> `C-01 → C-02 → C-03 → C-04`. **No representaba el árbol de conocimientos**: trataba
> `disponibilidad`, `catálogos` y `agenda` como dependencias sucesivas de la reserva
> guest (son paralelas), y **ocultaba la rama de persistencia**, que es una dependencia
> dura porque la migración 003 dropeó `token_cancelacion`, `cancelled_at` y el índice
> `rn05_un_activo_por_dia`. La versión nueva separa ramas, declara las dependencias
> cruzadas y agrega el hito `us-001-completa`. La versión anterior se conserva **íntegra**
> al final, en § "Roadmap anterior (superseded)".

---

## Cómo usar este documento

1. Identificá el change: buscá el próximo `[ ]` cuyas dependencias estén todas en `[x]` (usá el árbol y los GATES).
2. Leé la KB: abrí cada archivo de "Leer antes" del change, en especial las reglas RN-* y los escenarios US-* que cita el Scope.
3. Proponé: `/opsx:propose C-NN-nombre-del-change` (el slug en kebab-case es el que figura en el título del change).
4. Implementá y archivá: `/opsx:apply` con Strict TDD (todo escenario de la KB tiene un test automatizado de pytest) y luego `/opsx:archive`.
5. Marcá el checkbox: pasá Estado de `[ ]` a `[x]` en este archivo. Si el change tiene nivel **ALTO** o **CRITICO**, frená y esperá la revisión antes de escribir código.
6. Convenciones: intervalos semiabiertos `[inicio, fin)`; instantes en UTC (`timestamptz` en PostgreSQL y `datetime` con zona en Python); hora local `America/Argentina/Buenos_Aires`; `now` inyectado; solo datos ficticios; el dominio es la autoridad de las reglas y no importa FastAPI, SQLAlchemy ni Redis (DD-06, DD-07). Secretos solo en `.env`; en el repo, `.env.example` sin valores.

---

## Convenciones de lectura del árbol

Sin este contrato, el árbol es ambiguo. Estas 5 reglas son parte del documento.

| # | Convención | Cómo se lee |
|---|-----------|------------|
| 1 | **Sangría = dependencia dura** | el hijo no arranca hasta que el padre está `[x]` |
| 2 | **`(también requiere X)`** | dependencia obligatoria **fuera** de la línea del padre (cruza ramas) |
| 3 | **`A + B + C` debajo del `│`** | nodo de confluencia: requiere **todas** las ramas listadas, no solo una |
| 4 | **Hermanos al mismo nivel** | paralelizables: son el mismo GATE |
| 5 | **Prefijo del slug = capa** | `persistencia-` / `api-` / `disponibilidad-` / `ui-` / `decision-`. Es lo que convierte el árbol en **árbol de conocimientos** y no en lista de tareas |

> El **prefijo no es decorativo**: `persistencia-X` depende de esquema, `api-X` depende de contrato HTTP. Por eso nunca se planifica un `api-X` sin su `persistencia-X` cuando toca escribir.

---

## Árbol de dependencias

```
C-01 turnos-mvp                                       [x] ARCHIVADO (entregado)
 │    └── fundacion + dominio (rules.py RN01/RN03) + docker-compose PG16 + btree_gist
 │         + Alembic 001/002/003 + 6 modelos + POST /turnos + 26 tests
 │
 ├── PERSISTENCIA — el esquema va antes que la API ─────────────────────────
 │    ├── C-20 persistencia-cancelacion-rn04                  [ ]
 │    │      └── C-22 api-cancelacion-recepcionista           [ ]
 │    │              └── C-23 api-reprogramacion-atómica      [ ]
 │    └── C-21 persistencia-token-y-rn05                      [ ]
 │           └── C-26 rn05-limite-paciente                     [ ]
 │
 ├── API DE LECTURA — sin esquema nuevo, no dependen de la rama de persistencia
 │    ├── C-24 api-catalogos-publicos                        [ ]
 │    ├── C-25 disponibilidad-real                           [ ]
 │    └── C-27 api-agenda-odontologo                         [ ]
 │
 ├── TRANSVERSAL ─────────────────────────────────────────────────────────
 │    └── C-28 notificaciones-mock                           [ ]
 │
 ├── CONFLUENCIAS ────────────────────────────────────────────────────────
 │    C-21 + C-24 + C-25 + C-26
 │    └── C-29 reservas-guest                                [ ]
 │
 │    C-01 + C-26 + C-28
 │    └── ▸ HITO us-001-completa (4/4 criterios) — no es un change
 │
 │    C-01
 │    └── C-30 decision-frontend-alcance                     [ ]
 │
 └── C-29 + C-23 + C-27 + C-30
      └── C-31 frontend-base-react-vite                       [ ] BLOQUEADO
           ├── C-32 ui-agenda-diaria                          [ ] (también C-27)
           ├── C-33 ui-dar-turno-con-errores                  [ ] (también C-24, C-25)
           ├── C-34 ui-reprogramar-cancelar-y-estados         [ ] (también C-22, C-23)
           └── C-35 ui-reserva-publica                        [ ] (también C-24, C-25, C-29)
```

### Por qué estas dependencias y no otras

- **Esquema antes que API.** La mig. 003 dropeó `cancelled_at`, `token_cancelacion` y `rn05_un_activo_por_dia`. Sin `C-20` no existe `POST /turnos/{id}/cancelacion`; sin `C-21` la reserva guest no puede persistir el token ni garantizar RN05. De ahí `C-20 → C-22 → C-23` y `C-21 → C-26 → C-29`.
- **Contrato antes que consumidor.** `KB-07 §Flujo 1` es *descubrir profesional/prestación → ver slots → reservar*. Sin `C-24` y `C-25` la reserva se desarrolla contra datos inventados y el e2e de `KB-01 §Métricas` no se puede escribir. De ahí `C-24 + C-25 → C-29`.
- **Decisión antes que frontend.** `C-31…C-35` dependen de contratos que solo existen al final **y** de una decisión que la KB prohíbe explícitamente (DD-01). Por eso están BLOQUEADOS, no pendientes: no falta trabajo, falta una decisión de alcance.
- **Dos criterios de US-001 nunca se implementaron.** RN05 (409 1 activo/día) y la notificación mock son criterios de aceptación de US-001, y la mig. 003 + `tasks.md` los declararon fuera del change. Se cubren con `C-26` y `C-28` **sin replanificar `POST /turnos`**.

### Paralelismo por gate

> Cada GATE es un punto de sincronización. Los changes dentro de un grupo se pueden ejecutar en paralelo.

```
GATE 0: ninguna
  → C-01 turnos-mvp (solo — un integrante, sin paralelismo real)        [CERRADO]

GATE 1: C-01 cerrado
  → C-20 persistencia-cancelacion-rn04
  → C-21 persistencia-token-y-rn05
  → C-24 api-catalogos-publicos
  → C-25 disponibilidad-real
  → C-27 api-agenda-odontologo
  → C-28 notificaciones-mock
  → C-30 decision-frontend-alcance
    (7 en paralelo: 2 de esquema, 3 de lectura, 1 transversal, 1 decisión)

GATE 2: C-20 y C-21 cerrados
  → C-22 api-cancelacion-recepcionista
  → C-26 rn05-limite-paciente
    (2 en paralelo)

GATE 3: C-22 y C-26 cerrados
  → C-23 api-reprogramacion-atómica
  → C-29 reservas-guest
    (2 en paralelo — y con esto cierra el HITO us-001-completa)

GATE 4: C-23, C-27, C-29 y C-30 cerrados
  → C-31 frontend-base-react-vite   (bloqueado por la decisión C-30)

GATE 5: C-31 cerrado
  → C-32 ui-agenda-diaria
  → C-33 ui-dar-turno-con-errores
  → C-34 ui-reprogramar-cancelar-y-estados
  → C-35 ui-reserva-publica
    (4 en paralelo)
```

### Camino crítico (dos cadenas de igual longitud)

```
A) C-01 → C-21 → C-26 → C-29 → C-31 → C-35   (reserva pública)
B) C-01 → C-20 → C-22 → C-23 → C-31 → C-34   (ciclo de vida del turno)
```

> El frontend **no** es el cuello de botella: ambas cadenas son de 6 nodos y el trabajo
> real se reparte en GATE 1 (7 changes independientes). `C-30` es transversal y no está
> en ningún camino crítico.
>
> **Optimización disponible (no aplicada):** partir `C-31` en `base+shell` (solo necesita
> `C-30`) y `wiring de contrato` permitiría que `C-32`/`C-33`/`C-35` arranquen en GATE 3
> en vez de GATE 5.

### Plan con agentes

```
 Paso │ Agente A (API)          │ Agente B (Persistencia)  │ Agente C (Transversal/Docs)
 ─────┼─────────────────────────┼──────────────────────────┼────────────────────────────
   1  │ C-25 disponibilidad    │ C-20 cancelacion RN04    │ C-28 notificaciones-mock
      │ C-24 catalogos         │ C-21 token + RN05        │ C-30 decisión frontend
      │ C-27 agenda odontólogo │                          │
   2  │ C-26 rn05              │ C-22 api-cancelación     │ verifica GATE 2
   3  │ C-29 reservas-guest    │ C-23 api-reprogramación  │ trazabilidad final
   4  │ C-32…C-35 (UI)         │ —                        │ —
```

> Con un solo integrante no hay paralelismo explotable: la tabla se mantiene por
> contrato de formato. **Solo `C-01` se entrega**; `C-20` a `C-35` son para después.

---

## Trazabilidad: requisito de la KB → change

| Requisito KB | Change | Estado |
|---|---|---|
| RN01 `fin = inicio + duracion_min` en servidor | `C-01` | COMPLETADO |
| RN02 doble `EXCLUDE` + borde `[)` + carrera real | `C-01` | COMPLETADO |
| RN03 pasado / fuera de horario → 422 | `C-01` | COMPLETADO |
| **RN05** 1 activo por paciente/día → 409 | `C-21` + `C-26` | PENDIENTE |
| **RN04** cancelación libera el slot | `C-20` + `C-22` | PENDIENTE |
| US-001 (CU01) | `C-01` + `C-26` + `C-28` | COMPLETADO **3/4 CA** |
| US-002 (CU01) | `C-25` | PENDIENTE |
| US-003 (CU02) | `C-29` (+ `C-21`, `C-24`, `C-25`, `C-26`) | PENDIENTE |
| US-004 (CU03) | `C-22` + `C-29` (token) + `C-28` | PENDIENTE |
| US-005 (CU03) | `C-23` | PENDIENTE |
| US-006 (CU04) | `C-27` | PENDIENTE |
| KB-03 rutas públicas (5) | `C-24`, `C-25`, `C-29` | PENDIENTE (`/docs` ya existe) |
| KB-03 RBAC odontólogo (403) | `C-27` | PENDIENTE |
| KB-05 excepciones: notificación best-effort | `C-28` | PENDIENTE |
| KB-04 `idx_turno_paciente_fecha` | `C-20` | PENDIENTE |
| KB-08 layout (`notifications/`, `availability.py`, `reservas.py`, `agenda.py`) | `C-28`, `C-25`, `C-29`, `C-27` | PENDIENTE |
| DD-01 / KB-01 §Fuera de alcance (frontend) | `C-30` → `C-31`…`C-35` | **BLOQUEADO** |

**Requisitos sin change (declarado, no olvidado):**

- **Consentimiento Ley 25.326 Art. 5.1** (`KB-10`, prioridad Media): la KB propone "documentado, no persistido" → no amerita change propio.
- **Notificaciones reales** (WhatsApp Business API, email): excluidas por DD-05 (verificación empresarial + costo por mensaje) → backlog sin change.
- **Pagos, ficha clínica, multi-sucursal, obras sociales**: fuera de alcance por `KB-01 §Fuera de alcance` y DD-06 → sin change.
- **Bloqueos de agenda, agenda semanal, historial de transiciones**: **no existen en la KB**. Si la cátedra los quiere, se **agregan a la KB primero** y después entran al roadmap como change. Al revés es inventar alcance.
- **Ningún change está EN PROGRESO**: no hay código a medio escribir.

### Mapeo de ids: roadmap anterior → actual

| Id anterior (superseded) | Id actual | Motivo del reordenamiento |
|---|---|---|
| `C-01 turnos-mvp` | `C-01 turnos-mvp` | sin cambios (único `[x]`) |
| `C-02 disponibilidad-real` | `C-25` | pasa a ser rama paralela, no paso previo de la reserva |
| `C-03 reserva-guest` | `C-21` + `C-26` + `C-29` | se parte en esquema (token + RN05), regla (RN05) y endpoint |
| `C-04 cancelacion-y-reprogramacion` | `C-20` + `C-22` + `C-23` | se separa esquema de API, como el resto de la rama de persistencia |
| `C-05 agenda-odontologo` | `C-27` | mismo alcance, nuevo id (sin colisión) |
| `C-06 catalogos-publicos` | `C-24` | mismo alcance, nuevo id (sin colisión) |
| `C-07 frontend-react-vite` | `C-30` + `C-31`…`C-35` | se le antepone la decisión de alcance `C-30` y se descompone por pantalla |

> Los ids nuevos arrancan en `C-20` a propósito: `C-02`…`C-07` quedan reservados como
> históricos superseded y no se reutilizan, para que el historial de git no mezcle dos
> alcances distintos bajo el mismo id.

---

## FASE 1 — Base e invariante (entregado)

> Sin forks ni gates intermedios: todo el MVP entregado vive en un solo change demostrable.

### [C-01] `turnos-mvp`
- **Estado**: `[x]` archivado (`openspec/changes/archive/2026-10-03-turnos-mvp/`)
- **Scope**: MVP API puro FastAPI + PostgreSQL 16 con invariante RN02 en persistencia (solo CU01: alta evitando solapamientos; CU02/CU03/CU04 fuera del change)
  - `docker-compose.yml`: servicio `db` Postgres 16 con extensión `btree_gist` habilitada
  - `alembic/versions/`: Migración 001 tablas (`profesional`, `sillon`, `prestacion`, `paciente_guest`, `turno`, `horario_atencion`); Migración 002 doble `EXCLUDE USING gist` (`profesional_id WITH =`, `sillon_id WITH =`, `tstzrange(inicio, fin) WITH &&`) `WHERE (estado = 'activo')` + `CHECK (fin > inicio)`; Migración 003 recorte de alcance (dropea `rn05_un_activo_por_dia`, `token_cancelacion`, `cancelled_at`)
  - Modelos: `Profesional`, `Sillon`, `Prestacion`, `PacienteGuest` (solo contacto, sin DNI/clínico), `Turno` (`inicio`, `fin = inicio + duracion prestacion`, `estado activo`), `HorarioAtencion`
  - `app/domain/rules.py`: RN01 (cálculo `fin`) y RN03 (pasado vs `now()` en `America/Argentina/Buenos_Aires` + horario) como funciones puras testeables, solo como soporte del alta
  - `POST /turnos` (US-001, con API key recepcionista): crea turno, calcula `fin` por RN01; 409 `RN02_PROFESIONAL`/`RN02_SILLON`, 422 pasado/fuera de horario
  - `app/core/security.py`: auth mínima (API key recepcionista por env); middleware traduce `IntegrityError` por EXCLUDE → 409 con código de regla, nunca 500; Pydantic → 422; rechazo explícito de campos clínicos con 422
  - Seed mínimo: profesionales, sillones y prestaciones ficticias + horario de atención; `.env.example` con `DATABASE_URL`, `TZ_CONSULTORIO` (sin secretos reales)
  - Tests (26 en 5 archivos): `test_rn02_solapamiento.py` (borde que se toca `[)` no choca, doble eje profesional/sillón, cancelado libera), `test_rn02_concurrencia.py` (2 `POST` concurrentes al mismo slot → una 201 + otra 409, contra Postgres real), `test_turnos_api.py`, `test_rules.py`, `test_api_pure.py`
- **Dependencias**: ninguna
- **Governance**: MEDIO (lógica de negocio + invariante de concurrencia RN02; checkpoints por ser el núcleo evaluado)
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Turno (EXCLUDE x2, `btree_gist`, borde `[)`)
  - `knowledge-base/05_reglas_de_negocio.md` §RN02 (invariante central) + §Excepciones globales (409/422)
  - `knowledge-base/06_funcionalidades.md` §US-001 (criterios de aceptación del alta)
  - `knowledge-base/07_flujos_principales.md` §Flujo 2 (alta por recepcionista)
  - `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios + §Seguridad (auth mínima, env vars)

> **Déficit conocido de C-001** (documentado, no re-planificado como `POST /turnos`):
> US-001 tiene 4 criterios de aceptación y C-01 cumple 3. Faltan **RN05** (409 1 activo
> por paciente/día) y **notificación mock best-effort**. Los cubren `C-26` y `C-28`; el
> hito `us-001-completa` marca cuándo US-001 queda 4/4.

---

## FASE 2 — Cimientos del resto (GATE 1, sin dependencias entre sí)

> Lo que hoy falta en el esquema y en las lecturas. Siete changes independientes: se
> pueden hacer en cualquier orden.

### [C-20] `persistencia-cancelacion-rn04`
- **Estado**: `[ ]` pendiente
- **Scope**: devolver a `turno` la capacidad de registrar cancelación (RN04)
  - Alembic **004** nueva (nunca editar 001/002/003 aplicadas): `ALTER TABLE turno ADD COLUMN cancelled_at TIMESTAMPTZ`
  - Índice `idx_turno_paciente_fecha` (`paciente_id`, `inicio`) — el único índice de `KB-04 §Turno` que falta
  - `downgrade` reversible; `alembic current` = head y `alembic upgrade head` en verde
  - Test de migración: aplicar 004 sobre el esquema de 003 y verificar que `estado`, `fin` y los dos EXCLUDE siguen intactos
- **Dependencias**: `C-01 turnos-mvp`
- **Governance**: BAJO (una columna y un índice; no introduce invariante nueva)
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Turno (estados: la cancelación es cambio de estado, no borrado físico)
  - `knowledge-base/05_reglas_de_negocio.md` §RN04 (libera inmediatamente en ambas agendas)
  - `knowledge-base/07_flujos_principales.md` §Flujo 3 (paso 2: `UPDATE ... cancelled_at=now()`)
  - `knowledge-base/10_preguntas_abiertas.md` §IN-02 (nunca re-derivar el stack; toda migración nueva va en un change)

### [C-21] `persistencia-token-y-rn05`
- **Estado**: `[ ]` pendiente
- **Scope**: habilitar el esquema de la reserva pública: token opaco + invariante RN05 en la base
  - Alembic **005** nueva: `ALTER TABLE turno ADD COLUMN token_cancelacion TEXT UNIQUE` (el `downgrade` de la 003 ya tiene el DDL exacto, se copia de ahí)
  - Índice único parcial `rn05_un_activo_por_dia ON turno (paciente_id, ((inicio AT TIME ZONE 'America/Argentina/Buenos_Aires')::date)) WHERE estado = 'activo'`
  - **Cierra la pregunta de prioridad Alta de `KB-10`**: RN05 se implementa como invariante declarativa en la base (no solo validación en aplicación), siguiendo el mismo patrón que RN02
  - Test: dos inserts activos del mismo paciente y mismo día → el 2.º viola `rn05_un_activo_por_dia`; mismo paciente otro día → commit; `token_cancelacion` repetido → violación de unicidad
- **Dependencias**: `C-01 turnos-mvp`
- **Governance**: MEDIO (es una invariante en persistencia: la base decide, como RN02)
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Turno (`token_cancelacion`, RN05 como índice parcial funcional)
  - `knowledge-base/05_reglas_de_negocio.md` §RN05 (límite por paciente) + §Excepciones globales (409)
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-06 (guest sin auth) + §SU-03 (clave de identidad)
  - `knowledge-base/10_preguntas_abiertas.md` §RN05 (pregunta de prioridad Alta que este change resuelve)

### [C-24] `api-catalogos-publicos`
- **Estado**: `[ ]` pendiente
- **Scope**: lectura mínima de catálogos para que el flujo público pueda armar una reserva (`KB-03 §Rutas públicas`)
  - `GET /profesionales`, `GET /sillones`, `GET /prestaciones` — solo activos; en prestaciones, `duracion_min` visible (RN01)
  - **Públicos** (sin API key): son parte de las 5 rutas públicas de `KB-03`
  - `.env.example`: agregar `API_KEY_ODONTOLOGO` cuando exista el change que la usa (`C-27`)
  - Tests: 3 endpoints 200 con solo activos; sin credencial → 200; aparecen en `/openapi.json`
- **Dependencias**: `C-01 turnos-mvp`
- **Governance**: BAJO (tres endpoints de lectura sobre entidades ya persistidas)
- **Leer antes**:
  - `knowledge-base/02_descripcion_general.md` §API REST (resumen por recurso)
  - `knowledge-base/03_actores_y_roles.md` §Rutas públicas (qué es público y qué no)
  - `knowledge-base/04_modelo_de_datos.md` §Profesional, §Sillon, §Prestacion

### [C-25] `disponibilidad-real`
- **Estado**: `[ ]` pendiente
- **Scope**: convertir la agenda en algo elegible (US-002), requisito de `C-29`
  - `app/application/availability.py`: cómputo de slots como **función pura** de (HorarioAtencion − turnos activos, duración RN01, `now()` **inyectado**) — sin random, sin clock implícito
  - `GET /disponibilidad?profesional_id=&fecha=&prestacion_id=` (público, mismo endpoint para recepcionista y paciente)
  - El bloque completo `[inicio, fin)` tiene que entrar dentro del horario (RN03); descarta el pasado
  - Determinismo: dos consultas seguidas sin altas intermedias devuelven **exactamente** lo mismo
  - Tests (`tests/test_availability.py`): huecos correctos, bloque que no entra completo en el horario, borde `[)` no pisa turnos existentes, determinismo
- **Dependencias**: `C-01 turnos-mvp`
- **Governance**: BAJO (lógica de lectura pura, sin invariantes nuevas ni escrituras)
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-002 (criterios de aceptación)
  - `knowledge-base/07_flujos_principales.md` §Flujo 1 (paso 1: computa slots desde HorarioAtencion menos activos)
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: Temporalidad (RN03)
  - `knowledge-base/04_modelo_de_datos.md` §HorarioAtencion

### [C-27] `api-agenda-odontologo`
- **Estado**: `[ ]` pendiente
- **Scope**: lectura de la jornada del odontólogo (US-006 / CU04)
  - `app/api/v1/agenda.py`: `GET /agenda?profesional_id=&fecha=` con turnos activos ordenados por `inicio`, con prestación (y duración RN01 visible), sillón y paciente
  - Autorización mínima: `require_odontologo` en `app/core/security.py` con `API_KEY_ODONTOLOGO` (hoy solo existe `require_recepcion`); pedir agenda ajena → **403** (solo ve la propia)
  - `?incluir_cancelados=true` como filtro explícito; por defecto los cancelados no aparecen
  - Tests: orden por `inicio`, cancelados fuera por defecto, 403 de agenda ajena, fecha inválida → 422, sin credencial → 401
- **Dependencias**: `C-01 turnos-mvp`
- **Governance**: BAJO (endpoint de lectura; agrega el rol odontólogo pero sin reglas nuevas)
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-006
  - `knowledge-base/07_flujos_principales.md` §Flujo 4 (agenda del día del odontólogo)
  - `knowledge-base/03_actores_y_roles.md` §RBAC (odontólogo: solo lectura sobre su propia agenda)
  - `knowledge-base/08_arquitectura_propuesta.md` §Seguridad (auth mínima por rol)

### [C-28] `notificaciones-mock`
- **Estado**: `[ ]` pendiente
- **Scope**: la interfaz `NotificationService` que `KB-02`, `KB-08` y DD-05 ya exigen y que hoy **no existe**
  - `app/notifications/interface.py` (ABC) + `app/notifications/mock.py` (`MockNotificationService`: registra, no envía)
  - Cableado **best-effort post-commit** en todas las escrituras: si el mock lanza excepción, el turno **igual persiste** y la API responde 201 (`KB-05 §Excepciones globales`)
  - `NOTIF_BACKEND=mock` en `app/core/config.py` y en `.env.example`
  - Tests: el mock registra la llamada; con mock que falla, el turno queda persistido
- **Dependencias**: `C-01 turnos-mvp`
- **Governance**: BAJO (interfaz + mock en memoria, sin canal externo ni costo)
- **Leer antes**:
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-05 (interfaz con mock, sin WhatsApp Business API)
  - `knowledge-base/05_reglas_de_negocio.md` §Excepciones globales (la notificación no bloquea la agenda)
  - `knowledge-base/08_arquitectura_propuesta.md` §Patrones aplicados (interfaz de notificación + mock)
  - `knowledge-base/02_descripcion_general.md` §Integraciones externas

### [C-30] `decision-frontend-alcance`
- **Estado**: `[ ]` pendiente — **bloquea `C-31`…`C-35`**
- **Scope**: resolver por escrito si DD-01 ("API pura, sin frontend propio") se mantiene o se deroga
  - **No escribe código de UI**: es un change de decisión, con salida documental
  - Preguntas a responder: (a) ¿se deroga DD-01? (b) ¿cómo obtiene credencial el navegador sin exponer la API key (`KB-08 §Seguridad`)? (c) ¿qué costo/plazo se asume?
  - Salida: decisión escrita en `knowledge-base/09_decisiones_y_supuestos.md` (§DD-08) y `01_vision_y_objetivos.md` §Fuera de alcance, más el alcance de `.env.example`
  - Mientras no se apruebe, `C-31`…`C-35` quedan **BLOQUEADOS**
- **Dependencias**: `C-01 turnos-mvp`
- **Governance**: MEDIO (toca una decisión de alcance cerrada; contradice `KB-01 §Fuera de alcance`)
- **Leer antes**:
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-01 (API pura, sin frontend propio — y por qué)
  - `knowledge-base/01_vision_y_objetivos.md` §Fuera de alcance (frontend propio web o móvil)
  - `knowledge-base/08_arquitectura_propuesta.md` §Seguridad (por qué la API key no puede vivir en el cliente)
  - `docs/discovery/informe-discovery.md` §alcance del change (el frontend nunca fue parte del MVP)

---

## FASE 3 — Agenda operable (GATE 2 y GATE 3)

> Cierra el ciclo del consultorio: lo que hoy existe es solo el alta.

### [C-26] `rn05-limite-paciente`
- **Estado**: `[ ]` pendiente
- **Scope**: el 2.º de los 4 criterios de US-001 que C-01 no cubrió
  - Chequeo de 1 turno `activo` por paciente y día calendario (clave de identidad: teléfono normalizado, fallback email — SU-03)
  - Traducción de la violación de `rn05_un_activo_por_dia` a **409 `code="RN05"`** por nombre de constraint (nunca 500, nunca parseo de mensaje)
  - `PacienteIn` ya exige teléfono o email (`KB-04`: sin DNI, sin obra social, sin dato clínico)
  - Tests: mismo paciente mismo día → 409 `RN05`; paciente distinto → 201; mismo paciente otro día → 201; el `get_or_create_paciente` normaliza antes de comparar
- **Dependencias**: `C-01 turnos-mvp`, `C-21 persistencia-token-y-rn05` (el índice parcial)
- **Governance**: MEDIO (toca la invariante de paciente y agrega un código de error nuevo)
- **Leer antes**:
  - `knowledge-base/05_reglas_de_negocio.md` §RN05 (límite por paciente) + §Excepciones globales
  - `knowledge-base/06_funcionalidades.md` §US-001 (criterio "409 si el paciente ya tiene un activo ese día")
  - `knowledge-base/09_decisiones_y_supuestos.md` §SU-03 (clave de identidad del guest)
  - `knowledge-base/10_preguntas_abiertas.md` §RN05 (prioridad Alta, resuelta por `C-21`)

### [C-22] `api-cancelacion-recepcionista`
- **Estado**: `[ ]` pendiente
- **Scope**: liberar slots (RN04) para la recepcionista (US-004, parte R)
  - `POST /turnos/{id}/cancelacion` con API key de recepcionista → `estado='cancelado'` + `cancelled_at=now()`
  - El `WHERE (estado='activo')` de los EXCLUDE deja de contar el rango → el slot **reaparece** en `GET /disponibilidad` (por eso depende de `C-25` para poder probar el efecto)
  - **Idempotencia**: cancelar algo ya cancelado no duplica el efecto ni cambia `cancelled_at`
  - Notificación mock de cancelación (best-effort)
  - Tests: cancela y libera el slot (assert en `GET /disponibilidad`), idempotencia, sin credencial → 401, `id` inexistente → 404 `NO_ENCONTRADO`
- **Dependencias**: `C-01 turnos-mvp`, `C-20 persistencia-cancelacion-rn04`
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-004
  - `knowledge-base/07_flujos_principales.md` §Flujo 3 (pasos 1–4 de cancelación)
  - `knowledge-base/05_reglas_de_negocio.md` §RN04
  - `knowledge-base/04_modelo_de_datos.md` §Turno (estados: cambio de estado, no borrado físico)
- **Governance**: MEDIO (escritura que libera un slot + idempotencia)

### [C-23] `api-reprogramacion-atómica`
- **Estado**: `[ ]` pendiente
- **Scope**: mover turnos sin perderlos (US-005 / CU03)
  - `POST /turnos/{id}/reprogramacion`: **una sola transacción** — marca el original `cancelado` e inserta el nuevo
  - Si el destino viola RN02/RN03/RN05 → **rollback total** y el original sigue `activo`
  - Valida RN03 y RN05 sobre el slot nuevo
  - Tests: reprogramar a slot libre → 200; a slot tomado → 409 y el original **intacto** (assert en DB); al pasado → 422 sin tocar el original; violates RN05 → rollback
- **Dependencias**: `C-22 api-cancelacion-recepcionista` (reutiliza su lógica de cancelación), `C-20 persistencia-cancelacion-rn04`
- **Governance**: ALTO (atomicidad de la reprogramación y ventana de carrera entre cancelar e insertar) — **frenar y esperar revisión antes de escribir código**
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-005
  - `knowledge-base/07_flujos_principales.md` §Flujo 3 (pasos de reprogramación)
  - `knowledge-base/05_reglas_de_negocio.md` §RN04 (reprogramar = cancelar + crear en una transacción)
  - `knowledge-base/04_modelo_de_datos.md` §Turno

### [C-29] `reservas-guest`
- **Estado**: `[ ]` pendiente
- **Scope**: reserva pública sin autenticación del paciente (US-003 / CU02), con test de concurrencia real como criterio de aceptación
  - `app/api/v1/reservas.py`: `POST /reservas` público (sin API key), con datos mínimos + `profesional_id`, `prestacion_id`, `inicio` y `sillon_id` **opcional con auto-asignación al primero libre dentro de la transacción**
  - Devuelve **201 + `token_cancelacion`**; `POST /reservas/{token}/cancelacion` para que el guest cancele solo lo suyo (sin token no toca turnos ajenos)
  - Rate-limit en memoria `10/min` (`RESERVA_RATE_LIMIT`), deuda documentada
  - Rechazo explícito de campos clínicos con 422 (Ley 25.326: la reserva pública no persiste dato sensible)
  - Tests: `tests/test_reserva_guest.py` (e2e: `GET /disponibilidad` → reserva → cancelación con token → slot liberado) + 2 `POST /reservas` concurrentes al mismo slot → una 201 y otra 409 + rate-limit exceeded
- **Dependencias**: `C-01 turnos-mvp`, `C-21 persistencia-token-y-rn05`, `C-24 api-catalogos-publicos`, `C-25 disponibilidad-real`, `C-26 rn05-limite-paciente`
- **Governance**: ALTO (endpoint público sin auth + manejo de datos personales + carrera real bajo RN02/RN05; es el riesgo R3 de Discovery) — **frenar y esperar revisión antes de escribir código**
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-003
  - `knowledge-base/07_flujos_principales.md` §Flujo 1 completo (reserva guest sobre disponibilidad real)
  - `knowledge-base/03_actores_y_roles.md` §Rutas públicas + §RBAC (qué es público y qué no)
  - `knowledge-base/05_reglas_de_negocio.md` §Dominio: Paciente (RN05) + §Excepciones globales
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-06 + §SU-03 (clave de identidad del guest)

---

## FASE 4 — Interfaz (fuera del alcance de la entrega)

> Changes documentados para dejar el camino visible, **no forman parte de esta entrega**.
> Todos BLOQUEADOS hasta que `C-30` apruebe o derogue DD-01.

### [C-31] `frontend-base-react-vite`
- **Estado**: `[ ]` pendiente — **BLOQUEADO por `C-30`**
- **Scope**: base de la interfaz sobre la API cerrada
  - React + Vite + cliente HTTP tipado que consume el contrato `{code, message}` de la API
  - Manejo centralizado de errores por código de regla (`RN02_PROFESIONAL`, `RN02_SILLON`, `RN05`, `RN03_*`) — no parsear texto
  - Credencial según lo que decida `C-30` (nunca la API key en el bundle del navegador)
  - Build reproducible con `$0` (sin servicios pagos)
- **Dependencias**: `C-29 reservas-guest`, `C-23 api-reprogramacion-atómica`, `C-27 api-agenda-odontologo`, `C-30 decision-frontend-alcance`
- **Governance**: ALTO (stack nuevo completo; contradice DD-01) — **frenar y esperar revisión**
- **Leer antes**:
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-01 (API pura, sin frontend propio — y por qué)
  - `knowledge-base/01_vision_y_objetivos.md` §Fuera de alcance (frontend propio)
  - `knowledge-base/02_descripcion_general.md` §Arquitectura general
  - `knowledge-base/08_arquitectura_propuesta.md` §Seguridad

### [C-32] `ui-agenda-diaria`
- **Estado**: `[ ]` pendiente — **BLOQUEADO por `C-30`**
- **Scope**: pantalla de agenda del día para odontólogo y recepcionista
  - Consume `GET /agenda` (orden por `inicio`, prestación + duración, sillón, paciente)
  - Filtro `incluir_cancelados` expuesto de forma explícita
  - 403 visible si el odontólogo pide agenda ajena
- **Dependencias**: `C-31 frontend-base-react-vite` (también requiere `C-27 api-agenda-odontologo`)
- **Governance**: MEDIO (pantalla de lectura sobre un endpoint ya cerrado)
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-006
  - `knowledge-base/07_flujos_principales.md` §Flujo 4
  - `knowledge-base/03_actores_y_roles.md` §RBAC

### [C-33] `ui-dar-turno-con-errores`
- **Estado**: `[ ]` pendiente — **BLOQUEADO por `C-30`**
- **Scope**: pantalla de alta de turno para recepcionista, con los errores de negocio visibles
  - Consumo de catálogos + `GET /disponibilidad` para elegir profesional, sillón, prestación y hora
  - `POST /turnos`; el `fin` **nunca** se manda (RN01 lo calcula el servidor)
  - 409 con código por regla y 422 de validación diferenciados en la UI
- **Dependencias**: `C-31 frontend-base-react-vite` (también requiere `C-24 api-catalogos-publicos`, `C-25 disponibilidad-real`)
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-001 + §US-002
  - `knowledge-base/05_reglas_de_negocio.md` §RN01 + §RN02 + §Excepciones globales
  - `knowledge-base/07_flujos_principales.md` §Flujo 2

### [C-34] `ui-reprogramar-cancelar-y-estados`
- **Estado**: `[ ]` pendiente — **BLOQUEADO por `C-30`**
- **Scope**: cancelación y reprogramación desde la interfaz, mostrando el resultado de la transacción
  - `POST /turnos/{id}/cancelacion` y `POST /turnos/{id}/reprogramacion`
  - Si la reprogramación falla, la UI deja explícito que **el turno original sigue activo** (rollback total)
  - Estados `activo`/`cancelado` visibles con `cancelled_at`
- **Dependencias**: `C-31 frontend-base-react-vite` (también requiere `C-22 api-cancelacion-recepcionista`, `C-23 api-reprogramacion-atómica`)
- **Governance**: MEDIO
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-004 + §US-005
  - `knowledge-base/07_flujos_principales.md` §Flujo 3
  - `knowledge-base/05_reglas_de_negocio.md` §RN04

### [C-35] `ui-reserva-publica`
- **Estado**: `[ ]` pendiente — **BLOQUEADO por `C-30`**
- **Scope**: flujo público del paciente (enlace sin autenticación), el CU02 de punta a punta
  - Catálogos → `GET /disponibilidad` → `POST /reservas` → muestra y guarda el **token de cancelación**
  - `POST /reservas/{token}/cancelacion`: el paciente cancela solo lo suyo
  - Solo datos de contacto ficticios; la UI no pide ni muestra dato clínico (Ley 25.326)
- **Dependencias**: `C-31 frontend-base-react-vite` (también requiere `C-24 api-catalogos-publicos`, `C-25 disponibilidad-real`, `C-29 reservas-guest`)
- **Governance**: ALTO (superficie pública sin auth, expone el endpoint de mayor riesgo R3)
- **Leer antes**:
  - `knowledge-base/06_funcionalidades.md` §US-003 + §US-004
  - `knowledge-base/07_flujos_principales.md` §Flujo 1 completo
  - `knowledge-base/03_actores_y_roles.md` §Rutas públicas
  - `knowledge-base/09_decisiones_y_supuestos.md` §DD-06 (guest sin auth, sin ficha clínica)

---

## Checklist de validación al cerrar

- [x] El header dice "CHANGES — Secuencia de Implementación".
- [x] La sección "Cómo usar este documento" tiene los pasos numerados + convenciones.
- [x] **Conveciones de lectura del árbol declaradas** (5 reglas: sangría, `también requiere`, confluencia `A+B+C`, hermanos = paralelo, prefijo = capa).
- [x] El "Árbol de dependencias" separa ramas (PERSISTENCIA / API DE LECTURA / TRANSVERSAL / CONFLUENCIAS / FRONTEND) y no es una lista ordenada por capa.
- [x] Las dependencias cruzadas que no caben en la sangría están anotadas como `(también requiere X)`.
- [x] Hay un GATE por cada fork de paralelismo. (GATE 1 con 7 changes en paralelo.)
- [x] El camino crítico está declarado: 2 cadenas de 6 nodos, con el frontend fuera del cuello de botella.
- [x] Los estados reales son explícitos: solo `C-01` `[x]`; `C-20`…`C-35` `[ ]`, con `C-31`…`C-35` BLOQUEADOS por decisión.
- [x] Cada change tiene exactamente 5 campos: Estado, Scope, Dependencias, Governance, Leer antes.
- [x] Cada "Leer antes" tiene 3 a 5 archivos KB con sección cuando aplique.
- [x] El Scope tiene bullets operacionales (modelos, endpoints, migraciones, tests).
- [x] Cada Governance tiene uno de los 4 niveles: BAJO, MEDIO, ALTO, CRITICO. Los ALTO marcan "frenar y esperar revisión".
- [x] Los changes están agrupados en FASES con nombres semánticos, alineadas a los GATES.
- [x] Hay tabla de trazabilidad KB → change, y los requisitos **sin** change están declarados como tales.
- [x] Hay mapeo de ids del roadmap anterior al actual, y los ids superseded no se reutilizan.
- [x] El déficit conocido de `C-01` (RN05 y notificación) está documentado y cubierto por changes separados, sin replanificar `POST /turnos`.
- [x] La versión anterior del roadmap se conserva íntegra (sección siguiente).

---

## Roadmap anterior (superseded, sin commitear)

> Esta es la **primera versión** de este documento, escrita antes de la observación de la
> cátedra sobre el árbol. Se conserva a propósito: el error y su corrección son parte del
> entregable. **No usar para implementar**: su camino crítico y sus gates quedaron
> desmentidos por el árbol de arriba.
>
> **Errores concretos que corregir:**
> 1. Trató `disponibilidad-real`, `agenda-odontologo` y `catalogos-publicos` como
>    dependencias sucesivas de `reserva-guest`. No lo son: son lecturas paralelas.
> 2. No tenía rama de persistencia. La reserva guest y la cancelación dependían de
>    migraciones que **no existían** (003 dropeó `token_cancelacion`, `cancelled_at` y
>    `rn05_un_activo_por_dia`) y eso no estaba declarado como dependencia.
> 3. `C-07 frontend-react-vite` figuraba como "Fase 3" sin la decisión de alcance que
>    lo habilita (DD-01 lo prohíbe).
> 4. Declaraba a `C-01` como change que cubría CU01+CU02 con RN01–RN05 "como núcleo",
>    cuando el alcance real implementado es solo CU01 + RN02/RN03 de soporte.

### Árbol de dependencias (versión anterior)

```
C-01 turnos-mvp                                  [x] entregado
 ├─ C-02 disponibilidad-real
 ├─ C-03 reserva-guest                           (también C-02)
 │   └─ C-04 cancelacion-y-reprogramacion
 ├─ C-05 agenda-odontologo
 └─ C-06 catalogos-publicos

Fase 3 (fuera de la entrega) — C-07 frontend-react-vite  (también C-03, C-04, C-05, C-06)
```

### Paralelismo por fase (versión anterior)

```
GATE 0: ninguna
  → C-01 turnos-mvp (solo — un integrante, sin paralelismo real)   [CERRADO]

GATE 1: C-01 cerrado
  → C-02 disponibilidad-real  ‖  C-05 agenda-odontologo  ‖  C-06 catalogos-publicos

GATE 2: C-02 y C-01 cerrados
  → C-03 reserva-guest

GATE 3: C-03 y C-01 cerrados
  → C-04 cancelacion-y-reprogramacion

GATE 4: toda la API cerrada
  → C-07 frontend-react-vite   (fuera del alcance de esta entrega)
```

### Camino crítico (versión anterior)

```
C-01 → C-02 → C-03 → C-04
```

### FASE 2 — Agenda operable (versión anterior)

#### [C-02] `disponibilidad-real` — `[ ]` → ahora `C-25`
- **Scope**: `app/application/availability.py` como función pura; `GET /disponibilidad`; determinismo.
- **Dependencias**: `C-01`. **Governance**: BAJO.

#### [C-03] `reserva-guest` — `[ ]` → ahora `C-21` + `C-26` + `C-29`
- **Scope**: `POST /reservas` público, rate-limit `10/min`, migración con `token_cancelacion` + índice RN05, cancelación por token, rechazo de campos clínicos.
- **Dependencias**: `C-01`, `C-02`. **Governance**: ALTO.

#### [C-04] `cancelacion-y-reprogramacion` — `[ ]` → ahora `C-20` + `C-22` + `C-23`
- **Scope**: migración con `cancelled_at`; `POST /turnos/{id}/cancelacion`; idempotencia; `POST /turnos/{id}/reprogramacion` en una transacción.
- **Dependencias**: `C-01`, `C-03`. **Governance**: MEDIO.

#### [C-05] `agenda-odontologo` — `[ ]` → ahora `C-27`
- **Scope**: `GET /agenda`; `API_KEY_ODONTOLOGO`; 403 en agenda ajena; `?incluir_cancelados=true`.
- **Dependencias**: `C-01`. **Governance**: BAJO.

#### [C-06] `catalogos-publicos` — `[ ]` → ahora `C-24`
- **Scope**: `GET /profesionales`, `/sillones`, `/prestaciones`.
- **Dependencias**: `C-01`. **Governance**: BAJO.

### FASE 3 — Fuera de alcance (versión anterior)

#### [C-07] `frontend-react-vite` — `[ ]` → ahora `C-30` + `C-31`…`C-35`
- **Scope**: interfaz web sobre las APIs cerradas.
- **Dependencias**: `C-03`, `C-04`, `C-05`, `C-06`. **Governance**: ALTO.
- **Defecto**: declaraba que "contradecía DD-01" pero no la modelaba como dependencia,
  así que quedaba como trabajo que parecía próximo.
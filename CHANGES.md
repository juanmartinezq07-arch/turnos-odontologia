# CHANGES — Secuencia de Implementación

> Índice canónico de todos los changes del proyecto **TurnosAR (turnos-odontologia)**.
> Cada change es atómico: un agente puede implementarlo en una sesión (~4-6 horas).
> **Leer este archivo antes de ejecutar cualquier `/opsx:propose`.**

> **Nota de alcance (cátedra — Change OPSX 25% = 1 change):** este roadmap contiene
> **un único change** (`C-01 turnos-mvp`): alta de un turno evitando solapamientos
> por profesional y por sillón/box (CU01 + RN02, el ejemplo de la consigna), con
> RN01/RN03 solo como soporte necesario del flujo. CU02 (reserva guest), CU03
> (cancelación/reprogramación) y CU04 (agenda) son trabajo futuro, fuera del change.
> Decisión registrada en Discovery (`change_scope`).

---

## Cómo usar este documento

1. Identificar el change a implementar (verificar que sus dependencias están en `openspec/changes/archive/`).
2. Leer los docs de la knowledge-base indicados en "Leer antes".
3. Ejecutar `/opsx:propose turnos-mvp`.
4. Al terminar el change, archivarlo con `/opsx:archive turnos-mvp`.
5. Marcar el checkbox `[x]` en este archivo.

---

## Árbol de dependencias

```
C-01 turnos-mvp                         ← único change (sin dependencias)
```

### Paralelismo por fase

> Cada "gate" es un punto de sincronización. Los changes dentro de un grupo pueden ejecutarse en paralelo.

```
GATE 0: ninguna
  → C-01 turnos-mvp (solo — un integrante, sin paralelismo real)
```

### Camino crítico (1 change — mínimo irreducible)

```
C-01
```

### Plan óptimo con 3 agentes

```
Paso │ Agente A (API alta) │ Agente B (Tests RN02) │ Agente C (Docs Verify)
─────┼─────────────────────────┼────────────────────────┼─────────────────────────
  1  │ C-01 turnos-mvp         │ C-01 turnos-mvp         │ C-01 turnos-mvp
```

> Con un solo change y un solo integrante no hay paralelismo explotable.
> La tabla se mantiene por contrato de formato. Todo el proyecto es API/backend puro, sin frontend.

---

## FASE 0 — MVP Turnos (única fase)

> Sin forks ni gates intermedios: todo el MVP vive en un solo change demostrable.

### [C-01] `turnos-mvp`
- **Estado**: `[x]` archivado (`openspec/changes/archive/2026-10-03-turnos-mvp/`)
- **Scope**: MVP API puro FastAPI + PostgreSQL 16 con invariante RN02 en persistencia (solo CU01: alta evitando solapamientos; CU02/CU03/CU04 fuera del change)
  - `docker-compose.yml`: servicio `db` Postgres 16 con extensión `btree_gist` habilitada
  - `alembic/versions/`: Migración 001 tablas (`profesional`, `sillon`, `prestacion`, `paciente_guest`, `turno`, `horario_atencion`); Migración 002 doble `EXCLUDE USING gist` (`profesional_id WITH =`, `sillon_id WITH =`, `tstzrange(inicio, fin) WITH &&`) `WHERE (estado = 'activo')` + `CHECK (fin > inicio)`
  - Modelos: `Profesional`, `Sillon`, `Prestacion`, `PacienteGuest` (solo contacto, sin DNI/clínico), `Turno` (`inicio`, `fin = inicio + duracion prestacion`, `estado activo`), `HorarioAtencion`
  - `app/domain/rules.py`: RN01 (cálculo `fin`) y RN03 (pasado vs `now()` en `America/Argentina/Buenos_Aires` + horario) como funciones puras testeables, solo como soporte del alta
  - `POST /turnos` (US-001, con API key recepcionista): crea turno, calcula `fin` por RN01; 409 `RN02_PROFESIONAL`/`RN02_SILLON`, 422 pasado/fuera de horario
  - `app/core/security.py`: auth mínima (API key recepcionista por env); middleware traduce `IntegrityError` por EXCLUDE → 409 con código de regla, nunca 500; Pydantic → 422; rechazo explícito de campos clínicos con 422
  - Seed mínimo: profesionales, sillones y prestaciones ficticias + horario de atención; `.env.example` con `DATABASE_URL`, `TZ_CONSULTORIO` (sin secretos reales)
  - Tests: `test_rn02_solapamiento.py` (borde que se toca `[)` no choca, doble eje profesional/sillón), `test_rn02_concurrencia.py` (2 `POST` concurrentes al mismo slot → una 201 + otra 409, contra Postgres real)
- **Dependencias**: ninguna
- **Governance**: MEDIO (lógica de negocio + invariante de concurrencia RN02; checkpoints por ser el núcleo evaluado)
- **Leer antes**:
  - `knowledge-base/04_modelo_de_datos.md` §Turno (EXCLUDE x2, `btree_gist`, borde `[)`)
  - `knowledge-base/05_reglas_de_negocio.md` §RN02 (invariante central) + §Excepciones globales (409/422)
  - `knowledge-base/06_funcionalidades.md` §US-001 (criterios de aceptación del alta)
  - `knowledge-base/07_flujos_principales.md` §Flujo 2 (alta por recepcionista)
  - `knowledge-base/08_arquitectura_propuesta.md` §Estructura de directorios + §Seguridad (auth mínima, env vars)

---

## Checklist de validación al cerrar

- [x] El header dice "CHANGES — Secuencia de Implementación".
- [x] La sección "Cómo usar este documento" tiene los 5 pasos numerados.
- [x] El "Árbol de dependencias" usa ASCII art con `└──` y `│`. (N/A trivial: un solo nodo, sin ramas — formato conservado por contrato.)
- [x] Hay al menos un GATE por cada fork de paralelismo detectado. (GATE 0 único: sin forks en un roadmap de 1 change.)
- [x] El camino crítico tiene una flecha lineal sin ramas. (`C-01`.)
- [x] La tabla de "Plan óptimo con 3 agentes" tiene 3 columnas y los pasos enumerados.
- [x] Cada change tiene exactamente 5 campos: Estado, Scope, Dependencias, Governance, Leer antes.
- [x] Cada "Leer antes" tiene 3 a 5 archivos KB con sección cuando aplique. (5 archivos.)
- [x] El Scope tiene bullets operacionales (modelos, endpoints, migraciones, tests).
- [x] Cada Governance tiene uno de los 4 niveles: BAJO, MEDIO, ALTO, CRITICO. (MEDIO — ver justificación en el change.)
- [x] Los changes están agrupados en FASES con nombres semánticos (no "Fase 1, 2, 3" pelados). (FASE 0 — MVP Turnos.)

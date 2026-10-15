# TurnosAR — turnos-odontologia

MVP de API para alta de turnos en consultorios odontológicos (mercado
argentino). Trabajo de integración de Metodología I (TUP): del Discovery al
primer change con Spec-Driven Development (OpenSpec) y Active Stack.

El change C-01 implementa una sola funcionalidad: **crear un turno evitando
solapamientos por profesional y por sillón/box (CU01 + RN02)**. La invariante
central vive en PostgreSQL como doble `EXCLUDE USING gist` parcial, no solo
como validación en Python. RN01/RN03 se incluyen solo como soporte del flujo.
CU02 (reserva guest), CU03 (cancelación/reprogramación) y CU04 (agenda) son
trabajo futuro, fuera del change.

## Requisitos

- Python 3.12+
- Docker Compose (para la base `db`, Postgres 16)
- Git

## Instalación

```bash
git clone <url-del-repo>
cd turnos-odontologia/backend

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

pip install -e .
pip install uvicorn
```

## Configuración

```bash
cd backend
copy .env.example .env        # Windows
# cp .env.example .env        # Linux/macOS
```

`.env` ya trae valores locales de desarrollo (sin secretos reales).
Variables: `DATABASE_URL`, `POSTGRES_PASSWORD`, `TZ_CONSULTORIO`,
`API_KEY_RECEPCION`.

> Nunca commitear el `.env` real. Solo datos ficticios en seeds y tests
> (Ley 25.326: nada de datos reales de pacientes en el repo).

## Levantar la base y migrar

```bash
docker compose up -d db     # desde la raíz del repo
cd backend
python -m alembic upgrade head
```

> Con el venv activado, usar siempre `python -m ...`: los `.exe` del venv
> están rotos en esta máquina (salen con código 1 sin mensaje). El
> `backend/.env` se carga solo (nada que exportar salvo que quieras
> pisar valores); se usa `127.0.0.1` porque `localhost` resuelve lento
> a IPv6 en Windows.

Esto crea las tablas (migración 001), el doble `EXCLUDE` de RN02 más el
`CHECK (fin > inicio)` (migración 002, con `btree_gist`) y el recorte de
alcance (migración 003, nunca se edita una migración aplicada).

## Datos de ejemplo (ficticios)

```bash
cd backend
python -m app.seed
```

Carga profesionales, sillones, prestaciones (30/45/90 min) y horario
Lun–Vie 9–18 + Sáb 9–12. Todo sintético (`@example.com`).

## Correr la API

```bash
cd backend
python -m uvicorn app.main:app --reload
```

- Swagger: http://127.0.0.1:8000/docs
- OpenAPI: http://127.0.0.1:8000/openapi.json

Endpoint del change:

| Método | Ruta | Quién |
|--------|------|-------|
| POST | `/turnos` | recepcionista (header `X-API-Key` con `API_KEY_RECEPCION`) |

Respuestas: 201 alta (con `fin` calculado por el servidor), 409
`RN02_PROFESIONAL`/`RN02_SILLON`, 422 validación, 401 sin credencial.

## Correr los tests

Los tests de RN02 van **contra Postgres 16 real** (nunca SQLite ni mocks
de DB), así que la base tiene que estar levantada:

```bash
docker compose up -d db     # desde la raíz del repo
cd backend
python -m pytest -v
```

Archivos:

- `tests/test_rn02_solapamiento.py` — borde `[)` que se toca no choca,
  doble eje profesional/sillón, cancelado no bloquea (predicado parcial).
- `tests/test_rn02_concurrencia.py` — 2 POST concurrentes al mismo slot:
  uno da 201 y el otro 409.
- `tests/test_turnos_api.py` — alta e2e: RN01, 409 por eje, RN03, 422.
- `tests/test_rules.py` — RN01/RN03 puras, sin DB.
- `tests/test_api_pure.py` — docs, auth 401, schemas estrictos, mapper 409.

## Problemas comunes

- **Puerto 5432 ocupado** (`ports are not available`): otro Postgres local usa el
  puerto. Detené ese servicio o levantá un PG16 alternativo en otro puerto y
  apuntá `DATABASE_URL` ahí (ej. `localhost:5433`) solo para tu corrida local.
- **`localhost` lento en Windows**: si cada conexión tarda ~10 s, usá `127.0.0.1`
  en `DATABASE_URL` (resolución IPv6 lenta en algunas máquinas).
- **Tests que no conectan**: verificá `docker compose ps` (db en `healthy`) y que
  `alembic upgrade head` esté en `head` (`alembic current`).

## Estructura

```
backend/                # API FastAPI (todo comando Python desde acá)
backend/app/            # API (main.py solo cablea el router)
backend/app/core/       # config por env vars + seguridad (API key)
backend/app/domain/     # models.py + rules.py (RN01/RN03 puras)
backend/app/application/ # bookings.py (alta transaccional)
backend/app/api/v1/     # turnos.py (POST /turnos)
backend/app/schemas/    # TurnoCreate/TurnoOut estrictos (sin campo fin)
backend/alembic/versions/ # 001 tablas, 002 doble EXCLUDE, 003 recorte
backend/tests/          # suite pytest contra Postgres real
frontend/               # placeholder BLOQUEADO por C-30 (solo README)
docker-compose.yml      # raíz: orquesta db (+ futuro frontend)
docs/discovery/       # informe-discovery.md + .pdf + verificación de fuentes
knowledge-base/       # los 10 archivos canónicos del dominio
openspec/             # specs vigentes (turnos, plataforma-mvp) + change archivado
.agents/skills/         # skills versionadas en el repo (ver AGENTS.md)
```

## Documentos del trabajo

- `docs/discovery/informe-discovery.md` (y `.pdf`): investigación de mercado.
- `CHANGES.md`: roadmap (un único change C-01, archivado).
- `docs/reflexion.md`: reflexión escrita del trabajo.
- `AGENTS.md` / `CLAUDE.md`: reglas del agente.

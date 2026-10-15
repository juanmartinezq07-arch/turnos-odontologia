# Backend — TurnosAR (FastAPI + PostgreSQL 16)

API de turnos odontológicos. Todos los comandos se corren **desde esta carpeta**
(`cd backend`).

## Requisitos

- Python 3.12+
- Docker Compose (la base `db` se levanta desde la **raíz** del repo: `docker compose up -d db`)
- Git

## Instalación

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
# source .venv/bin/activate

pip install -e .
pip install uvicorn
copy .env.example .env        # Windows
# cp .env.example .env        # Linux/macOS
```

`.env` ya trae valores locales de desarrollo (sin secretos reales).
Variables: `DATABASE_URL`, `POSTGRES_PASSWORD`, `TZ_CONSULTORIO`, `API_KEY_RECEPCION`.
Nunca commitear el `.env` real. Solo datos ficticios (Ley 25.326).

## Migrar y cargar datos ficticios

```bash
python -m alembic upgrade head
python -m app.seed
```

> Usar siempre `python -m ...` (con el venv activado): los `.exe` del venv
> están rotos en esta máquina (salen con código 1 sin mensaje) y `alembic`
> a secas tampoco existe como módulo ejecutable — `alembic/__main__.py`
> lo habilita. `backend/.env` se carga solo (`config.py`, `alembic/env.py`
> y `tests/conftest.py` hacen `load_dotenv`); lo exportado en la shell
> siempre gana. Se usa `127.0.0.1` porque `localhost` resuelve lento a
> IPv6 en Windows. El password (`turnos-dev`) debe coincidir con
> `POSTGRES_PASSWORD` del `.env` de la raíz (lo lee el compose).

## Correr la API

```bash
python -m uvicorn app.main:app --reload
```

- Swagger: http://127.0.0.1:8000/docs
- OpenAPI: http://127.0.0.1:8000/openapi.json

| Método | Ruta | Quién |
|--------|------|-------|
| POST | `/turnos` | recepcionista (header `X-API-Key` con `API_KEY_RECEPCION`) |

## Tests (contra Postgres 16 real, nunca SQLite)

```bash
docker compose up -d db     # desde la raíz del repo
python -m pytest -v         # desde backend/
```

## Estructura

```
app/                  # API (main.py solo cablea el router)
app/core/             # config por env vars + seguridad (API key)
app/domain/           # models.py + rules.py (RN01/RN03 puras)
app/application/      # bookings.py (alta transaccional)
app/api/v1/           # turnos.py (POST /turnos)
app/schemas/          # TurnoCreate/TurnoOut estrictos (sin campo fin)
alembic/versions/     # 001 tablas, 002 doble EXCLUDE, 003 recorte
tests/                # suite pytest contra Postgres real
```

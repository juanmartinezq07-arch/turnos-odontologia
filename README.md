# TurnosAR — turnos-odontologia

MVP de API para gestión de turnos y agenda de pacientes en consultorios
odontológicos (mercado argentino). Trabajo de integración de Metodología I
(TUP): del Discovery al primer change con Spec-Driven Development (OpenSpec)
y Active Stack.

La invariante central es **RN02**: un turno no puede solaparse con otro del
mismo profesional ni del mismo sillón/box. Vive en PostgreSQL como doble
`EXCLUDE USING gist` parcial, no solo como validación en Python.

## Requisitos

- Python 3.12+
- Docker Compose (para la base `db`, Postgres 16)
- Git

## Instalación

```bash
git clone <url-del-repo>
cd turnos-odontologia

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
copy .env.example .env        # Windows
# cp .env.example .env        # Linux/macOS
```

`.env` ya trae valores locales de desarrollo (sin secretos reales).
Variables: `DATABASE_URL`, `POSTGRES_PASSWORD`, `TZ_CONSULTORIO`,
`NOTIF_BACKEND=mock`, `API_KEY_RECEPCION`, `API_KEY_ODONTOLOGO`,
`RESERVA_RATE_LIMIT`.

> Nunca commitear el `.env` real. Solo datos ficticios en seeds y tests
> (Ley 25.326: nada de datos reales de pacientes en el repo).

## Levantar la base y migrar

```bash
docker compose up -d db
alembic upgrade head
```

Esto crea las tablas (migración 001) y el doble `EXCLUDE` de RN02 más el
`CHECK (fin > inicio)` (migración 002, con `btree_gist`).

## Datos de ejemplo (ficticios)

```bash
python -m app.seed
```

Carga 2 profesionales, 2 sillones, 3 prestaciones (30/45/90 min), horario
Lun–Vie 9–18 + Sáb 9–12 y turnos de ejemplo. Todo sintético (`@example.com`).

## Correr la API

```bash
uvicorn app.main:app --reload
```

- Swagger: http://127.0.0.1:8000/docs
- OpenAPI: http://127.0.0.1:8000/openapi.json

Endpoints principales:

| Método | Ruta | Quién |
|--------|------|-------|
| POST | `/turnos` | recepcionista (API key) |
| GET | `/disponibilidad?profesional_id=&fecha=&prestacion_id=` | público |
| POST | `/reservas` | público (guest, rate-limit 10/min) |
| POST | `/reservas/{token}/cancelacion` | guest (dueño del token) |
| DELETE/PATCH | `/turnos/{id}` | recepcionista |
| GET | `/agenda?profesional_id=&fecha=` | odontólogo (solo su agenda) |
| GET | `/profesionales`, `/sillones`, `/prestaciones` | público |

Auth por header `X-API-Key` con los valores de `API_KEY_RECEPCION` /
`API_KEY_ODONTOLOGO`.

## Correr los tests

Los tests de RN02 van **contra Postgres 16 real** (nunca SQLite ni mocks
de DB), así que la base tiene que estar levantada:

```bash
docker compose up -d db
pytest
```

Archivos obligatorios:

- `tests/test_rn02_solapamiento.py` — borde `[)` que se toca no choca,
  doble eje profesional/sillón, cancelado libera el slot.
- `tests/test_rn02_concurrencia.py` — 2 POST concurrentes al mismo slot:
  una da 201 y la otra 409.
- `tests/test_reserva_guest.py` — reserva guest e2e, cancelación con
  token y RN05 (un activo por paciente/día).

Extras: `test_rules.py` (RN01/RN03 puras), `test_turnos_api.py`,
`test_disponibilidad_agenda.py`, `test_api_pure.py`.

## Estructura

```
app/                  # API (main.py solo cablea routers)
app/core/             # config por env vars + seguridad (API keys)
app/domain/           # models.py + rules.py (RN01/RN03/RN04/RN05 puras)
app/application/      # bookings.py + availability.py (casos de uso)
app/api/v1/           # routers finos (turnos, reservas, disponibilidad, agenda, catalogos)
app/notifications/    # interfaz + mock best-effort (no bloquea persistencia)
alembic/versions/     # 001 tablas, 002 doble EXCLUDE
tests/                # suite pytest contra Postgres real
docs/discovery/       # informe-discovery.md + .pdf + verificación de fuentes
knowledge-base/       # los 10 archivos canónicos del dominio
openspec/             # specs vigentes + changes/archive/2026-10-03-turnos-mvp/
```

## Documentos del trabajo

- `docs/discovery/informe-discovery.md` (y `.pdf`): investigación de mercado.
- `CHANGES.md`: roadmap (un único change C-01, archivado).
- `docs/reflexion.md`: reflexión escrita del trabajo.
- `AGENTS.md` / `CLAUDE.md`: reglas del agente.

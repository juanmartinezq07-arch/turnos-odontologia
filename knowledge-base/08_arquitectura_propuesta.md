# Arquitectura Propuesta

Prioriza **mantenibilidad con foco en velocidad de entrega** (P5 = b): código chico, explícito y testeable, sin sobrediseño. Un solo integrante, una semana, $0.

## Patrones aplicados

| Patrón | Dónde se usa | Por qué |
|--------|--------------|---------|
| Monolito modular (API pura) | Toda la app | Un deploy, cero orquestación; alcanza para 2–10 profesionales |
| Capas finas (routers → servicios → repositorios) | FastAPI | Los routers no tocan la DB; los servicios concentran RN01/RN03/RN04/RN05; RN02 vive en la DB |
| Invariante en persistencia (EXCLUDE) | Migración Alembic + modelo SQLAlchemy | Cierra la ventana de carrera que la validación de aplicación no puede cerrar (R1) |
| Interfaz de notificación + mock | `NotificationService` / `MockNotificationService` | Desacopla el dominio del canal; permite demo sin WhatsApp Business API ni costo |
| Guest booking con token opaco | `POST /reservas` + `token_cancelacion` | Reserva sin auth sin introducir tabla de usuarios paciente ni RBAC complejo |
| Soft-delete por estado | `turno.estado` | La cancelación libera el slot sin borrar historia (RN04) |
| Manejo de errores por código de regla | Middleware de excepciones | `IntegrityError` por EXCLUDE → 409 con `RN02_*`; validación Pydantic → 422 |

## Estructura de directorios

```
turnos-odontologia/
├── docker-compose.yml          # servicio db (Postgres 16 + btree_gist)
├── alembic/                    # migraciones (la de EXCLUDE es la crítica)
│   └── versions/
├── app/
│   ├── main.py                 # factory FastAPI, routers, exception handlers
│   ├── core/
│   │   ├── config.py           # settings via env vars
│   │   └── security.py         # auth mínima por rol (API key / usuario fijo)
│   ├── domain/
│   │   ├── models.py           # SQLAlchemy 2.0: Profesional, Sillon, Prestacion, PacienteGuest, Turno, HorarioAtencion
│   │   └── rules.py            # RN01/RN03/RN04/RN05 como funciones puras testeables
│   ├── application/
│   │   ├── availability.py     # cómputo de slots (US-002)
│   │   └── bookings.py         # agendar / reservar / cancelar / reprogramar
│   ├── notifications/
│   │   ├── interface.py        # NotificationService (abc)
│   │   └── mock.py             # MockNotificationService (registra, no envía)
│   ├── api/
│   │   └── v1/
│   │       ├── disponibilidad.py
│   │       ├── turnos.py
│   │       ├── reservas.py
│   │       └── agenda.py
│   └── schemas/                # Pydantic v2 request/response
├── tests/
│   ├── test_rn02_solapamiento.py   # secuencial: borde que se toca, doble eje
│   ├── test_rn02_concurrencia.py   # real: 2 hilos/procesos al mismo slot
│   └── test_reserva_guest.py       # end-to-end guest + cancelación
├── knowledge-base/             # esta KB
├── discovery/discovery.md      # artefacto Discovery (fuente)
└── openspec/                   # specs y changes (un solo change)
```

## Seguridad

- Autenticación: mínima por rol para personal del consultorio (API key o usuario fijo por entorno local). Paciente guest sin auth, acotado a sus dos endpoints + cancelación con token.
- Autorización: matriz de 03_actores_y_roles; el odontólogo solo lee su agenda; el guest solo toca su reserva con token.
- Validación de input: Pydantic v2 en borde (tipos, fechas futuras, ids existentes); reglas de dominio en servicios; invariante en DB. Rechazo explícito de campos clínicos (422).
- Secrets management: todo por env vars; nada hardcodeado. Credenciales de demo solo en `.env` local no commiteado (proveer `.env.example`).
- Abuso del endpoint público: rate-limit básico en `POST /reservas` (a definir en el change: ventana simple en memoria es suficiente para el MVP) + token opaco para cancelar.

## Variables de entorno

| Variable | Descripción | Ejemplo | Sensible |
|----------|-------------|---------|----------|
| `DATABASE_URL` | DSN Postgres | `postgresql+psycopg://turnos:turnos@localhost:5432/turnos` | Sí |
| `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` | Credenciales Compose local | `turnos` / `turnos` / `turnos-dev` | Sí |
| `TZ_CONSULTORIO` | Zona horaria para RN03 | `America/Argentina/Buenos_Aires` | No |
| `API_KEY_RECEPCION` | Credencial demo recepcionista | `dev-recepcion-123` | Sí |
| `API_KEY_ODONTOLOGO` | Credencial demo odontólogo | `dev-odonto-123` | Sí |
| `NOTIF_BACKEND` | Backend de notificaciones | `mock` | No |
| `RESERVA_RATE_LIMIT` | Ventana del rate-limit público | `10/minute` | No |

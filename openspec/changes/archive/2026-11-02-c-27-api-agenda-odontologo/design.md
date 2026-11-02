# Design

## Context

Ver `proposal.md` para la motivación. El sistema ya cuenta con las entidades `Turno`, `Profesional`, `Sillon`, `Prestacion` y `PacienteGuest` en `backend/app/domain/models.py`, y con `get_api_key_odontologo()` / `require_odontologo` preliminar en `backend/app/core/config.py` y `backend/app/core/security.py`. Falta la autorización por identidad de profesional para el rol odontólogo (`403` ante agenda ajena según `KB-03 §RBAC` y `KB-07 §Flujo 4`), el caso de uso de lectura de agenda diaria y el router `GET /agenda`.

Decision: no (no UI)

## Goals / Non-Goals

**Goals:**
- Exponer `GET /agenda?profesional_id=&fecha=&incluir_cancelados=false` autenticado.
- Garantizar RBAC mínimo: sin credencial válida → `401`; con `API_KEY_ODONTOLOGO` pidiendo un `profesional_id` distinto de su `X-Profesional-Id` (o sin indicar `X-Profesional-Id`) → `403` (`code="AGENDA_AJENA"`); con `API_KEY_RECEPCION` → lectura global permitida (`KB-03`).
- Devolver cada turno con prestación (`id`, `nombre`, `duracion_min`), sillón (`id`, `nombre`) y paciente (`id`, `nombre`, `telefono`, `email`), ordenado por `inicio` ascendente.

**Non-Goals:**
- No se implementa agenda semanal ni bloqueos de agenda (fuera de la KB).
- No se implementa OAuth/JWT ni tabla de usuarios (deuda deliberada DD-07 / `KB-03`).
- No se modifica el modelo de datos ni se agregan migraciones Alembic.

## Decisions

### D-01 — Autorización RBAC de agenda con `X-API-Key` + `X-Profesional-Id`
- **Decisión**: En `backend/app/core/security.py`, `require_odontologo` (o dependencia de autorización de agenda) valida `X-API-Key`:
  1. Si `X-API-Key` coincide con `API_KEY_ODONTOLOGO`: verifica el header `X-Profesional-Id` (UUID) contra el query param `profesional_id`. Si falta `X-Profesional-Id`, no es un UUID válido o es distinto de `profesional_id`, lanza `HTTPException(status_code=403, detail={"code": "AGENDA_AJENA", "message": "El odontologo solo puede consultar su propia agenda"})`.
  2. Si `X-API-Key` coincide con `API_KEY_RECEPCION`: autoriza la lectura global de cualquier `profesional_id` conforme a la matriz RBAC de `KB-03`.
  3. En cualquier otro caso (sin `X-API-Key` o clave inválida): lanza `HTTPException(status_code=401, detail="API key invalida")`.
- **Alternativas consideradas**: Crear una API key distinta por cada fila de `Profesional` en la base de datos. Descartado porque `KB-08 §Variables de entorno` define una única variable `API_KEY_ODONTOLOGO` en `.env` y pide mantener auth mínima sin tabla de usuarios ni credenciales en DB.

### D-02 — Consulta con JOIN en `backend/app/application/agenda.py` acotada al día local
- **Decisión**: `consultar_agenda_dia(session, profesional_id, fecha, incluir_cancelados=False)` construye el rango `[inicio_dia, fin_dia)` del día `fecha` en `ZoneInfo(get_tz_consultorio())` (`America/Argentina/Buenos_Aires`), hace `select(Turno, Prestacion, Sillon, PacienteGuest)` con `join` explícitos filtrando por `Turno.profesional_id == profesional_id`, `Turno.inicio >= inicio_dia`, `Turno.inicio < fin_dia`, y si `not incluir_cancelados` filtra `Turno.estado == "activo"`, ordenando por `Turno.inicio.asc()`.
- **Alternativas consideradas**: Lazy loading de relaciones ORM. Descartado porque en SQLAlchemy 2.0 async el lazy loading implícito lanza `MissingGreenlet`; un `select` con `join` trae todo en una sola query determinista.

### D-03 — Schemas de salida estrictos con `extra="forbid"`
- **Decisión**: Definir `AgendaPrestacionOut`, `AgendaSillonOut`, `AgendaPacienteOut` y `AgendaTurnoOut` en `backend/app/schemas/agenda.py` todos con `ConfigDict(extra="forbid")`, exponiendo `duracion_min` en la prestación (RN01) y solo contacto mínimo en el paciente (Ley 25.326).

## Risks / Trade-offs

- [Risk] Turnos cerca de la medianoche evaluados en UTC vs hora local → Mitigación: El rango `[00:00, 24:00)` del día `fecha` se construye con `ZoneInfo(get_tz_consultorio())` (`America/Argentina/Buenos_Aires`) antes de consultar `timestamptz` en PostgreSQL.
- [Risk] `HTTPException(status_code=403)` con `detail` dict vs string en el handler global → Mitigación: Soportar o usar `DomainError` / ajustar el handler de `HTTPException` en `main.py` para que cuando `exc.detail` sea un `dict` con `code` y `message` lo preserve tal cual (y si es `str` use `ERROR_HTTP`).

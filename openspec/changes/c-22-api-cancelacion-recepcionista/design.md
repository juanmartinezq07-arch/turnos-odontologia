# Design

## Context

El modelo `Turno` en `backend/app/domain/models.py` ya cuenta con la columna `cancelled_at: Mapped[datetime | None]` incorporada en la migración Alembic `004` (`C-20`), y los constraints de exclusión `rn02_profesional`, `rn02_sillon` e índice único `rn05_un_activo_por_dia` filtran por `WHERE (estado = 'activo')`. Asimismo, `C-28` introdujo `get_notification_service().notify_turn_updated(turn_id)` con semántica *best-effort*. Ver `proposal.md` para la motivación de negocio.

## Goals / Non-Goals

**Goals:**
- Exponer `POST /turnos/{turno_id}/cancelacion` en `backend/app/api/v1/turnos.py` protegido por `require_recepcion`.
- Implementar `cancelar_turno(session: AsyncSession, turno_id: uuid.UUID) -> Turno` en `backend/app/application/bookings.py`.
- Garantizar idempotencia estricta sobre `cancelled_at` y liberación inmediata del slot para nuevas reservas y consultas de disponibilidad.
- Incluir `cancelled_at: datetime | None = None` en `TurnoOut` (`backend/app/schemas/turno.py`).

**Non-Goals:**
- Cancelación pública por token de paciente guest (`POST /reservas/{token}/cancelacion`), que corresponde a `C-29`.
- Reprogramación transaccional (`POST /turnos/{id}/reprogramacion`), que corresponde a `C-23`.
- Cambios de esquema o nuevas migraciones Alembic (la columna `cancelled_at` ya existe desde `C-20`).

## Decisions

### D-01: Idempotencia mediante chequeo previo de `turno.estado == "cancelado"`
- **Decisión**: En `cancelar_turno(session, turno_id)`, recuperar la entidad con `await session.get(Turno, turno_id)`. Si es `None`, lanzar `NotFound("NO_ENCONTRADO", "Turno inexistente")`. Si `turno.estado == "cancelado"`, retornar `turno` inmediatamente sin ejecutar `UPDATE`, sin modificar `turno.cancelled_at` y sin duplicar eventos de notificación.
- **Justificación (verificada con MCP `Context7` — SQLAlchemy 2.0 `AsyncSession`)**: Al usar `async_sessionmaker(..., expire_on_commit=False)`, los atributos de `Turno` permanecen accesibles en memoria tras el `commit()` sin disparar IO implícito. Evitar un segundo `UPDATE` preserva el timestamp de auditoría original (`T1`) exigido por `CHANGES.md` §C-22.
- **Alternativas consideradas**: Ejecutar `UPDATE ... SET cancelled_at = COALESCE(cancelled_at, now())` siempre; descartado porque ensucia la sesión y dispararía notificaciones duplicadas en reintentos de red de la recepcionista.

### D-02: Notificación *best-effort* post-commit (`notify_turn_updated`)
- **Decisión**: Invocar `get_notification_service().notify_turn_updated(turno.id)` dentro de un bloque `try / except Exception` **después** de `await session.commit()` únicamente cuando el turno transiciona de `activo` a `cancelado`.
- **Justificación**: Cumple con `KB-05 §Excepciones` y `C-28`: si el backend de notificaciones lanza una excepción, se registra un warning en el log pero la cancelación y la liberación del slot ya quedaron confirmadas en PostgreSQL.

## Risks / Trade-offs

- **[Riesgo]** Expiración de atributos en `AsyncSession` tras `await session.commit()` al serializar `TurnoOut` → **Mitigación**: La fábrica de sesiones en `app/db.py` y `tests/conftest.py` utiliza `expire_on_commit=False` (patrón oficial de SQLAlchemy 2.0 validado vía MCP `Context7`).
- **[Trade-off]** `POST /turnos/{id}/cancelacion` no recibe body JSON → **Mitigación**: No se requiere payload de entrada, eliminando el riesgo de inyección de campos clínicos (Ley 25.326).

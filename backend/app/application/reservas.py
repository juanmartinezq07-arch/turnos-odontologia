"""Lógica de aplicación para reservas públicas guest (C-29)."""
from datetime import datetime, timedelta
import logging
import secrets
import uuid
from zoneinfo import ZoneInfo

from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.application import bookings
from app.core.config import get_tz_consultorio
from app.core.errors import DomainConflict, NotFound, conflict_code_from_integrity_error
from app.domain import rules
from app.domain.models import Sillon, Turno
from app.notifications import get_notification_service


def _ahora() -> datetime:
    return datetime.now(ZoneInfo(get_tz_consultorio()))


async def autoasignar_sillon(
    session: AsyncSession, inicio: datetime, fin: datetime
) -> uuid.UUID:
    """Busca el primer sillón activo disponible en [inicio, fin)."""
    # 1. Obtener todos los sillones activos ordenados
    res = await session.execute(
        select(Sillon.id).where(Sillon.activo.is_(True)).order_by(Sillon.nombre)
    )
    sillones_ids = [row[0] for row in res.all()]
    if not sillones_ids:
        raise DomainConflict("RN02_SILLON", "No hay sillones disponibles en el consultorio", status=409)

    # 2. Obtener sillones que ya tienen turnos activos en conflicto
    solapa = and_(
        Turno.estado == "activo",
        Turno.inicio < fin,
        Turno.fin > inicio,
        Turno.sillon_id.in_(sillones_ids),
    )
    res_ocupados = await session.execute(select(Turno.sillon_id).where(solapa))
    ocupados = set(row[0] for row in res_ocupados.all())

    for sid in sillones_ids:
        if sid not in ocupados:
            return sid

    raise DomainConflict("RN02_SILLON", "No hay ningún sillón disponible en ese horario", status=409)


async def crear_reserva_guest(
    session: AsyncSession,
    profesional_id: uuid.UUID,
    prestacion_id: uuid.UUID,
    inicio: datetime,
    nombre: str,
    telefono: str | None,
    email: str | None,
    sillon_id: uuid.UUID | None = None,
) -> Turno:
    """Crea una reserva pública guest con auto-asignación de sillón y token_cancelacion."""
    inicio = bookings._asegurar_aware(inicio)

    # Validar profesional y prestación
    prof = await session.get(bookings.Profesional, profesional_id)
    if prof is None or not prof.activo:
        raise NotFound("PROFESIONAL_INVALIDO", "Profesional inexistente o inactivo")

    prest = await session.get(bookings.Prestacion, prestacion_id)
    if prest is None or not prest.activa:
        raise NotFound("PRESTACION_INVALIDA", "Prestacion inexistente o inactiva")

    fin = rules.calcular_fin(inicio, prest.duracion_min)
    await bookings._validar_temporalidad(session, profesional_id, inicio, fin)

    # Auto-asignación de sillón si no fue provisto
    if sillon_id is None:
        sillon_id = await autoasignar_sillon(session, inicio, fin)
    else:
        sillon = await session.get(Sillon, sillon_id)
        if sillon is None or not sillon.activo:
            raise NotFound("SILLON_INVALIDO", "Sillon inexistente o inactivo")
        await bookings._precheck_rn02(session, profesional_id, sillon_id, inicio, fin)

    paciente = await bookings.get_or_create_paciente(session, nombre, telefono, email)
    await bookings._precheck_rn05(session, paciente.id, inicio)

    token = secrets.token_urlsafe(32)

    turno = Turno(
        profesional_id=profesional_id,
        sillon_id=sillon_id,
        prestacion_id=prestacion_id,
        paciente_id=paciente.id,
        inicio=inicio,
        fin=fin,
        estado="activo",
        token_cancelacion=token,
    )
    session.add(turno)

    try:
        await session.flush()
    except IntegrityError as exc:
        await session.rollback()
        code = conflict_code_from_integrity_error(exc)
        raise DomainConflict(code, "Conflicto de agenda al persistir la reserva", status=409)

    await session.commit()
    await session.refresh(turno)

    try:
        get_notification_service().notify_turn_created(turno.id)
    except Exception as exc:
        logging.getLogger(__name__).warning("Fallo notificacion best-effort en reserva guest: %s", exc)

    return turno


async def cancelar_reserva_por_token(session: AsyncSession, token: str) -> Turno:
    """Cancela un turno mediante su token_cancelacion con idempotencia."""
    res = await session.execute(
        select(Turno).where(Turno.token_cancelacion == token).limit(1)
    )
    turno = res.scalar_one_or_none()
    if turno is None:
        raise NotFound("NO_ENCONTRADO", "Token de cancelación inexistente")

    if turno.estado == "cancelado":
        return turno

    turno.estado = "cancelado"
    turno.cancelled_at = _ahora()

    await session.commit()
    await session.refresh(turno)

    try:
        get_notification_service().notify_turn_updated(turno.id)
    except Exception as exc:
        logging.getLogger(__name__).warning("Fallo notificacion best-effort en cancelacion por token: %s", exc)

    return turno

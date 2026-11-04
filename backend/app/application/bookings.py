"""Orquestacion del alta y reprogramacion: RN01/RN03 + prechecks RN02 (D-02).

La app pre-valida para dar 409 claro, pero la base decide (D-01):
todo IntegrityError se mapea por nombre de constraint y nunca es 500.
"""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import logging
import uuid

from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_tz_consultorio
from app.core.errors import (
    DomainConflict,
    NotFound,
    conflict_code_from_integrity_error,
)
from app.domain import rules
from app.domain.models import (
    HorarioAtencion,
    PacienteGuest,
    Prestacion,
    Profesional,
    Sillon,
    Turno,
)
from app.notifications import get_notification_service


def _ahora() -> datetime:
    return datetime.now(ZoneInfo(get_tz_consultorio()))


def _asegurar_aware(inicio: datetime) -> datetime:
    if inicio.tzinfo is None:
        return inicio.replace(tzinfo=ZoneInfo(get_tz_consultorio()))
    return inicio


def _normalizar_telefono(telefono: str | None) -> str | None:
    if not telefono:
        return None
    digitos = "".join(c for c in telefono if c.isdigit())
    return digitos or None


def _normalizar_email(email: str | None) -> str | None:
    if not email:
        return None
    return email.strip().lower() or None


async def get_or_create_paciente(
    session: AsyncSession,
    nombre: str,
    telefono: str | None,
    email: str | None,
) -> PacienteGuest:
    nombre_limpio = " ".join(nombre.split())
    tel_norm = _normalizar_telefono(telefono)
    mail_norm = _normalizar_email(email)

    criterios = []
    if tel_norm:
        criterios.append(PacienteGuest.telefono == tel_norm)
    if mail_norm:
        criterios.append(PacienteGuest.email == mail_norm)

    if criterios:
        condicion = criterios[0] if len(criterios) == 1 else (criterios[0] | criterios[1])
        res = await session.execute(
            select(PacienteGuest).where(condicion).limit(1)
        )
        existente = res.scalar_one_or_none()
        if existente is not None:
            return existente

    paciente = PacienteGuest(
        nombre=nombre_limpio, telefono=tel_norm, email=mail_norm
    )
    session.add(paciente)
    await session.flush()
    return paciente


async def _bloques_del_dia(
    session: AsyncSession, profesional_id, dia_semana: int
) -> list[tuple]:
    res = await session.execute(
        select(HorarioAtencion.hora_desde, HorarioAtencion.hora_hasta).where(
            and_(
                HorarioAtencion.dia_semana == dia_semana,
                HorarioAtencion.profesional_id.is_(None),
            )
        )
    )
    bloques = list(res.all())
    res = await session.execute(
        select(HorarioAtencion.hora_desde, HorarioAtencion.hora_hasta).where(
            and_(
                HorarioAtencion.dia_semana == dia_semana,
                HorarioAtencion.profesional_id == profesional_id,
            )
        )
    )
    return bloques + list(res.all())


async def _validar_temporalidad(
    session: AsyncSession, profesional_id, inicio: datetime, fin: datetime
) -> None:
    if rules.esta_en_pasado(inicio, _ahora()):
        raise DomainConflict(
            "RN03_PASADO", "El turno no puede ser en el pasado", status=422
        )
    bloques = await _bloques_del_dia(session, profesional_id, inicio.weekday())
    if not rules.dentro_de_horario(inicio, fin, bloques):
        raise DomainConflict(
            "RN03_FUERA_DE_HORARIO", "Fuera del horario de atencion", status=422
        )


async def _precheck_rn02(
    session: AsyncSession,
    profesional_id,
    sillon_id,
    inicio: datetime,
    fin: datetime,
) -> None:
    solapa = and_(
        Turno.estado == "activo",
        Turno.inicio < fin,
        Turno.fin > inicio,
    )
    res = await session.execute(
        select(Turno.id).where(
            solapa, Turno.profesional_id == profesional_id
        ).limit(1)
    )
    if res.first() is not None:
        raise DomainConflict(
            "RN02_PROFESIONAL", "El profesional ya tiene un turno activo en ese rango"
        )
    res = await session.execute(
        select(Turno.id).where(solapa, Turno.sillon_id == sillon_id).limit(1)
    )
    if res.first() is not None:
        raise DomainConflict(
            "RN02_SILLON", "El sillon ya esta ocupado en ese rango"
        )


async def _precheck_rn05(
    session: AsyncSession, paciente_id, inicio: datetime
) -> None:
    """RN05: maximo 1 turno activo por paciente y dia calendario."""
    tz = ZoneInfo(get_tz_consultorio())
    inicio_local = inicio.astimezone(tz)
    dia = inicio_local.date()
    inicio_dia = datetime(dia.year, dia.month, dia.day, tzinfo=tz)
    fin_dia = inicio_dia + timedelta(days=1)

    res = await session.execute(
        select(Turno.id).where(
            Turno.paciente_id == paciente_id,
            Turno.estado == "activo",
            Turno.inicio >= inicio_dia,
            Turno.inicio < fin_dia,
        ).limit(1)
    )
    if res.first() is not None:
        raise DomainConflict(
            "RN05",
            "El paciente ya tiene un turno activo este dia",
            status=409,
        )


async def _cargar_recursos(
    session: AsyncSession, profesional_id, sillon_id, prestacion_id
) -> Prestacion:
    prof = await session.get(Profesional, profesional_id)
    if prof is None or not prof.activo:
        raise NotFound(
            "PROFESIONAL_INVALIDO", "Profesional inexistente o inactivo"
        )
    sillon = await session.get(Sillon, sillon_id)
    if sillon is None or not sillon.activo:
        raise NotFound("SILLON_INVALIDO", "Sillon inexistente o inactivo")
    prest = await session.get(Prestacion, prestacion_id)
    if prest is None or not prest.activa:
        raise NotFound("PRESTACION_INVALIDA", "Prestacion inexistente o inactiva")
    return prest


async def crear_turno(
    session: AsyncSession,
    profesional_id,
    sillon_id,
    prestacion_id,
    inicio: datetime,
    nombre: str,
    telefono: str | None,
    email: str | None,
) -> Turno:
    inicio = _asegurar_aware(inicio)
    prest = await _cargar_recursos(session, profesional_id, sillon_id, prestacion_id)
    paciente = await get_or_create_paciente(session, nombre, telefono, email)
    fin = rules.calcular_fin(inicio, prest.duracion_min)
    await _validar_temporalidad(session, profesional_id, inicio, fin)
    await _precheck_rn02(session, profesional_id, sillon_id, inicio, fin)
    await _precheck_rn05(session, paciente.id, inicio)
    turno = Turno(
        profesional_id=profesional_id,
        sillon_id=sillon_id,
        prestacion_id=prest.id,
        paciente_id=paciente.id,
        inicio=inicio,
        fin=fin,
        estado="activo",
    )
    session.add(turno)
    try:
        await session.flush()
    except IntegrityError as exc:
        await session.rollback()
        code = conflict_code_from_integrity_error(exc)
        raise DomainConflict(code, "Conflicto de agenda al persistir el turno")
    await session.commit()
    try:
        get_notification_service().notify_turn_created(turno.id)
    except Exception as exc:
        logging.getLogger(__name__).warning('Fallo notificacion best-effort: %s', exc)
    return turno


async def cancelar_turno(session: AsyncSession, turno_id) -> Turno:
    """RN04: cancela un turno activo registrando cancelled_at e idempotente si ya estaba cancelado."""
    turno = await session.get(Turno, turno_id)
    if turno is None:
        raise NotFound("NO_ENCONTRADO", "Turno inexistente")
    if turno.estado == "cancelado":
        return turno
    turno.estado = "cancelado"
    turno.cancelled_at = _ahora()
    await session.commit()
    await session.refresh(turno)
    try:
        get_notification_service().notify_turn_updated(turno.id)
    except Exception as exc:
        logging.getLogger(__name__).warning("Fallo notificacion best-effort: %s", exc)
    return turno


async def reprogramar_turno(
    session: AsyncSession,
    turno_id: uuid.UUID,
    nuevo_inicio: datetime,
    nuevo_sillon_id: uuid.UUID | None = None,
) -> tuple[Turno, Turno]:
    """C-23: Reprogramación atómica de turno en una única transacción.

    Cancela el turno original y crea el nuevo turno para el mismo paciente,
    profesional y prestación (o sillón alternativo si se especificó).
    Si ocurre cualquier conflicto (RN02, RN03, RN05), se realiza rollback total.
    """
    turno_orig = await session.get(Turno, turno_id)
    if turno_orig is None:
        raise NotFound("NO_ENCONTRADO", "Turno inexistente")
    if turno_orig.estado == "cancelado":
        raise DomainConflict("TURNO_NO_ACTIVO", "El turno origen ya se encuentra cancelado")

    sillon_destino = nuevo_sillon_id or turno_orig.sillon_id
    nuevo_inicio = _asegurar_aware(nuevo_inicio)

    prest = await _cargar_recursos(
        session, turno_orig.profesional_id, sillon_destino, turno_orig.prestacion_id
    )
    fin_nuevo = rules.calcular_fin(nuevo_inicio, prest.duracion_min)

    # Validaciones temporales y disponibilidad destino
    await _validar_temporalidad(session, turno_orig.profesional_id, nuevo_inicio, fin_nuevo)
    await _precheck_rn02(session, turno_orig.profesional_id, sillon_destino, nuevo_inicio, fin_nuevo)

    # Cancelar original en memoria/sesión
    turno_orig.estado = "cancelado"
    turno_orig.cancelled_at = _ahora()

    # Precheck RN-05 posterior a cancelación de turno original
    await _precheck_rn05(session, turno_orig.paciente_id, nuevo_inicio)

    # Crear nuevo turno
    nuevo_turno = Turno(
        profesional_id=turno_orig.profesional_id,
        sillon_id=sillon_destino,
        prestacion_id=turno_orig.prestacion_id,
        paciente_id=turno_orig.paciente_id,
        inicio=nuevo_inicio,
        fin=fin_nuevo,
        estado="activo",
    )
    session.add(nuevo_turno)

    try:
        await session.flush()
    except IntegrityError as exc:
        await session.rollback()
        code = conflict_code_from_integrity_error(exc)
        raise DomainConflict(code, "Conflicto de agenda al reprogramar el turno")

    await session.commit()
    await session.refresh(turno_orig)
    await session.refresh(nuevo_turno)

    # Notificaciones best-effort
    try:
        service = get_notification_service()
        service.notify_turn_updated(turno_orig.id)
        service.notify_turn_created(nuevo_turno.id)
    except Exception as exc:
        logging.getLogger(__name__).warning("Fallo notificacion best-effort en reprogramacion: %s", exc)

    return turno_orig, nuevo_turno

"""Orquestacion de reservas: RN01/RN03/RN04/RN05 + prechecks RN02 (D-03).

La app pre-valida para dar 409 claro, pero la base decide (D-01):
todo IntegrityError se mapea por nombre de constraint y nunca es 500.
"""
import secrets
from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import and_, func, select
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
from app.notifications.interface import NotificationService


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
    limpio = email.strip().lower()
    return limpio or None


async def get_or_create_paciente(
    session: AsyncSession, nombre: str, telefono: str | None, email: str | None
) -> PacienteGuest:
    tel = _normalizar_telefono(telefono)
    mail = _normalizar_email(email)
    stmt = select(PacienteGuest)
    if tel and mail:
        stmt = stmt.where(
            (PacienteGuest.telefono == tel) | (PacienteGuest.email == mail)
        )
    elif tel:
        stmt = stmt.where(PacienteGuest.telefono == tel)
    else:
        stmt = stmt.where(PacienteGuest.email == mail)
    existente = (await session.execute(stmt)).scalars().first()
    if existente is not None:
        return existente
    paciente = PacienteGuest(nombre=nombre, telefono=tel, email=mail)
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
    ahora = _ahora()
    if rules.esta_en_pasado(inicio, ahora):
        raise DomainConflict("RN03_PASADO", "El turno no puede ser en el pasado")
    bloques = await _bloques_del_dia(session, profesional_id, inicio.weekday())
    if not rules.dentro_de_horario(inicio, fin, bloques):
        raise DomainConflict("RN03_FUERA_DE_HORARIO", "Fuera del horario de atencion")


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


async def _precheck_rn05(session: AsyncSession, paciente_id, inicio: datetime) -> None:
    tz_nombre = get_tz_consultorio()
    fecha = inicio.astimezone(ZoneInfo(tz_nombre)).date()
    res = await session.execute(
        select(Turno.id).where(
            and_(
                Turno.paciente_id == paciente_id,
                Turno.estado == "activo",
                func.date(func.timezone(tz_nombre, Turno.inicio)) == fecha,
            )
        ).limit(1)
    )
    if res.first() is not None:
        raise DomainConflict(
            "RN05", "El paciente ya tiene un turno activo ese dia"
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


async def _insertar_turno(
    session: AsyncSession,
    profesional_id,
    sillon_id,
    prest: Prestacion,
    paciente: PacienteGuest,
    inicio: datetime,
    token: str | None,
) -> Turno:
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
        token_cancelacion=token,
    )
    session.add(turno)
    try:
        await session.flush()
    except IntegrityError as exc:
        await session.rollback()
        code = conflict_code_from_integrity_error(exc)
        raise DomainConflict(code, "Conflicto de agenda al persistir el turno")
    return turno


async def _notificar_best_effort(
    notify: NotificationService | None, evento: str, turno: Turno
) -> None:
    if notify is None:
        return
    try:
        destino = turno.paciente_id
        await notify.notificar(evento, str(turno.id), str(destino))
    except Exception:
        import logging

        logging.getLogger(__name__).exception("notificacion best-effort fallida")


async def crear_turno(
    session: AsyncSession,
    profesional_id,
    sillon_id,
    prestacion_id,
    inicio: datetime,
    nombre: str,
    telefono: str | None,
    email: str | None,
    notify: NotificationService | None = None,
) -> Turno:
    inicio = _asegurar_aware(inicio)
    prest = await _cargar_recursos(session, profesional_id, sillon_id, prestacion_id)
    paciente = await get_or_create_paciente(session, nombre, telefono, email)
    turno = await _insertar_turno(
        session, profesional_id, sillon_id, prest, paciente, inicio, None
    )
    await session.commit()
    await _notificar_best_effort(notify, "turno_creado", turno)
    return turno


async def _sillones_activos(session: AsyncSession) -> list[Sillon]:
    res = await session.execute(
        select(Sillon).where(Sillon.activo.is_(True)).order_by(Sillon.nombre)
    )
    return list(res.scalars().all())


async def crear_reserva(
    session: AsyncSession,
    profesional_id,
    prestacion_id,
    inicio: datetime,
    nombre: str,
    telefono: str | None,
    email: str | None,
    sillon_id=None,
    notify: NotificationService | None = None,
) -> Turno:
    """Guest publica. Sillon opcional con auto-asignacion al primero libre (D-10)."""
    inicio = _asegurar_aware(inicio)
    token = secrets.token_urlsafe(32)
    if sillon_id is not None:
        prest = await _cargar_recursos(
            session, profesional_id, sillon_id, prestacion_id
        )
        paciente = await get_or_create_paciente(session, nombre, telefono, email)
        turno = await _insertar_turno(
            session, profesional_id, sillon_id, prest, paciente, inicio, token
        )
        await session.commit()
        await _notificar_best_effort(notify, "reserva_creada", turno)
        return turno
    # validacion de profesional/prestacion sin sillon fijo
    prof = await session.get(Profesional, profesional_id)
    if prof is None or not prof.activo:
        raise NotFound(
            "PROFESIONAL_INVALIDO", "Profesional inexistente o inactivo"
        )
    prest = await session.get(Prestacion, prestacion_id)
    if prest is None or not prest.activa:
        raise NotFound("PRESTACION_INVALIDA", "Prestacion inexistente o inactiva")
    paciente = await get_or_create_paciente(session, nombre, telefono, email)
    fin = rules.calcular_fin(inicio, prest.duracion_min)
    await _validar_temporalidad(session, profesional_id, inicio, fin)
    await _precheck_rn05(session, paciente.id, inicio)
    ultimo_error: DomainConflict | None = None
    for sillon in await _sillones_activos(session):
        try:
            async with session.begin_nested():
                await _precheck_rn02(session, profesional_id, sillon.id, inicio, fin)
                turno = Turno(
                    profesional_id=profesional_id,
                    sillon_id=sillon.id,
                    prestacion_id=prest.id,
                    paciente_id=paciente.id,
                    inicio=inicio,
                    fin=fin,
                    estado="activo",
                    token_cancelacion=token,
                )
                session.add(turno)
                await session.flush()
        except IntegrityError as exc:
            code = conflict_code_from_integrity_error(exc)
            ultimo_error = DomainConflict(code, "Sillon ocupado, probando siguiente")
            continue
        except DomainConflict as exc:
            if exc.code == "RN02_SILLON":
                ultimo_error = exc
                continue
            raise
        else:
            await session.commit()
            await _notificar_best_effort(notify, "reserva_creada", turno)
            return turno
    if ultimo_error is not None and ultimo_error.code == "RN02_PROFESIONAL":
        raise ultimo_error
    raise DomainConflict("RN02_SILLON", "Ningun sillon libre en ese rango")


async def cancelar_turno(
    session: AsyncSession,
    turno_id,
    notify: NotificationService | None = None,
) -> Turno:
    turno = await session.get(Turno, turno_id)
    if turno is None:
        raise NotFound("TURNO_INEXISTENTE", "Turno inexistente")
    if not rules.puede_cancelar(turno.estado):
        raise DomainConflict("TURNO_YA_CANCELADO", "El turno ya esta cancelado")
    turno.estado = "cancelado"
    turno.cancelled_at = _ahora()
    await session.commit()
    await _notificar_best_effort(notify, "turno_cancelado", turno)
    return turno


async def cancelar_por_token(
    session: AsyncSession,
    token: str,
    notify: NotificationService | None = None,
) -> Turno | None:
    res = await session.execute(
        select(Turno).where(Turno.token_cancelacion == token)
    )
    turno = res.scalars().first()
    if turno is None:
        return None
    if not rules.puede_cancelar(turno.estado):
        raise DomainConflict("TURNO_YA_CANCELADO", "La reserva ya esta cancelada")
    turno.estado = "cancelado"
    turno.cancelled_at = _ahora()
    await session.commit()
    await _notificar_best_effort(notify, "reserva_cancelada", turno)
    return turno


async def reprogramar_turno(
    session: AsyncSession,
    turno_id,
    nuevo_inicio: datetime,
    notify: NotificationService | None = None,
) -> Turno:
    """Cancelar+crear en una transaccion (D-09): si el destino choca, rollback total."""
    nuevo_inicio = _asegurar_aware(nuevo_inicio)
    original = await session.get(Turno, turno_id)
    if original is None:
        raise NotFound("TURNO_INEXISTENTE", "Turno inexistente")
    if not rules.puede_cancelar(original.estado):
        raise DomainConflict("TURNO_YA_CANCELADO", "El turno ya esta cancelado")
    prest = await session.get(Prestacion, original.prestacion_id)
    assert prest is not None
    nuevo_fin = rules.calcular_fin(nuevo_inicio, prest.duracion_min)
    try:
        original.estado = "cancelado"
        original.cancelled_at = _ahora()
        await session.flush()
        await _validar_temporalidad(
            session, original.profesional_id, nuevo_inicio, nuevo_fin
        )
        await _precheck_rn02(
            session,
            original.profesional_id,
            original.sillon_id,
            nuevo_inicio,
            nuevo_fin,
        )
        await _precheck_rn05(session, original.paciente_id, nuevo_inicio)
        nuevo = Turno(
            profesional_id=original.profesional_id,
            sillon_id=original.sillon_id,
            prestacion_id=original.prestacion_id,
            paciente_id=original.paciente_id,
            inicio=nuevo_inicio,
            fin=nuevo_fin,
            estado="activo",
            token_cancelacion=original.token_cancelacion,
        )
        original.token_cancelacion = None
        session.add(nuevo)
        await session.flush()
    except IntegrityError as exc:
        await session.rollback()
        code = conflict_code_from_integrity_error(exc)
        raise DomainConflict(code, "Destino ocupado, se conserva el turno original")
    except DomainConflict:
        await session.rollback()
        raise
    await session.commit()
    await _notificar_best_effort(notify, "turno_reprogramado", nuevo)
    return nuevo

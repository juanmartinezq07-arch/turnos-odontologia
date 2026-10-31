"""Orquestacion del alta: RN01/RN03 + prechecks RN02 (D-02).

La app pre-valida para dar 409 claro, pero la base decide (D-01):
todo IntegrityError se mapea por nombre de constraint y nunca es 500.
"""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

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
    return turno

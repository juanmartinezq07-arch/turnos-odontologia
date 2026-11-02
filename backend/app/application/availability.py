"""Cálculo de disponibilidad real por profesional, fecha y prestación (C-25 / US-002).

Orquesta las lecturas de HorarioAtencion y Turnos activos en DB y delega el
cálculo determinista a la función pura rules.calcular_slots_disponibles.
"""
import uuid
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_tz_consultorio
from app.core.errors import NotFound
from app.domain import rules
from app.domain.models import HorarioAtencion, Prestacion, Profesional, Turno


def _ahora_consultorio() -> datetime:
    return datetime.now(ZoneInfo(get_tz_consultorio()))


async def _bloques_del_dia(
    session: AsyncSession, profesional_id: uuid.UUID, dia_semana: int
) -> list[tuple]:
    res_global = await session.execute(
        select(HorarioAtencion.hora_desde, HorarioAtencion.hora_hasta).where(
            and_(
                HorarioAtencion.dia_semana == dia_semana,
                HorarioAtencion.profesional_id.is_(None),
            )
        )
    )
    bloques = list(res_global.all())
    res_prof = await session.execute(
        select(HorarioAtencion.hora_desde, HorarioAtencion.hora_hasta).where(
            and_(
                HorarioAtencion.dia_semana == dia_semana,
                HorarioAtencion.profesional_id == profesional_id,
            )
        )
    )
    return bloques + list(res_prof.all())


async def _turnos_activos_del_dia(
    session: AsyncSession,
    profesional_id: uuid.UUID,
    fecha: date,
    tz: ZoneInfo,
) -> list[tuple[datetime, datetime]]:
    inicio_dia = datetime(fecha.year, fecha.month, fecha.day, tzinfo=tz)
    fin_dia = inicio_dia + timedelta(days=1)
    stmt = (
        select(Turno.inicio, Turno.fin)
        .where(
            and_(
                Turno.profesional_id == profesional_id,
                Turno.estado == "activo",
                Turno.inicio < fin_dia,
                Turno.fin > inicio_dia,
            )
        )
        .order_by(Turno.inicio.asc())
    )
    res = await session.execute(stmt)
    return [(row[0], row[1]) for row in res.all()]


async def consultar_disponibilidad(
    session: AsyncSession,
    profesional_id: uuid.UUID,
    fecha: date,
    prestacion_id: uuid.UUID,
    ahora: datetime | None = None,
) -> list[tuple[datetime, datetime]]:
    """Devuelve la lista determinista de slots [inicio, fin) disponibles."""
    prof = await session.get(Profesional, profesional_id)
    if prof is None or not prof.activo:
        raise NotFound(
            "PROFESIONAL_INVALIDO", "Profesional inexistente o inactivo"
        )
    prest = await session.get(Prestacion, prestacion_id)
    if prest is None or not prest.activa:
        raise NotFound(
            "PRESTACION_INVALIDA", "Prestacion inexistente o inactiva"
        )

    tz = ZoneInfo(get_tz_consultorio())
    instante_ahora = ahora if ahora is not None else _ahora_consultorio()
    bloques = await _bloques_del_dia(session, profesional_id, fecha.weekday())
    ocupados = await _turnos_activos_del_dia(session, profesional_id, fecha, tz)

    return rules.calcular_slots_disponibles(
        fecha=fecha,
        bloques=bloques,
        ocupados=ocupados,
        duracion_min=prest.duracion_min,
        ahora=instante_ahora,
        tz=tz,
    )

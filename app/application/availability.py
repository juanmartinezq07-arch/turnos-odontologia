"""Disponibilidad determinista (D-08): horario menos activos, RN01 y RN03."""
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_tz_consultorio
from app.domain.models import HorarioAtencion, Prestacion, Profesional, Turno


def generar_slots(
    bloques: list[tuple[time, time]],
    ocupados: list[tuple[datetime, datetime]],
    duracion_min: int,
    dia: date,
    tz: ZoneInfo,
    desde: datetime | None = None,
) -> list[datetime]:
    """Funcion pura: mismos inputs -> mismos slots ordenados."""
    slots: list[datetime] = []
    paso = timedelta(minutes=duracion_min)
    for hora_desde, hora_hasta in sorted(bloques):
        cursor = datetime.combine(dia, hora_desde, tzinfo=tz)
        limite = datetime.combine(dia, hora_hasta, tzinfo=tz)
        while cursor + paso <= limite:
            fin = cursor + paso
            if desde is not None and cursor < desde:
                cursor += paso
                continue
            choca = any(cursor < o_fin and fin > o_ini for o_ini, o_fin in ocupados)
            if not choca:
                slots.append(cursor)
            cursor += paso
    return slots


async def obtener_disponibilidad(
    session: AsyncSession,
    profesional_id,
    fecha: date,
    prestacion_id,
) -> list[datetime]:
    tz = ZoneInfo(get_tz_consultorio())
    prest = await session.get(Prestacion, prestacion_id)
    if prest is None or not prest.activa:
        from app.core.errors import NotFound

        raise NotFound("PRESTACION_INVALIDA", "Prestacion inexistente o inactiva")
    prof = await session.get(Profesional, profesional_id)
    if prof is None or not prof.activo:
        from app.core.errors import NotFound

        raise NotFound(
            "PROFESIONAL_INVALIDO", "Profesional inexistente o inactivo"
        )
    dia_semana = fecha.weekday()
    res = await session.execute(
        select(HorarioAtencion).where(
            and_(
                HorarioAtencion.dia_semana == dia_semana,
                HorarioAtencion.profesional_id.is_(None),
            )
        )
    )
    bloques = [(h.hora_desde, h.hora_hasta) for h in res.scalars().all()]
    res = await session.execute(
        select(HorarioAtencion).where(
            and_(
                HorarioAtencion.dia_semana == dia_semana,
                HorarioAtencion.profesional_id == profesional_id,
            )
        )
    )
    bloques += [(h.hora_desde, h.hora_hasta) for h in res.scalars().all()]
    inicio_dia = datetime.combine(fecha, time(0, 0), tzinfo=tz)
    fin_dia = inicio_dia + timedelta(days=1)
    res = await session.execute(
        select(Turno.inicio, Turno.fin).where(
            and_(
                Turno.profesional_id == profesional_id,
                Turno.estado == "activo",
                Turno.inicio < fin_dia,
                Turno.fin > inicio_dia,
            )
        )
    )
    ocupados = [(i, f) for i, f in res.all()]
    ahora = datetime.now(tz) if fecha == datetime.now(tz).date() else None
    return generar_slots(bloques, ocupados, prest.duracion_min, fecha, tz, desde=ahora)

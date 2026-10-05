"""GET /agenda (odontologo, solo propia, 403 ajena)."""
import uuid
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_tz_consultorio
from app.core.security import get_current_odontologo, require_odontologo_agenda
from app.db import get_session
from app.domain.models import PacienteGuest, Prestacion, Sillon, Turno
from app.schemas.turno import AgendaOut, TurnoAgendaOut

router = APIRouter()


@router.get("/agenda", response_model=AgendaOut)
async def agenda(
    profesional_id: uuid.UUID,
    fecha: date,
    incluir_cancelados: bool = False,
    session: AsyncSession = Depends(get_session),
    actual: str | None = Depends(get_current_odontologo),
):
    await require_odontologo_agenda(str(profesional_id), actual)
    tz = ZoneInfo(get_tz_consultorio())
    inicio_dia = datetime.combine(fecha, time(0, 0), tzinfo=tz)
    fin_dia = inicio_dia + timedelta(days=1)
    filtros = [
        Turno.profesional_id == profesional_id,
        Turno.inicio < fin_dia,
        Turno.fin > inicio_dia,
    ]
    if not incluir_cancelados:
        filtros.append(Turno.estado == "activo")
    res = await session.execute(
        select(Turno).where(and_(*filtros)).order_by(Turno.inicio)
    )
    turnos = res.scalars().all()
    prest_ids = {t.prestacion_id for t in turnos}
    sillon_ids = {t.sillon_id for t in turnos}
    paciente_ids = {t.paciente_id for t in turnos}
    prests = (
        (await session.execute(select(Prestacion).where(Prestacion.id.in_(prest_ids))))
        .scalars()
        .all()
        if prest_ids
        else []
    )
    sills = (
        (await session.execute(select(Sillon).where(Sillon.id.in_(sillon_ids))))
        .scalars()
        .all()
        if sillon_ids
        else []
    )
    pacs = (
        (
            await session.execute(
                select(PacienteGuest).where(PacienteGuest.id.in_(paciente_ids))
            )
        )
        .scalars()
        .all()
        if paciente_ids
        else []
    )
    por_prest = {p.id: p for p in prests}
    por_sillon = {s.id: s for s in sills}
    por_pac = {p.id: p for p in pacs}
    items = [
        TurnoAgendaOut(
            id=t.id,
            inicio=t.inicio,
            fin=t.fin,
            estado=t.estado,
            prestacion=por_prest[t.prestacion_id].nombre,
            duracion_min=por_prest[t.prestacion_id].duracion_min,
            sillon=por_sillon[t.sillon_id].nombre,
            paciente=por_pac[t.paciente_id].nombre,
        )
        for t in turnos
    ]
    return AgendaOut(profesional_id=profesional_id, fecha=fecha, turnos=items)

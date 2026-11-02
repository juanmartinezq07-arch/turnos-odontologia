"""Caso de uso de lectura de agenda del dia del odontologo (US-006 / C-27)."""
from datetime import date, datetime, time, timedelta
import uuid
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_tz_consultorio
from app.domain.models import PacienteGuest, Prestacion, Sillon, Turno
from app.schemas.agenda import (
    AgendaPacienteOut,
    AgendaPrestacionOut,
    AgendaSillonOut,
    AgendaTurnoOut,
)


async def consultar_agenda_dia(
    session: AsyncSession,
    profesional_id: uuid.UUID,
    fecha: date,
    incluir_cancelados: bool = False,
) -> list[AgendaTurnoOut]:
    """Devuelve los turnos del profesional en la fecha local ordenados por inicio."""
    tz = ZoneInfo(get_tz_consultorio())
    inicio_dia = datetime.combine(fecha, time(0, 0), tzinfo=tz)
    fin_dia = inicio_dia + timedelta(days=1)

    stmt = (
        select(Turno, Prestacion, Sillon, PacienteGuest)
        .join(Prestacion, Turno.prestacion_id == Prestacion.id)
        .join(Sillon, Turno.sillon_id == Sillon.id)
        .join(PacienteGuest, Turno.paciente_id == PacienteGuest.id)
        .where(
            Turno.profesional_id == profesional_id,
            Turno.inicio >= inicio_dia,
            Turno.inicio < fin_dia,
        )
    )
    if not incluir_cancelados:
        stmt = stmt.where(Turno.estado == "activo")

    stmt = stmt.order_by(Turno.inicio.asc())
    filas = (await session.execute(stmt)).all()

    return [
        AgendaTurnoOut(
            id=turno.id,
            profesional_id=turno.profesional_id,
            inicio=turno.inicio,
            fin=turno.fin,
            estado=turno.estado,
            prestacion=AgendaPrestacionOut.model_validate(prestacion),
            sillon=AgendaSillonOut.model_validate(sillon),
            paciente=AgendaPacienteOut.model_validate(paciente),
        )
        for turno, prestacion, sillon, paciente in filas
    ]

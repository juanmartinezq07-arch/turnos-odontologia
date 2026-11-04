"""POST /turnos, POST /turnos/{turno_id}/cancelacion y POST /turnos/{turno_id}/reprogramacion."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application import bookings
from app.core.security import require_recepcion
from app.db import get_session
from app.schemas.turno import ReprogramacionOut, TurnoCreate, TurnoOut, TurnoReprogramar

router = APIRouter()


def _out(turno) -> TurnoOut:
    return TurnoOut(
        id=turno.id,
        profesional_id=turno.profesional_id,
        sillon_id=turno.sillon_id,
        prestacion_id=turno.prestacion_id,
        paciente_id=turno.paciente_id,
        inicio=turno.inicio,
        fin=turno.fin,
        estado=turno.estado,
        cancelled_at=turno.cancelled_at,
    )


@router.post("/turnos", response_model=TurnoOut, status_code=201)
async def alta_turno(
    payload: TurnoCreate,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(require_recepcion),
):
    turno = await bookings.crear_turno(
        session,
        payload.profesional_id,
        payload.sillon_id,
        payload.prestacion_id,
        payload.inicio,
        payload.paciente.nombre,
        payload.paciente.telefono,
        payload.paciente.email,
    )
    return _out(turno)


@router.post("/turnos/{turno_id}/cancelacion", response_model=TurnoOut, status_code=200)
async def cancelar_turno_endpoint(
    turno_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(require_recepcion),
):
    turno = await bookings.cancelar_turno(session, turno_id)
    return _out(turno)


@router.post("/turnos/{turno_id}/reprogramacion", response_model=ReprogramacionOut, status_code=200)
async def reprogramar_turno_endpoint(
    turno_id: uuid.UUID,
    payload: TurnoReprogramar,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(require_recepcion),
):
    orig, nuevo = await bookings.reprogramar_turno(
        session,
        turno_id=turno_id,
        nuevo_inicio=payload.inicio,
        nuevo_sillon_id=payload.sillon_id,
    )
    return ReprogramacionOut(original=_out(orig), nuevo=_out(nuevo))

"""POST /turnos (recepcionista): alta evitando solapamientos."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application import bookings
from app.core.security import require_recepcion
from app.db import get_session
from app.schemas.turno import TurnoCreate, TurnoOut

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

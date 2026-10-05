"""POST /turnos + cancelacion y reprogramacion (recepcionista)."""
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application import bookings
from app.core.security import require_recepcion
from app.db import get_session
from app.notifications.mock import get_notifier
from app.schemas.turno import ReprogramarIn, TurnoCreate, TurnoOut

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
        token_cancelacion=turno.token_cancelacion,
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
        notify=get_notifier(),
    )
    return _out(turno)


@router.delete("/turnos/{turno_id}", response_model=TurnoOut)
async def cancelar_turno(
    turno_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(require_recepcion),
):
    turno = await bookings.cancelar_turno(session, turno_id, notify=get_notifier())
    return _out(turno)


@router.patch("/turnos/{turno_id}/reprogramacion", response_model=TurnoOut)
async def reprogramar_turno(
    turno_id: uuid.UUID,
    payload: ReprogramarIn,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(require_recepcion),
):
    turno = await bookings.reprogramar_turno(
        session, turno_id, payload.nuevo_inicio, notify=get_notifier()
    )
    return _out(turno)

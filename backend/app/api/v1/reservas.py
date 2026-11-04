"""Rutas de API públicas para reservas guest (C-29)."""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.application import reservas
from app.core.rate_limit import check_rate_limit
from app.db import get_session
from app.schemas.reserva import ReservaCreate, ReservaOut

router = APIRouter(tags=["reservas"])


@router.post("/reservas", response_model=ReservaOut, status_code=201)
async def crear_reserva(
    payload: ReservaCreate,
    request: Request,
    session: AsyncSession = Depends(get_session),
    _: None = Depends(check_rate_limit),
):
    turno = await reservas.crear_reserva_guest(
        session=session,
        profesional_id=payload.profesional_id,
        prestacion_id=payload.prestacion_id,
        inicio=payload.inicio,
        nombre=payload.paciente.nombre,
        telefono=payload.paciente.telefono,
        email=payload.paciente.email,
        sillon_id=payload.sillon_id,
    )
    return ReservaOut(
        id=turno.id,
        profesional_id=turno.profesional_id,
        sillon_id=turno.sillon_id,
        prestacion_id=turno.prestacion_id,
        paciente_id=turno.paciente_id,
        inicio=turno.inicio,
        fin=turno.fin,
        estado=turno.estado,
        cancelled_at=turno.cancelled_at,
        token_cancelacion=turno.token_cancelacion or "",
    )


@router.post("/reservas/{token}/cancelacion", response_model=ReservaOut, status_code=200)
async def cancelar_reserva(
    token: str,
    session: AsyncSession = Depends(get_session),
):
    turno = await reservas.cancelar_reserva_por_token(session, token)
    return ReservaOut(
        id=turno.id,
        profesional_id=turno.profesional_id,
        sillon_id=turno.sillon_id,
        prestacion_id=turno.prestacion_id,
        paciente_id=turno.paciente_id,
        inicio=turno.inicio,
        fin=turno.fin,
        estado=turno.estado,
        cancelled_at=turno.cancelled_at,
        token_cancelacion=turno.token_cancelacion or "",
    )

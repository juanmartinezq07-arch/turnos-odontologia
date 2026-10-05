"""POST /reservas publico con rate-limit + cancelacion por token (guest)."""
import time
import uuid

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.application import bookings
from app.core.config import get_reserva_rate_limit
from app.core.errors import NotFound
from app.db import get_session
from app.notifications.mock import get_notifier
from app.schemas.turno import ReservaCreate, ReservaOut, TurnoOut

router = APIRouter()

_ventanas: dict[str, list[float]] = {}


class RateLimited(Exception):
    pass


def reset_rate_limit() -> None:
    _ventanas.clear()


def _chequear_rate_limit(request: Request) -> None:
    cantidad, segundos = get_reserva_rate_limit()
    cliente = request.headers.get("x-forwarded-for") or (
        request.client.host if request.client else "anon"
    )
    ahora = time.monotonic()
    marcas = [m for m in _ventanas.get(cliente, []) if ahora - m < segundos]
    if len(marcas) >= cantidad:
        raise RateLimited()
    marcas.append(ahora)
    _ventanas[cliente] = marcas


@router.post("/reservas", response_model=ReservaOut, status_code=201)
async def crear_reserva(
    payload: ReservaCreate,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    _chequear_rate_limit(request)
    turno = await bookings.crear_reserva(
        session,
        payload.profesional_id,
        payload.prestacion_id,
        payload.inicio,
        payload.paciente.nombre,
        payload.paciente.telefono,
        payload.paciente.email,
        sillon_id=payload.sillon_id,
        notify=get_notifier(),
    )
    assert turno.token_cancelacion is not None
    return ReservaOut(
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


@router.post("/reservas/{token}/cancelacion", response_model=TurnoOut)
async def cancelar_reserva(
    token: str,
    session: AsyncSession = Depends(get_session),
):
    turno = await bookings.cancelar_por_token(
        session, token, notify=get_notifier()
    )
    if turno is None:
        raise NotFound("TOKEN_INVALIDO", "Token de cancelacion inexistente")
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

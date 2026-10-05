"""GET /disponibilidad publico y determinista."""
import uuid
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application import availability
from app.db import get_session
from app.schemas.turno import DisponibilidadOut

router = APIRouter()


@router.get("/disponibilidad", response_model=DisponibilidadOut)
async def disponibilidad(
    profesional_id: uuid.UUID,
    fecha: date,
    prestacion_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
):
    slots = await availability.obtener_disponibilidad(
        session, profesional_id, fecha, prestacion_id
    )
    return DisponibilidadOut(
        profesional_id=profesional_id,
        fecha=fecha,
        prestacion_id=prestacion_id,
        slots=slots,
    )

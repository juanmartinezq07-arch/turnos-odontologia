"""GET /disponibilidad (C-25 / US-002): consulta pública de slots libres reales."""
import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.application import availability
from app.db import get_session
from app.schemas.disponibilidad import SlotDisponibilidadOut

router = APIRouter(tags=["disponibilidad"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/disponibilidad", response_model=list[SlotDisponibilidadOut])
async def get_disponibilidad(
    session: SessionDep,
    profesional_id: Annotated[uuid.UUID, Query()],
    fecha: Annotated[date, Query()],
    prestacion_id: Annotated[uuid.UUID, Query()],
) -> list[SlotDisponibilidadOut]:
    slots = await availability.consultar_disponibilidad(
        session=session,
        profesional_id=profesional_id,
        fecha=fecha,
        prestacion_id=prestacion_id,
    )
    return [SlotDisponibilidadOut(inicio=ini, fin=fin) for ini, fin in slots]

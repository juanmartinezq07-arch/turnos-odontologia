"""Endpoint autenticado de agenda diaria del odontologo (C-27 / US-006)."""
from datetime import date
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.agenda import consultar_agenda_dia
from app.core.security import require_odontologo
from app.db import get_session
from app.schemas.agenda import AgendaTurnoOut

router = APIRouter(tags=["agenda"])


@router.get("/agenda", response_model=list[AgendaTurnoOut])
async def get_agenda(
    profesional_id: uuid.UUID = Query(...),
    fecha: date = Query(...),
    incluir_cancelados: bool = Query(default=False),
    session: AsyncSession = Depends(get_session),
    _: None = Depends(require_odontologo),
) -> list[AgendaTurnoOut]:
    return await consultar_agenda_dia(
        session=session,
        profesional_id=profesional_id,
        fecha=fecha,
        incluir_cancelados=incluir_cancelados,
    )

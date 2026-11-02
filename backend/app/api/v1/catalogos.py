"""Endpoints públicos de catálogos (C-24): GET /profesionales, /sillones, /prestaciones.

Rutas públicas (KB-03): no exigen API key.
"""
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application import catalogs
from app.db import get_session
from app.schemas.catalogo import PrestacionOut, ProfesionalOut, SillonOut

router = APIRouter(tags=["catalogos"])

SessionDep = Annotated[AsyncSession, Depends(get_session)]


@router.get("/profesionales", response_model=list[ProfesionalOut])
async def get_profesionales(session: SessionDep) -> list[ProfesionalOut]:
    items = await catalogs.listar_profesionales_activos(session)
    return [ProfesionalOut.model_validate(p) for p in items]


@router.get("/sillones", response_model=list[SillonOut])
async def get_sillones(session: SessionDep) -> list[SillonOut]:
    items = await catalogs.listar_sillones_activos(session)
    return [SillonOut.model_validate(s) for s in items]


@router.get("/prestaciones", response_model=list[PrestacionOut])
async def get_prestaciones(session: SessionDep) -> list[PrestacionOut]:
    items = await catalogs.listar_prestaciones_activas(session)
    return [PrestacionOut.model_validate(pr) for pr in items]

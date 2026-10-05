"""Catalogos publicos de lectura."""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.domain.models import Prestacion, Profesional, Sillon
from app.schemas.turno import CatalogoOut, PrestacionOut

router = APIRouter()


@router.get("/profesionales", response_model=list[CatalogoOut])
async def profesionales(session: AsyncSession = Depends(get_session)):
    res = await session.execute(
        select(Profesional).where(Profesional.activo.is_(True))
    )
    return [
        CatalogoOut(id=p.id, nombre=f"{p.nombre} {p.apellido}")
        for p in res.scalars().all()
    ]


@router.get("/sillones", response_model=list[CatalogoOut])
async def sillones(session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Sillon).where(Sillon.activo.is_(True)))
    return [CatalogoOut(id=s.id, nombre=s.nombre) for s in res.scalars().all()]


@router.get("/prestaciones", response_model=list[PrestacionOut])
async def prestaciones(session: AsyncSession = Depends(get_session)):
    res = await session.execute(
        select(Prestacion).where(Prestacion.activa.is_(True))
    )
    return [
        PrestacionOut(id=p.id, nombre=p.nombre, duracion_min=p.duracion_min)
        for p in res.scalars().all()
    ]

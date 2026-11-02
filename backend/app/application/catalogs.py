"""Consultas de aplicación para los catálogos públicos (C-24).

Filtran solo recursos activos con orden determinista.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import Prestacion, Profesional, Sillon


async def listar_profesionales_activos(
    session: AsyncSession,
) -> list[Profesional]:
    stmt = (
        select(Profesional)
        .where(Profesional.activo.is_(True))
        .order_by(Profesional.apellido.asc(), Profesional.nombre.asc())
    )
    res = await session.execute(stmt)
    return list(res.scalars().all())


async def listar_sillones_activos(session: AsyncSession) -> list[Sillon]:
    stmt = (
        select(Sillon)
        .where(Sillon.activo.is_(True))
        .order_by(Sillon.nombre.asc())
    )
    res = await session.execute(stmt)
    return list(res.scalars().all())


async def listar_prestaciones_activas(
    session: AsyncSession,
) -> list[Prestacion]:
    stmt = (
        select(Prestacion)
        .where(Prestacion.activa.is_(True))
        .order_by(Prestacion.nombre.asc())
    )
    res = await session.execute(stmt)
    return list(res.scalars().all())

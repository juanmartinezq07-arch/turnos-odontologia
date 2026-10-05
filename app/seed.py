"""Seed ficticio (task 6.3). Solo datos sinteticos. Uso: python -m app.seed."""
import asyncio
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_tz_consultorio
from app.db import get_session_factory
from app.domain.models import (
    HorarioAtencion,
    PacienteGuest,
    Prestacion,
    Profesional,
    Sillon,
    Turno,
)

TZ = ZoneInfo(get_tz_consultorio())


async def seed(session: AsyncSession) -> dict:
    existe = (await session.execute(select(Profesional).limit(1))).first()
    if existe is not None:
        return {"seed": "ya existente"}
    p1 = Profesional(nombre="Maria", apellido="Gomez Demo", matricula="MAT-DEMO-001")
    p2 = Profesional(nombre="Carlos", apellido="Ruiz Demo", matricula="MAT-DEMO-002")
    s1 = Sillon(nombre="Sillon 1")
    s2 = Sillon(nombre="Sillon 2")
    c30 = Prestacion(nombre="Consulta Demo", duracion_min=30)
    o45 = Prestacion(nombre="Obturacion Demo", duracion_min=45)
    e90 = Prestacion(nombre="Endodoncia Demo", duracion_min=90)
    session.add_all([p1, p2, s1, s2, c30, o45, e90])
    await session.flush()
    horarios = [
        HorarioAtencion(
            profesional_id=None, dia_semana=d,
            hora_desde=time(9, 0), hora_hasta=time(18, 0),
        )
        for d in range(0, 5)
    ] + [
        HorarioAtencion(
            profesional_id=None, dia_semana=5,
            hora_desde=time(9, 0), hora_hasta=time(12, 0),
        )
    ]
    session.add_all(horarios)
    pa = PacienteGuest(
        nombre="Juan Perez Demo", telefono="1100000000", email="juan@example.com"
    )
    session.add(pa)
    await session.flush()
    ahora = datetime.now(TZ)
    dia = ahora.date()
    inicio_activo = datetime(dia.year, dia.month, dia.day, 10, 0, tzinfo=TZ)
    if inicio_activo <= ahora:
        inicio_activo = ahora.replace(microsecond=0) + timedelta(hours=1)
    session.add(
        Turno(
            profesional_id=p1.id, sillon_id=s1.id, prestacion_id=c30.id,
            paciente_id=pa.id, inicio=inicio_activo,
            fin=inicio_activo + timedelta(minutes=30),
            estado="activo",
        )
    )
    inicio_cancelado = inicio_activo + timedelta(hours=1)
    session.add(
        Turno(
            profesional_id=p1.id, sillon_id=s1.id, prestacion_id=c30.id,
            paciente_id=pa.id, inicio=inicio_cancelado,
            fin=inicio_cancelado + timedelta(minutes=30),
            estado="cancelado", cancelled_at=ahora,
        )
    )
    await session.commit()
    return {"seed": "ok", "profesionales": 2, "sillones": 2, "prestaciones": 3}


async def main() -> None:
    async with get_session_factory()() as session:
        print(await seed(session))


if __name__ == "__main__":
    asyncio.run(main())

"""Schemas Pydantic v2 estrictos para reservas públicas guest (C-29)."""
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.turno import PacienteIn


class _Estricto(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ReservaCreate(_Estricto):
    profesional_id: uuid.UUID
    prestacion_id: uuid.UUID
    inicio: datetime
    sillon_id: uuid.UUID | None = None
    paciente: PacienteIn


class ReservaOut(BaseModel):
    id: uuid.UUID
    profesional_id: uuid.UUID
    sillon_id: uuid.UUID
    prestacion_id: uuid.UUID
    paciente_id: uuid.UUID
    inicio: datetime
    fin: datetime
    estado: str
    cancelled_at: datetime | None = None
    token_cancelacion: str

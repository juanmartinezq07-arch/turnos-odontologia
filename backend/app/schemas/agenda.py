"""Schemas Pydantic v2 para consulta de agenda diaria (C-27, extra='forbid')."""
from datetime import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class AgendaPrestacionOut(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: uuid.UUID
    nombre: str
    duracion_min: int


class AgendaSillonOut(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: uuid.UUID
    nombre: str


class AgendaPacienteOut(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: uuid.UUID
    nombre: str
    telefono: str | None = None
    email: str | None = None


class AgendaTurnoOut(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: uuid.UUID
    profesional_id: uuid.UUID
    inicio: datetime
    fin: datetime
    estado: str
    prestacion: AgendaPrestacionOut
    sillon: AgendaSillonOut
    paciente: AgendaPacienteOut

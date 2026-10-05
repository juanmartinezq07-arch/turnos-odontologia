"""Schemas Pydantic v2 estrictos: extra='forbid', el cliente manda inicio NUNCA fin."""
import uuid
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, model_validator


class _Estricto(BaseModel):
    model_config = ConfigDict(extra="forbid")


class PacienteIn(_Estricto):
    nombre: str
    telefono: str | None = None
    email: str | None = None

    @model_validator(mode="after")
    def contacto_minimo(self):
        if not self.telefono and not self.email:
            raise ValueError("se requiere telefono o email")
        return self


class TurnoCreate(_Estricto):
    profesional_id: uuid.UUID
    sillon_id: uuid.UUID
    prestacion_id: uuid.UUID
    inicio: datetime
    paciente: PacienteIn


class ReservaCreate(_Estricto):
    profesional_id: uuid.UUID
    prestacion_id: uuid.UUID
    inicio: datetime
    sillon_id: uuid.UUID | None = None
    paciente: PacienteIn


class ReprogramarIn(_Estricto):
    nuevo_inicio: datetime


class TurnoOut(BaseModel):
    id: uuid.UUID
    profesional_id: uuid.UUID
    sillon_id: uuid.UUID
    prestacion_id: uuid.UUID
    paciente_id: uuid.UUID
    inicio: datetime
    fin: datetime
    estado: str
    token_cancelacion: str | None = None


class ReservaOut(TurnoOut):
    token_cancelacion: str


class DisponibilidadOut(BaseModel):
    profesional_id: uuid.UUID
    fecha: date
    prestacion_id: uuid.UUID
    slots: list[datetime]


class TurnoAgendaOut(BaseModel):
    id: uuid.UUID
    inicio: datetime
    fin: datetime
    estado: str
    prestacion: str
    duracion_min: int
    sillon: str
    paciente: str


class AgendaOut(BaseModel):
    profesional_id: uuid.UUID
    fecha: date
    turnos: list[TurnoAgendaOut]


class CatalogoOut(BaseModel):
    id: uuid.UUID
    nombre: str


class PrestacionOut(CatalogoOut):
    duracion_min: int


class ErrorOut(BaseModel):
    code: str
    message: str

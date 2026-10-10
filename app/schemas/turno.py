"""Schemas Pydantic v2 estrictos: extra='forbid', el cliente manda inicio NUNCA fin."""
import uuid
from datetime import datetime

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


class TurnoOut(BaseModel):
    id: uuid.UUID
    profesional_id: uuid.UUID
    sillon_id: uuid.UUID
    prestacion_id: uuid.UUID
    paciente_id: uuid.UUID
    inicio: datetime
    fin: datetime
    estado: str


class ErrorOut(BaseModel):
    code: str
    message: str

"""Schemas Pydantic v2 estrictos para catálogos públicos (C-24)."""
import uuid

from pydantic import BaseModel, ConfigDict


class _CatalogoBase(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


class ProfesionalOut(_CatalogoBase):
    id: uuid.UUID
    nombre: str
    apellido: str
    matricula: str | None = None


class SillonOut(_CatalogoBase):
    id: uuid.UUID
    nombre: str


class PrestacionOut(_CatalogoBase):
    id: uuid.UUID
    nombre: str
    duracion_min: int

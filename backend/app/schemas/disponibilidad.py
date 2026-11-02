"""Schemas Pydantic v2 estrictos para disponibilidad (C-25)."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SlotDisponibilidadOut(BaseModel):
    model_config = ConfigDict(extra="forbid")

    inicio: datetime
    fin: datetime

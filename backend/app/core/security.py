"""Auth minima por API key de recepcionista (alcance C-01)."""
from fastapi import Header, HTTPException

from app.core import config as cfg


async def require_recepcion(x_api_key: str | None = Header(default=None)) -> None:
    esperada = cfg.get_api_key_recepcion()
    if not esperada or x_api_key != esperada:
        raise HTTPException(status_code=401, detail="API key de recepcion invalida")


async def require_odontologo(x_api_key: str | None = Header(default=None)) -> None:
    esperada = cfg.get_api_key_odontologo()
    if not esperada or x_api_key != esperada:
        raise HTTPException(status_code=401, detail="API key de odontologo invalida")

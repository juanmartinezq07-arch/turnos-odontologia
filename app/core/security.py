"""Auth minima por API keys (task 1.3).

- Recepcionista: header X-API-Key == API_KEY_RECEPCION.
- Odontologo: identidad resuelta por ODONTOLOGO_KEYS (profesional_id -> key);
  con API_KEY_ODONTOLOGO generica la identidad se declara por test-override.
- Guest: sin auth en GET /disponibilidad, POST /reservas y cancelacion por token.
"""
from fastapi import Depends, Header, HTTPException

from app.core import config as cfg


async def require_recepcion(x_api_key: str | None = Header(default=None)) -> None:
    esperada = cfg.get_api_key_recepcion()
    if not esperada or x_api_key != esperada:
        raise HTTPException(status_code=401, detail="API key de recepcion invalida")


async def get_current_odontologo(
    x_api_key: str | None = Header(default=None),
) -> str | None:
    """Devuelve el profesional_id autenticado o None (generica sin identidad)."""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Falta API key de odontologo")
    mapa = cfg.get_odontologo_keys()
    for prof_id, key in mapa.items():
        if x_api_key == key:
            return prof_id
    if x_api_key == cfg.get_api_key_odontologo() and cfg.get_api_key_odontologo():
        return None
    raise HTTPException(status_code=401, detail="API key de odontologo invalida")


async def require_odontologo_agenda(
    profesional_id: str,
    actual: str | None = Depends(get_current_odontologo),
) -> None:
    """El odontologo solo lee su propia agenda (403 ajena)."""
    if actual is not None and actual != profesional_id:
        raise HTTPException(status_code=403, detail="Solo puede leer su propia agenda")

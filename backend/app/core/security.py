"""Auth minima por API key de recepcionista y odontologo (alcance C-01 / C-27)."""
import uuid

from fastapi import Header, HTTPException, Query

from app.core import config as cfg


async def require_recepcion(x_api_key: str | None = Header(default=None)) -> None:
    esperada = cfg.get_api_key_recepcion()
    if not esperada or x_api_key != esperada:
        raise HTTPException(status_code=401, detail="API key de recepcion invalida")


async def require_odontologo(
    profesional_id: uuid.UUID = Query(...),
    x_api_key: str | None = Header(default=None),
    x_profesional_id: str | None = Header(default=None),
) -> None:
    """Autoriza lectura de agenda: recepcionista global o odontologo solo propia (403 ajena)."""
    key_recepcion = cfg.get_api_key_recepcion()
    key_odontologo = cfg.get_api_key_odontologo()

    if key_recepcion and x_api_key == key_recepcion:
        return

    if key_odontologo and x_api_key == key_odontologo:
        try:
            prof_header = uuid.UUID(x_profesional_id) if x_profesional_id else None
        except ValueError:
            prof_header = None
        if prof_header != profesional_id:
            raise HTTPException(
                status_code=403,
                detail={
                    "code": "AGENDA_AJENA",
                    "message": "El odontologo solo puede consultar su propia agenda",
                },
            )
        return

    raise HTTPException(status_code=401, detail="API key de odontologo invalida")

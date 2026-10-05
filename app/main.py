"""Factory FastAPI: solo cableado (routers + handlers). Sin logica de dominio."""
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1 import agenda, catalogos, disponibilidad, reservas, turnos
from app.api.v1.reservas import RateLimited
from app.core.errors import DomainConflict, NotFound


def _error(code: str, message: str, status: int) -> JSONResponse:
    return JSONResponse(status_code=status, content={"code": code, "message": message})


def create_app() -> FastAPI:
    app = FastAPI(title="TurnosAR MVP", version="0.1.0")

    @app.exception_handler(DomainConflict)
    async def _conflicto(_: Request, exc: DomainConflict):
        return _error(exc.code, exc.message, 409)

    @app.exception_handler(NotFound)
    async def _no_encontrado(_: Request, exc: NotFound):
        return _error(exc.code, exc.message, 404)

    @app.exception_handler(RateLimited)
    async def _rate_limit(_: Request, __: RateLimited):
        return _error("RATE_LIMIT", "Excedio el limite de reservas por minuto", 429)

    @app.exception_handler(RequestValidationError)
    async def _validacion(_: Request, exc: RequestValidationError):
        return _error("VALIDACION", str(exc.errors()), 422)

    @app.exception_handler(HTTPException)
    async def _http(_: Request, exc: HTTPException):
        code = {401: "NO_AUTORIZADO", 403: "PROHIBIDO", 404: "NO_ENCONTRADO"}.get(
            exc.status_code, "ERROR_HTTP"
        )
        return _error(code, str(exc.detail), exc.status_code)

    app.include_router(turnos.router, tags=["turnos"])
    app.include_router(reservas.router, tags=["reservas"])
    app.include_router(disponibilidad.router, tags=["disponibilidad"])
    app.include_router(agenda.router, tags=["agenda"])
    app.include_router(catalogos.router, tags=["catalogos"])
    return app


app = create_app()

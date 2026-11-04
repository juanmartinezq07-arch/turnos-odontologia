"""Rate limiter en memoria simple por IP/clave (C-29)."""
import time
from collections import defaultdict
from fastapi import Request
from app.core.errors import DomainConflict

# Estructura en memoria: clave -> lista de timestamps (segundos)
_historial = defaultdict(list)
LIMITE_POR_MINUTO = 10
VENTANA_SEGUNDOS = 60.0


def check_rate_limit(request: Request) -> None:
    client_ip = request.client.host if request.client else "127.0.0.1"
    ahora = time.time()
    timestamps = _historial[client_ip]

    # Limpiar timestamps viejos fuera de la ventana
    _historial[client_ip] = [ts for ts in timestamps if ahora - ts < VENTANA_SEGUNDOS]

    if len(_historial[client_ip]) >= LIMITE_POR_MINUTO:
        raise DomainConflict(
            code="RATE_LIMIT_EXCEEDED",
            message=f"Se superó el límite de {LIMITE_POR_MINUTO} solicitudes por minuto",
            status=429,
        )

    _historial[client_ip].append(ahora)


def reset_rate_limit() -> None:
    """Utilidad para tests."""
    _historial.clear()

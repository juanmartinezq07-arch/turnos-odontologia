"""Configuracion solo por variables de entorno (task 1.3)."""
import os

DEFAULT_DATABASE_URL = "postgresql+psycopg://turnos:turnos@localhost:5432/turnos"
DEFAULT_TZ = "America/Argentina/Buenos_Aires"


def get_database_url() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)


def get_tz_consultorio() -> str:
    return os.environ.get("TZ_CONSULTORIO", DEFAULT_TZ)


def get_notif_backend() -> str:
    return os.environ.get("NOTIF_BACKEND", "mock")


def get_api_key_recepcion() -> str:
    return os.environ.get("API_KEY_RECEPCION", "")


def get_api_key_odontologo() -> str:
    return os.environ.get("API_KEY_ODONTOLOGO", "")


def get_odontologo_keys() -> dict[str, str]:
    """Mapa profesional_id -> api key desde ODONTOLOGO_KEYS="uuid:key,uuid:key".

    Permite que cada odontologo lea solo su agenda (403 ajena). Si esta vacio,
    se usa API_KEY_ODONTOLOGO como llave generica (demo de un profesional).
    """
    crudo = os.environ.get("ODONTOLOGO_KEYS", "").strip()
    mapa: dict[str, str] = {}
    if crudo:
        for par in crudo.split(","):
            if ":" in par:
                prof_id, key = par.split(":", 1)
                if prof_id.strip() and key.strip():
                    mapa[prof_id.strip()] = key.strip()
    return mapa


def get_reserva_rate_limit() -> tuple[int, int]:
    """Ventana del rate-limit publico. Formato 'N/minute' o 'N/second'."""
    crudo = os.environ.get("RESERVA_RATE_LIMIT", "10/minute")
    try:
        cantidad_s, ventana_s = crudo.split("/", 1)
        cantidad = int(cantidad_s)
        segundos = 60 if ventana_s.strip() == "minute" else 1
        return cantidad, segundos
    except ValueError:
        return 10, 60

"""Configuracion solo por variables de entorno (alcance C-01)."""
import os

DEFAULT_DATABASE_URL = "postgresql+psycopg://turnos:turnos@localhost:5432/turnos"
DEFAULT_TZ = "America/Argentina/Buenos_Aires"


def get_database_url() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)


def get_tz_consultorio() -> str:
    return os.environ.get("TZ_CONSULTORIO", DEFAULT_TZ)


def get_api_key_recepcion() -> str:
    return os.environ.get("API_KEY_RECEPCION", "")

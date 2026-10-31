"""Configuracion solo por variables de entorno (alcance C-01)."""
import os
from pathlib import Path

from dotenv import load_dotenv

# Carga backend/.env si existe. Nunca pisa variables ya exportadas en la
# shell (override=False): lo exportado siempre gana. El .env real no se
# commitea (ver .gitignore); la plantilla es backend/.env.example.
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

DEFAULT_DATABASE_URL = "postgresql+psycopg://turnos:turnos@localhost:5432/turnos"
DEFAULT_TZ = "America/Argentina/Buenos_Aires"


def get_database_url() -> str:
    return os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL)


def get_tz_consultorio() -> str:
    return os.environ.get("TZ_CONSULTORIO", DEFAULT_TZ)


def get_api_key_recepcion() -> str:
    return os.environ.get("API_KEY_RECEPCION", "")


def get_api_key_odontologo() -> str:
    return os.environ.get("API_KEY_ODONTOLOGO", "")

"""Reglas de negocio puras RN01/RN03 (soporte del alta).

Sin FastAPI ni DB: funciones deterministas testeables en aislamiento.
Todo datetime es timezone-aware (America/Argentina/Buenos_Aires).
"""
from datetime import datetime, time, timedelta


def calcular_fin(inicio: datetime, duracion_min: int) -> datetime:
    """RN01: fin = inicio + duracion de la prestacion."""
    if duracion_min <= 0:
        raise ValueError("duracion_min debe ser > 0")
    return inicio + timedelta(minutes=duracion_min)


def esta_en_pasado(inicio: datetime, ahora: datetime) -> bool:
    """RN03: True si el inicio es estrictamente anterior a ahora."""
    return inicio < ahora


def dentro_de_horario(
    inicio: datetime, fin: datetime, bloques: list[tuple[time, time]]
) -> bool:
    """RN03: True si [inicio, fin) cabe completo dentro de algun bloque del dia.

    Compara horas de reloj naive: los bloques de HorarioAtencion son Time
    sin zona y los datetimes llegan en TZ_CONSULTORIO, asi que se normaliza
    todo a naive para no mezclar aware/naive nunca.
    """
    if not bloques:
        return False
    hi, hf = inicio.timetz(), fin.timetz()
    if hi.tzinfo is not None:
        hi = hi.replace(tzinfo=None)
    if hf.tzinfo is not None:
        hf = hf.replace(tzinfo=None)
    return any(hi >= desde and hf <= hasta for desde, hasta in bloques)

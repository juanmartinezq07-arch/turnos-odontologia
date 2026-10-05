"""Reglas de negocio puras RN01/RN03/RN04/RN05.

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
    """RN03: True si [inicio, fin) cabe completo dentro de algun bloque del dia."""
    if not bloques:
        return False
    hi, hf = inicio.timetz(), fin.timetz()
    return any(hi >= desde and hf <= hasta for desde, hasta in bloques)


def puede_cancelar(estado: str) -> bool:
    """RN04: solo un turno activo puede cancelarse (idempotencia)."""
    return estado == "activo"


def normalizar_contacto(telefono: str | None, email: str | None) -> str:
    """RN05: clave de identidad del paciente guest (telefono o email normalizado)."""
    if telefono:
        digitos = "".join(c for c in telefono if c.isdigit())
        if digitos:
            return f"tel:{digitos}"
    if email:
        limpio = email.strip().lower()
        if limpio:
            return f"mail:{limpio}"
    raise ValueError("se requiere telefono o email")

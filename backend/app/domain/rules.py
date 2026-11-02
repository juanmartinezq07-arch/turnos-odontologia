"""Reglas de negocio puras RN01/RN03 y cálculo de disponibilidad (US-002).

Sin FastAPI ni DB: funciones deterministas testeables en aislamiento.
Todo datetime es timezone-aware (America/Argentina/Buenos_Aires).
"""
from datetime import date, datetime, time, timedelta
from zoneinfo import ZoneInfo


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


def calcular_slots_disponibles(
    fecha: date,
    bloques: list[tuple[time, time]],
    ocupados: list[tuple[datetime, datetime]],
    duracion_min: int,
    ahora: datetime,
    tz: ZoneInfo,
) -> list[tuple[datetime, datetime]]:
    """US-002: función pura y determinista de slots disponibles [inicio, fin).

    - RN01: fin = inicio + duracion_min.
    - RN02: excluye solapamientos (inicio < t_fin and fin > t_inicio) con
      semántica semiabierta [) (el borde inicio == t_fin es válido).
    - RN03: [inicio, fin) debe caber completo en el bloque y no estar en pasado.
    """
    if duracion_min <= 0 or not bloques:
        return []

    bloques_ordenados = sorted(set(bloques), key=lambda b: (b[0], b[1]))
    ocupados_norm = sorted(
        [(ini.astimezone(tz), fin.astimezone(tz)) for ini, fin in ocupados],
        key=lambda r: (r[0], r[1]),
    )
    ahora_tz = ahora.astimezone(tz)
    slots: list[tuple[datetime, datetime]] = []

    for hora_desde, hora_hasta in bloques_ordenados:
        bloque_inicio = datetime(
            fecha.year,
            fecha.month,
            fecha.day,
            hora_desde.hour,
            hora_desde.minute,
            hora_desde.second,
            tzinfo=tz,
        )
        bloque_fin = datetime(
            fecha.year,
            fecha.month,
            fecha.day,
            hora_hasta.hour,
            hora_hasta.minute,
            hora_hasta.second,
            tzinfo=tz,
        )
        cursor = bloque_inicio
        while True:
            fin_candidato = calcular_fin(cursor, duracion_min)
            if fin_candidato > bloque_fin:
                break

            # Si el candidato choca con algún intervalo ocupado [t_ini, t_fin),
            # saltar al fin del intervalo ocupado (semántica [): borde que se toca vale).
            choques = [
                t_fin
                for t_ini, t_fin in ocupados_norm
                if cursor < t_fin and fin_candidato > t_ini
            ]
            if choques:
                cursor = max(choques)
                continue

            if not esta_en_pasado(cursor, ahora_tz):
                slots.append((cursor, fin_candidato))
            cursor = fin_candidato

    return slots

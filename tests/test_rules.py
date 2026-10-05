"""Tests puros RN01/RN03 (task 3.1 RED). Sin DB ni FastAPI."""
from datetime import datetime, time
from zoneinfo import ZoneInfo

from app.domain.rules import (
    calcular_fin,
    dentro_de_horario,
    esta_en_pasado,
    normalizar_contacto,
    puede_cancelar,
)

TZ = ZoneInfo("America/Argentina/Buenos_Aires")


def _dt(y, mo, d, h, mi):
    return datetime(y, mo, d, h, mi, tzinfo=TZ)


def test_rn01_calcula_fin_30_min():
    inicio = _dt(2030, 5, 6, 10, 0)
    assert calcular_fin(inicio, 30) == _dt(2030, 5, 6, 10, 30)


def test_rn01_calcula_fin_90_min_cruza_hora():
    inicio = _dt(2030, 5, 6, 10, 45)
    assert calcular_fin(inicio, 90) == _dt(2030, 5, 6, 12, 15)


def test_rn03_pasado_rechaza_inicio_anterior_a_ahora():
    ahora = _dt(2030, 5, 6, 10, 0)
    assert esta_en_pasado(_dt(2030, 5, 6, 9, 59), ahora) is True


def test_rn03_borde_ahora_no_es_pasado():
    ahora = _dt(2030, 5, 6, 10, 0)
    assert esta_en_pasado(_dt(2030, 5, 6, 10, 0), ahora) is False


def test_rn03_futuro_no_es_pasado():
    ahora = _dt(2030, 5, 6, 10, 0)
    assert esta_en_pasado(_dt(2030, 5, 6, 10, 30), ahora) is False


def test_rn03_dentro_de_horario_lun_9_18():
    bloques = [(time(9, 0), time(18, 0))]
    assert dentro_de_horario(_dt(2030, 5, 6, 10, 0), _dt(2030, 5, 6, 10, 30), bloques) is True


def test_rn03_fuera_de_horario_domingo_sin_bloques():
    assert dentro_de_horario(_dt(2030, 5, 5, 10, 0), _dt(2030, 5, 5, 10, 30), []) is False


def test_rn03_turno_que_excede_cierre_rechazado():
    bloques = [(time(9, 0), time(18, 0))]
    assert dentro_de_horario(_dt(2030, 5, 6, 17, 45), _dt(2030, 5, 6, 18, 15), bloques) is False


def test_rn04_solo_activo_puede_cancelarse():
    assert puede_cancelar("activo") is True
    assert puede_cancelar("cancelado") is False


def test_rn05_normaliza_telefono_con_formato():
    assert normalizar_contacto("11-0000-0001", None) == normalizar_contacto("1100000001", None)


def test_rn05_email_case_insensitive():
    assert normalizar_contacto(None, "Juan@Example.com") == "mail:juan@example.com"

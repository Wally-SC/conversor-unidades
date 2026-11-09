import pytest

from conversor import UnidadeInvalida, converter, unidades_disponiveis
from conversor.cli import main


@pytest.mark.parametrize(
    "valor, origem, destino, esperado",
    [
        (1, "km", "m", 1000),
        (250, "cm", "m", 2.5),
        (1, "milha", "km", 1.609344),
        (1, "pol", "cm", 2.54),
        (1, "kg", "g", 1000),
        (1, "lb", "kg", 0.45359237),
        (1500, "ml", "l", 1.5),
        (100, "c", "f", 212),
        (32, "f", "c", 0),
        (0, "c", "k", 273.15),
        (300, "k", "c", 26.85),
    ],
)
def test_conversoes(valor, origem, destino, esperado):
    assert converter(valor, origem, destino) == pytest.approx(esperado)


def test_case_insensitive():
    assert converter(1, "KM", "M") == pytest.approx(1000)


def test_ida_e_volta():
    for origem, destino in [("km", "milha"), ("kg", "lb"), ("c", "f"), ("l", "galao")]:
        assert converter(converter(7.3, origem, destino), destino, origem) == pytest.approx(7.3)


def test_grandezas_incompativeis():
    with pytest.raises(UnidadeInvalida):
        converter(1, "kg", "m")


def test_unidade_desconhecida():
    with pytest.raises(UnidadeInvalida):
        converter(1, "parsec", "m")


def test_zero_absoluto():
    with pytest.raises(UnidadeInvalida):
        converter(-300, "c", "k")


def test_listagem():
    disponiveis = unidades_disponiveis()
    assert set(disponiveis) == {"comprimento", "massa", "volume", "temperatura"}


def test_cli(capsys):
    assert main(["1", "km", "m"]) == 0
    assert "1 km = 1000 m" in capsys.readouterr().out
    assert main(["1", "kg", "m"]) == 1

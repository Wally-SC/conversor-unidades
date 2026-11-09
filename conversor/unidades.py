"""Conversão de unidades de comprimento, massa, volume e temperatura."""

from __future__ import annotations

# Fatores para a unidade-base de cada grandeza.
# comprimento -> metro | massa -> grama | volume -> litro
_FATORES: dict[str, dict[str, float]] = {
    "comprimento": {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0,
        "pol": 0.0254,
        "pe": 0.3048,
        "milha": 1609.344,
    },
    "massa": {
        "mg": 0.001,
        "g": 1.0,
        "kg": 1000.0,
        "t": 1_000_000.0,
        "oz": 28.349523125,
        "lb": 453.59237,
    },
    "volume": {
        "ml": 0.001,
        "l": 1.0,
        "m3": 1000.0,
        "galao": 3.785411784,
        "xicara": 0.24,
    },
}

_TEMPERATURAS = {"c", "f", "k"}


class UnidadeInvalida(ValueError):
    """Unidade desconhecida ou conversão entre grandezas diferentes."""


def grandeza_de(unidade: str) -> str:
    unidade = unidade.lower()
    if unidade in _TEMPERATURAS:
        return "temperatura"
    for grandeza, tabela in _FATORES.items():
        if unidade in tabela:
            return grandeza
    raise UnidadeInvalida(f"unidade desconhecida: {unidade!r}")


def _converter_temperatura(valor: float, origem: str, destino: str) -> float:
    if origem == "c":
        celsius = valor
    elif origem == "f":
        celsius = (valor - 32) * 5 / 9
    else:  # kelvin
        celsius = valor - 273.15

    if celsius < -273.15 - 1e-9:
        raise UnidadeInvalida("temperatura abaixo do zero absoluto")

    if destino == "c":
        return celsius
    if destino == "f":
        return celsius * 9 / 5 + 32
    return celsius + 273.15


def converter(valor: float, origem: str, destino: str) -> float:
    """Converte ``valor`` de ``origem`` para ``destino``.

    >>> round(converter(1, "km", "m"), 6)
    1000.0
    >>> round(converter(100, "c", "f"), 6)
    212.0
    """
    origem, destino = origem.lower(), destino.lower()
    g_origem, g_destino = grandeza_de(origem), grandeza_de(destino)
    if g_origem != g_destino:
        raise UnidadeInvalida(f"não é possível converter {g_origem} ({origem}) para {g_destino} ({destino})")

    if g_origem == "temperatura":
        return _converter_temperatura(valor, origem, destino)

    tabela = _FATORES[g_origem]
    return valor * tabela[origem] / tabela[destino]


def unidades_disponiveis() -> dict[str, list[str]]:
    disponiveis = {g: sorted(t) for g, t in _FATORES.items()}
    disponiveis["temperatura"] = sorted(_TEMPERATURAS)
    return disponiveis

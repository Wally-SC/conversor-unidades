# conversor-unidades

Conversor de unidades de **comprimento**, **massa**, **volume** e **temperatura**.

## Uso

```bash
python -m conversor 10 km milha
python -m conversor 100 c f
python -m conversor --listar
```

Como biblioteca:

```python
from conversor import converter

converter(1, "km", "m")     # 1000.0
converter(100, "c", "f")    # 212.0
```

## Como funciona

Cada grandeza tem uma tabela de fatores para uma unidade-base (metro, grama,
litro). Converter `A -> B` vira `valor * fator[A] / fator[B]`, então adicionar uma
unidade nova é só acrescentar uma linha na tabela. As escalas de temperatura
têm origens diferentes (não bastam fatores multiplicativos), então usam fórmulas
próprias, passando por Celsius, e valores abaixo do zero absoluto são rejeitados.

Tentar converter grandezas diferentes (ex.: `kg` para `m`) levanta `UnidadeInvalida`.

## Testes

```bash
pip install pytest
pytest
```

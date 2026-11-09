from __future__ import annotations

import argparse
import sys

from conversor.unidades import UnidadeInvalida, converter, unidades_disponiveis


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="conversor", description="Conversor de unidades.")
    parser.add_argument("valor", nargs="?", type=float)
    parser.add_argument("origem", nargs="?")
    parser.add_argument("destino", nargs="?")
    parser.add_argument("--listar", action="store_true", help="mostra as unidades disponíveis")
    args = parser.parse_args(argv)

    if args.listar:
        for grandeza, unidades in unidades_disponiveis().items():
            print(f"{grandeza}: {', '.join(unidades)}")
        return 0

    if args.valor is None or args.origem is None or args.destino is None:
        parser.error("informe: valor origem destino (ex.: 10 km mi)")

    try:
        resultado = converter(args.valor, args.origem, args.destino)
    except UnidadeInvalida as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 1
    print(f"{args.valor:g} {args.origem} = {resultado:.6g} {args.destino}")
    return 0

"""Comandos do terminal: lê o que o usuário digitou e chama a função certa."""

import argparse

from app.gastos import (
    adicionar, alterar, apagar, converter_valor, listar, resumo,
)
from app.menu import menu


def ler_valor(texto):
    """Converte o valor para o argparse.

    Usa a função converter_valor. Se der erro, avisa o argparse,
    que mostra a mensagem e encerra o programa.
    """
    try:
        return converter_valor(texto)
    except ValueError as erro:
        raise argparse.ArgumentTypeError(str(erro))


def main(argumentos=None):
    """Monta os comandos do terminal e executa o que foi pedido.

    Sem argumentos, lê o que foi digitado no terminal.
    Os testes passam uma lista, como ["listar"].
    Se nenhum comando for digitado, abre o menu interativo.
    """
    parser = argparse.ArgumentParser(
        prog="python -m app",
        description="Controle de gastos. Sem comando, abre o menu.",
    )
    subcomandos = parser.add_subparsers(dest="comando")

    # Comando: adicionar
    parser_adicionar = subcomandos.add_parser(
        "adicionar", help="adiciona um gasto"
    )
    parser_adicionar.add_argument(
        "--descricao", required=True, help="o que foi comprado"
    )
    parser_adicionar.add_argument(
        "--valor", required=True, type=ler_valor,
        help="quanto custou, como 25.00",
    )

    # Comando: listar
    subcomandos.add_parser("listar", help="mostra todos os gastos")

    # Comando: alterar
    parser_alterar = subcomandos.add_parser(
        "alterar", help="muda a descrição e/ou o valor de um gasto"
    )
    parser_alterar.add_argument(
        "--id", required=True, type=int,
        help="número do gasto, mostrado no comando listar",
    )
    parser_alterar.add_argument("--descricao", help="nova descrição")
    parser_alterar.add_argument(
        "--valor", type=ler_valor, help="novo valor, como 25.00"
    )

    # Comando: apagar
    parser_apagar = subcomandos.add_parser("apagar", help="apaga um gasto")
    parser_apagar.add_argument(
        "--id", required=True, type=int,
        help="número do gasto, mostrado no comando listar",
    )

    # Comando: resumo
    parser_resumo = subcomandos.add_parser(
        "resumo", help="mostra o total dos gastos"
    )
    parser_resumo.add_argument(
        "--mes", type=int, choices=range(1, 13), metavar="MES",
        help="número do mês, de 1 a 12 (soma só esse mês do ano atual)",
    )

    args = parser.parse_args(argumentos)

    if args.comando is None:
        menu()
    elif args.comando == "adicionar":
        adicionar(args.descricao, args.valor)
    elif args.comando == "listar":
        listar()
    elif args.comando == "alterar":
        if args.descricao is None and args.valor is None:
            parser_alterar.error("informe --descricao ou --valor")
        alterar(args.id, args.descricao, args.valor)
    elif args.comando == "apagar":
        apagar(args.id)
    elif args.comando == "resumo":
        resumo(args.mes)

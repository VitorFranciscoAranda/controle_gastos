"""Menu interativo: o usuário escolhe as opções por número."""

import os

from app.armazenamento import carregar_gastos
from app.gastos import (
    adicionar, alterar, apagar, converter_valor, listar, resumo,
)


def limpar_tela():
    """Apaga tudo que está escrito no terminal."""
    # No Windows o comando é "cls". No Linux e no Mac é "clear".
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def pausar():
    """Espera o usuário apertar Enter antes de voltar ao menu."""
    print()
    input("Pressione Enter para voltar ao menu...")


def mostrar_titulo(texto):
    """Mostra um título com uma linha em branco antes e outra depois."""
    print()
    print(f"=== {texto} ===")
    print()


def mostrar_opcoes():
    """Mostra na tela a lista de opções do menu."""
    mostrar_titulo("Controle de gastos")
    print("  1 - Adicionar gasto")
    print("  2 - Listar gastos")
    print("  3 - Alterar gasto")
    print("  4 - Apagar gasto")
    print("  5 - Resumo geral")
    print("  6 - Resumo de um mês")
    print("  0 - Sair")
    print()


def perguntar_texto(pergunta):
    """Pergunta um texto e repete até o usuário digitar alguma coisa."""
    while True:
        texto = input(pergunta).strip()
        if texto:
            return texto
        print("Digite alguma coisa.")


def perguntar_valor(pergunta):
    """Pergunta um valor em dinheiro e repete até ser válido."""
    while True:
        texto = input(pergunta).strip()
        try:
            return converter_valor(texto)
        except ValueError as erro:
            print(f"Valor inválido: {erro}.")


def perguntar_inteiro(pergunta):
    """Pergunta um número inteiro e repete até ser válido."""
    while True:
        texto = input(pergunta).strip()
        try:
            return int(texto)
        except ValueError:
            print("Digite um número inteiro.")


def opcao_adicionar():
    """Pergunta a descrição e o valor e adiciona o gasto."""
    descricao = perguntar_texto("Descrição: ")
    valor = perguntar_valor("Valor: ")
    print()
    adicionar(descricao, valor)


def opcao_alterar():
    """Mostra os gastos, pergunta o ID e o que mudar, e altera o gasto."""
    listar()
    if not carregar_gastos():
        return

    print()
    id_gasto = perguntar_inteiro("ID do gasto que quer alterar: ")

    # Enter sem digitar nada quer dizer "não mudar".
    descricao = input("Nova descrição (Enter para manter): ").strip()
    if not descricao:
        descricao = None

    valor = None
    while True:
        texto = input("Novo valor (Enter para manter): ").strip()
        if not texto:
            break
        try:
            valor = converter_valor(texto)
            break
        except ValueError as erro:
            print(f"Valor inválido: {erro}.")

    print()
    if descricao is None and valor is None:
        print("Nada foi alterado.")
        return

    alterar(id_gasto, descricao, valor)


def opcao_apagar():
    """Mostra os gastos, pergunta o ID, pede confirmação e apaga."""
    listar()
    if not carregar_gastos():
        return

    print()
    id_gasto = perguntar_inteiro("ID do gasto que quer apagar: ")
    confirmacao = input(f"Apagar o gasto {id_gasto}? (s/n): ").strip().lower()
    print()
    if confirmacao == "s":
        apagar(id_gasto)
    else:
        print("Nada foi apagado.")


def opcao_resumo_do_mes():
    """Pergunta o mês (1 a 12) e mostra o total desse mês."""
    while True:
        mes = perguntar_inteiro("Mês (1 a 12): ")
        if 1 <= mes <= 12:
            break
        print("O mês precisa ser de 1 a 12.")
    print()
    resumo(mes)


def menu():
    """Mostra o menu e executa as opções até o usuário escolher sair.

    A tela é limpa antes do menu e antes de cada opção.
    Depois de cada opção, espera um Enter para o usuário ler o resultado.
    """
    while True:
        limpar_tela()
        mostrar_opcoes()
        opcao = input("Escolha uma opção: ").strip()
        limpar_tela()

        if opcao == "0":
            print("Até logo!")
            break

        if opcao == "1":
            mostrar_titulo("Adicionar gasto")
            opcao_adicionar()
        elif opcao == "2":
            mostrar_titulo("Lista de gastos")
            listar()
        elif opcao == "3":
            mostrar_titulo("Alterar gasto")
            opcao_alterar()
        elif opcao == "4":
            mostrar_titulo("Apagar gasto")
            opcao_apagar()
        elif opcao == "5":
            mostrar_titulo("Resumo geral")
            resumo()
        elif opcao == "6":
            mostrar_titulo("Resumo de um mês")
            opcao_resumo_do_mes()
        else:
            print()
            print("Opção inválida. Digite um número do menu.")

        pausar()

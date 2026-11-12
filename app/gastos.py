"""Regras do programa: adicionar, listar, alterar, apagar e resumir gastos."""

from datetime import date
from decimal import Decimal, InvalidOperation

from app.armazenamento import carregar_gastos, salvar_gastos

# Nomes dos meses. A posição 0 fica vazia para janeiro ser a posição 1.
MESES = [
    "", "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
]


def converter_valor(texto):
    """Transforma o texto digitado em Decimal e confere se é válido.

    Aceita ponto ou vírgula (25.00 ou 25,00).
    Dá erro (ValueError) se não for número ou se for menor ou igual a zero.
    """
    try:
        valor = Decimal(texto.replace(",", "."))
    except InvalidOperation:
        raise ValueError("o valor precisa ser um número, como 25.00")
    if not valor.is_finite() or valor <= 0:
        raise ValueError("o valor precisa ser maior que zero")
    return valor


def formatar_valor(texto):
    """Devolve o valor no formato brasileiro, como R$ 25,00."""
    return "R$ " + texto.replace(".", ",")


def adicionar(descricao, valor):
    """Cria um gasto novo com a data de hoje e salva no arquivo."""
    gastos = carregar_gastos()

    # O novo ID é o ID do último gasto mais 1. Se não há gastos, começa em 1.
    novo_id = 1
    if gastos:
        novo_id = gastos[-1]["id"] + 1

    gasto = {
        "id": novo_id,
        "data": date.today().isoformat(),
        "descricao": descricao,
        "valor": f"{valor:.2f}",
    }
    gastos.append(gasto)
    salvar_gastos(gastos)

    print(f"Gasto adicionado (ID {novo_id})")


def listar():
    """Mostra todos os gastos salvos em forma de tabela."""
    gastos = carregar_gastos()

    if not gastos:
        print("Nenhum gasto cadastrado.")
        return

    # Cabeçalho da tabela. Os números definem a largura de cada coluna.
    print(f"{'ID':<4} {'Data':<10} {'Descrição':<25} {'Valor':>12}")

    for gasto in gastos:
        valor = formatar_valor(gasto["valor"])
        print(
            f"{gasto['id']:<4} {gasto['data']:<10} "
            f"{gasto['descricao']:<25} {valor:>12}"
        )


def alterar(id_gasto, descricao=None, valor=None):
    """Muda a descrição e/ou o valor do gasto com o ID informado.

    O que vier como None fica como estava.
    """
    gastos = carregar_gastos()

    for gasto in gastos:
        if gasto["id"] == id_gasto:
            if descricao is not None:
                gasto["descricao"] = descricao
            if valor is not None:
                gasto["valor"] = f"{valor:.2f}"
            salvar_gastos(gastos)
            print(f"Gasto alterado (ID {id_gasto})")
            return

    # Só chega aqui se o laço terminou sem achar o ID.
    print(f"Não existe gasto com o ID {id_gasto}.")


def apagar(id_gasto):
    """Remove o gasto com o ID informado e salva a lista sem ele."""
    gastos = carregar_gastos()

    for gasto in gastos:
        if gasto["id"] == id_gasto:
            gastos.remove(gasto)
            salvar_gastos(gastos)
            print(f"Gasto apagado (ID {id_gasto})")
            # Achou e apagou, então a função pode terminar aqui.
            return

    # Só chega aqui se o laço terminou sem achar o ID.
    print(f"Não existe gasto com o ID {id_gasto}.")


def resumo(mes=None):
    """Mostra o total dos gastos.

    Sem mês, soma todos os gastos.
    Com mês (1 a 12), soma só os gastos desse mês no ano atual.
    """
    gastos = carregar_gastos()
    ano_atual = date.today().year
    total = Decimal("0")

    for gasto in gastos:
        data = date.fromisoformat(gasto["data"])
        if mes is None:
            total += Decimal(gasto["valor"])
        elif data.month == mes and data.year == ano_atual:
            total += Decimal(gasto["valor"])

    valor = formatar_valor(f"{total:.2f}")
    if mes is None:
        print(f"Total geral: {valor}")
    else:
        print(f"Total de {MESES[mes]}: {valor}")

"""Testes do comando listar."""

import unittest
from decimal import Decimal

from app.gastos import adicionar, listar
from tests.base import TesteComArquivoTemporario


class TesteListar(TesteComArquivoTemporario):
    """Confere a função listar."""

    def test_lista_vazia_mostra_aviso(self):
        saida = self.capturar_saida(listar)
        self.assertIn("Nenhum gasto cadastrado.", saida)

    def test_mostra_o_cabecalho(self):
        self.capturar_saida(adicionar, "Almoço", Decimal("25.00"))
        saida = self.capturar_saida(listar)
        self.assertIn("Descrição", saida)
        self.assertIn("Valor", saida)

    def test_mostra_todos_os_gastos(self):
        self.capturar_saida(adicionar, "Almoço", Decimal("25.00"))
        self.capturar_saida(adicionar, "Ônibus", Decimal("4.5"))
        saida = self.capturar_saida(listar)
        self.assertIn("Almoço", saida)
        self.assertIn("Ônibus", saida)

    def test_mostra_o_valor_com_virgula(self):
        self.capturar_saida(adicionar, "Almoço", Decimal("25.00"))
        saida = self.capturar_saida(listar)
        self.assertIn("R$ 25,00", saida)


if __name__ == "__main__":
    unittest.main()

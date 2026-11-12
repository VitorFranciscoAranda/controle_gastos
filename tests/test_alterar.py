"""Testes da função alterar."""

import unittest
from decimal import Decimal

from app.armazenamento import carregar_gastos
from app.gastos import adicionar, alterar
from tests.base import TesteComArquivoTemporario


class TesteAlterar(TesteComArquivoTemporario):
    """Confere a função alterar."""

    def setUp(self):
        """Além do arquivo temporário, começa cada teste com 2 gastos."""
        super().setUp()
        self.capturar_saida(adicionar, "Almoço", Decimal("25.00"))
        self.capturar_saida(adicionar, "Ônibus", Decimal("4.5"))

    def test_altera_so_a_descricao(self):
        self.capturar_saida(alterar, 1, "Jantar")
        gasto = carregar_gastos()[0]
        self.assertEqual(gasto["descricao"], "Jantar")
        self.assertEqual(gasto["valor"], "25.00")

    def test_altera_so_o_valor(self):
        self.capturar_saida(alterar, 1, None, Decimal("30"))
        gasto = carregar_gastos()[0]
        self.assertEqual(gasto["descricao"], "Almoço")
        self.assertEqual(gasto["valor"], "30.00")

    def test_altera_descricao_e_valor(self):
        self.capturar_saida(alterar, 2, "Metrô", Decimal("5.2"))
        gasto = carregar_gastos()[1]
        self.assertEqual(gasto["descricao"], "Metrô")
        self.assertEqual(gasto["valor"], "5.20")

    def test_nao_muda_o_id_nem_a_data(self):
        antes = carregar_gastos()[0]
        self.capturar_saida(alterar, 1, "Jantar", Decimal("30"))
        depois = carregar_gastos()[0]
        self.assertEqual(depois["id"], antes["id"])
        self.assertEqual(depois["data"], antes["data"])

    def test_nao_muda_os_outros_gastos(self):
        antes = carregar_gastos()[1]
        self.capturar_saida(alterar, 1, "Jantar")
        self.assertEqual(carregar_gastos()[1], antes)

    def test_mostra_mensagem_de_confirmacao(self):
        saida = self.capturar_saida(alterar, 1, "Jantar")
        self.assertIn("Gasto alterado (ID 1)", saida)

    def test_id_que_nao_existe_mostra_aviso(self):
        saida = self.capturar_saida(alterar, 99, "Jantar")
        self.assertIn("Não existe gasto com o ID 99.", saida)


if __name__ == "__main__":
    unittest.main()

"""Testes do comando apagar."""

import unittest
from decimal import Decimal

from app.armazenamento import carregar_gastos
from app.gastos import adicionar, apagar
from tests.base import TesteComArquivoTemporario


class TesteApagar(TesteComArquivoTemporario):
    """Confere a função apagar."""

    def setUp(self):
        """Além do arquivo temporário, começa cada teste com 3 gastos."""
        super().setUp()
        self.capturar_saida(adicionar, "Almoço", Decimal("25.00"))
        self.capturar_saida(adicionar, "Ônibus", Decimal("4.5"))
        self.capturar_saida(adicionar, "Aluguel", Decimal("1200"))

    def test_apaga_o_gasto_pedido(self):
        self.capturar_saida(apagar, 2)
        descricoes = [gasto["descricao"] for gasto in carregar_gastos()]
        self.assertNotIn("Ônibus", descricoes)

    def test_os_outros_gastos_mantem_o_id(self):
        self.capturar_saida(apagar, 2)
        ids = [gasto["id"] for gasto in carregar_gastos()]
        self.assertEqual(ids, [1, 3])

    def test_mostra_mensagem_de_confirmacao(self):
        saida = self.capturar_saida(apagar, 2)
        self.assertIn("Gasto apagado (ID 2)", saida)

    def test_id_que_nao_existe_mostra_aviso(self):
        saida = self.capturar_saida(apagar, 99)
        self.assertIn("Não existe gasto com o ID 99.", saida)

    def test_id_que_nao_existe_nao_apaga_nada(self):
        self.capturar_saida(apagar, 99)
        self.assertEqual(len(carregar_gastos()), 3)


if __name__ == "__main__":
    unittest.main()

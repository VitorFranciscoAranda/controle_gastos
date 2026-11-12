"""Testes do comando adicionar."""

import unittest
from datetime import date
from decimal import Decimal

from app.armazenamento import carregar_gastos
from app.gastos import adicionar, converter_valor
from tests.base import TesteComArquivoTemporario


class TesteConverterValor(unittest.TestCase):
    """Confere a função converter_valor, que valida o valor digitado."""

    def test_aceita_valor_com_ponto(self):
        self.assertEqual(converter_valor("25.00"), Decimal("25.00"))

    def test_aceita_valor_com_virgula(self):
        self.assertEqual(converter_valor("4,5"), Decimal("4.5"))

    def test_recusa_texto_que_nao_e_numero(self):
        with self.assertRaises(ValueError):
            converter_valor("abc")

    def test_recusa_zero(self):
        with self.assertRaises(ValueError):
            converter_valor("0")

    def test_recusa_valor_negativo(self):
        with self.assertRaises(ValueError):
            converter_valor("-3")


class TesteAdicionar(TesteComArquivoTemporario):
    """Confere a função adicionar."""

    def test_primeiro_gasto_tem_id_1(self):
        self.capturar_saida(adicionar, "Almoço", Decimal("25.00"))
        gastos = carregar_gastos()
        self.assertEqual(len(gastos), 1)
        self.assertEqual(gastos[0]["id"], 1)

    def test_segundo_gasto_tem_id_2(self):
        self.capturar_saida(adicionar, "Almoço", Decimal("25.00"))
        self.capturar_saida(adicionar, "Ônibus", Decimal("4.5"))
        gastos = carregar_gastos()
        self.assertEqual(gastos[1]["id"], 2)

    def test_salva_descricao_e_data_de_hoje(self):
        self.capturar_saida(adicionar, "Almoço", Decimal("25.00"))
        gasto = carregar_gastos()[0]
        self.assertEqual(gasto["descricao"], "Almoço")
        self.assertEqual(gasto["data"], date.today().isoformat())

    def test_salva_valor_com_duas_casas(self):
        self.capturar_saida(adicionar, "Ônibus", Decimal("4.5"))
        self.assertEqual(carregar_gastos()[0]["valor"], "4.50")

    def test_mostra_mensagem_com_o_id(self):
        saida = self.capturar_saida(adicionar, "Almoço", Decimal("25.00"))
        self.assertIn("Gasto adicionado (ID 1)", saida)


if __name__ == "__main__":
    unittest.main()

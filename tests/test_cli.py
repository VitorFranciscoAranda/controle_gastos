"""Testes do programa inteiro, como se fosse digitado no terminal."""

import argparse
import io
import unittest
from contextlib import redirect_stderr
from datetime import date
from decimal import Decimal
from unittest.mock import patch

from app.armazenamento import carregar_gastos
from app.cli import ler_valor, main
from app.gastos import MESES
from tests.base import TesteComArquivoTemporario


class TesteLerValor(unittest.TestCase):
    """Confere a função ler_valor, usada pelo argparse."""

    def test_devolve_o_valor_convertido(self):
        self.assertEqual(ler_valor("4,5"), Decimal("4.5"))

    def test_valor_invalido_vira_erro_do_argparse(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            ler_valor("abc")


class TesteLinhaDeComando(TesteComArquivoTemporario):
    """Confere a função main com os argumentos de cada comando."""

    def test_adicionar_salva_o_gasto(self):
        argumentos = ["adicionar", "--descricao", "Almoço", "--valor", "25"]
        saida = self.capturar_saida(main, argumentos)
        self.assertIn("Gasto adicionado (ID 1)", saida)
        self.assertEqual(carregar_gastos()[0]["valor"], "25.00")

    def test_listar_mostra_o_gasto_adicionado(self):
        self.capturar_saida(
            main, ["adicionar", "--descricao", "Almoço", "--valor", "25"]
        )
        saida = self.capturar_saida(main, ["listar"])
        self.assertIn("Almoço", saida)

    def test_alterar_muda_o_valor(self):
        self.capturar_saida(
            main, ["adicionar", "--descricao", "Almoço", "--valor", "25"]
        )
        self.capturar_saida(main, ["alterar", "--id", "1", "--valor", "30"])
        self.assertEqual(carregar_gastos()[0]["valor"], "30.00")

    def test_alterar_sem_dizer_o_que_mudar_encerra_com_erro(self):
        self.rodar_esperando_erro(["alterar", "--id", "1"])

    def test_apagar_remove_o_gasto(self):
        self.capturar_saida(
            main, ["adicionar", "--descricao", "Almoço", "--valor", "25"]
        )
        self.capturar_saida(main, ["apagar", "--id", "1"])
        self.assertEqual(carregar_gastos(), [])

    def test_resumo_mostra_o_total_geral(self):
        self.capturar_saida(
            main, ["adicionar", "--descricao", "Almoço", "--valor", "25"]
        )
        self.capturar_saida(
            main, ["adicionar", "--descricao", "Ônibus", "--valor", "4,5"]
        )
        saida = self.capturar_saida(main, ["resumo"])
        self.assertIn("Total geral: R$ 29,50", saida)

    def test_resumo_com_mes_mostra_o_total_do_mes(self):
        self.capturar_saida(
            main, ["adicionar", "--descricao", "Almoço", "--valor", "25"]
        )
        mes = date.today().month
        saida = self.capturar_saida(main, ["resumo", "--mes", str(mes)])
        self.assertIn(f"Total de {MESES[mes]}: R$ 25,00", saida)

    def rodar_esperando_erro(self, argumentos):
        """Roda o main e confere que o argparse encerrou com erro."""
        # O argparse escreve o erro em stderr. Guardamos para não sujar a tela.
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                main(argumentos)

    def test_valor_invalido_encerra_com_erro(self):
        self.rodar_esperando_erro(
            ["adicionar", "--descricao", "Almoço", "--valor", "abc"]
        )
        self.assertEqual(carregar_gastos(), [])

    def test_mes_fora_de_1_a_12_encerra_com_erro(self):
        self.rodar_esperando_erro(["resumo", "--mes", "13"])

    def test_id_que_nao_e_numero_encerra_com_erro(self):
        self.rodar_esperando_erro(["apagar", "--id", "abc"])

    def test_sem_comando_abre_o_menu(self):
        # O patch troca o input: em vez de esperar o teclado, devolve "0".
        with (
            patch("builtins.input", side_effect=["0"]),
            patch("app.menu.limpar_tela"),
        ):
            saida = self.capturar_saida(main, [])
        self.assertIn("=== Controle de gastos ===", saida)


if __name__ == "__main__":
    unittest.main()

"""Testes do menu interativo."""

import unittest
from datetime import date
from decimal import Decimal
from unittest.mock import patch

from app.armazenamento import carregar_gastos
from app.gastos import MESES, adicionar
from app.menu import limpar_tela, menu
from tests.base import TesteComArquivoTemporario


class TesteMenu(TesteComArquivoTemporario):
    """Confere o menu, fingindo o que o usuário digitaria."""

    def usar_menu(self, respostas):
        """Roda o menu com as respostas dadas e devolve o que apareceu.

        O patch troca o input: cada vez que o programa pergunta algo,
        ele recebe a próxima resposta da lista, sem esperar o teclado.
        Nos testes a tela não é limpa de verdade e a pausa não espera
        o Enter, para as respostas da lista serem só as das perguntas.
        """
        with (
            patch("builtins.input", side_effect=respostas),
            patch("app.menu.limpar_tela"),
            patch("app.menu.pausar"),
        ):
            return self.capturar_saida(menu)

    def test_opcao_0_sai_do_menu(self):
        saida = self.usar_menu(["0"])
        self.assertIn("Até logo!", saida)

    def test_opcao_invalida_mostra_aviso_e_continua(self):
        saida = self.usar_menu(["9", "0"])
        self.assertIn("Opção inválida", saida)
        self.assertIn("Até logo!", saida)

    def test_adicionar_salva_o_gasto(self):
        self.usar_menu(["1", "Almoço", "25,00", "0"])
        gasto = carregar_gastos()[0]
        self.assertEqual(gasto["descricao"], "Almoço")
        self.assertEqual(gasto["valor"], "25.00")

    def test_adicionar_pergunta_de_novo_se_o_valor_for_invalido(self):
        saida = self.usar_menu(["1", "Almoço", "abc", "25", "0"])
        self.assertIn("Valor inválido", saida)
        self.assertEqual(carregar_gastos()[0]["valor"], "25.00")

    def test_adicionar_pergunta_de_novo_se_a_descricao_for_vazia(self):
        self.usar_menu(["1", "", "Almoço", "25", "0"])
        self.assertEqual(carregar_gastos()[0]["descricao"], "Almoço")

    def test_listar_mostra_os_gastos(self):
        self.capturar_saida(adicionar, "Almoço", Decimal("25"))
        saida = self.usar_menu(["2", "0"])
        self.assertIn("Almoço", saida)

    def test_alterar_muda_descricao_e_valor(self):
        self.capturar_saida(adicionar, "Almoço", Decimal("25"))
        self.usar_menu(["3", "1", "Jantar", "30", "0"])
        gasto = carregar_gastos()[0]
        self.assertEqual(gasto["descricao"], "Jantar")
        self.assertEqual(gasto["valor"], "30.00")

    def test_alterar_com_enter_mantem_o_que_estava(self):
        self.capturar_saida(adicionar, "Almoço", Decimal("25"))
        self.usar_menu(["3", "1", "", "30", "0"])
        gasto = carregar_gastos()[0]
        self.assertEqual(gasto["descricao"], "Almoço")
        self.assertEqual(gasto["valor"], "30.00")

    def test_alterar_sem_mudar_nada_avisa(self):
        self.capturar_saida(adicionar, "Almoço", Decimal("25"))
        saida = self.usar_menu(["3", "1", "", "", "0"])
        self.assertIn("Nada foi alterado.", saida)

    def test_alterar_sem_gastos_volta_para_o_menu(self):
        saida = self.usar_menu(["3", "0"])
        self.assertIn("Nenhum gasto cadastrado.", saida)

    def test_apagar_com_confirmacao_apaga(self):
        self.capturar_saida(adicionar, "Almoço", Decimal("25"))
        self.usar_menu(["4", "1", "s", "0"])
        self.assertEqual(carregar_gastos(), [])

    def test_apagar_sem_confirmacao_nao_apaga(self):
        self.capturar_saida(adicionar, "Almoço", Decimal("25"))
        saida = self.usar_menu(["4", "1", "n", "0"])
        self.assertIn("Nada foi apagado.", saida)
        self.assertEqual(len(carregar_gastos()), 1)

    def test_apagar_pergunta_de_novo_se_o_id_nao_for_numero(self):
        self.capturar_saida(adicionar, "Almoço", Decimal("25"))
        saida = self.usar_menu(["4", "abc", "1", "s", "0"])
        self.assertIn("Digite um número inteiro.", saida)
        self.assertEqual(carregar_gastos(), [])

    def test_resumo_geral_mostra_o_total(self):
        self.capturar_saida(adicionar, "Almoço", Decimal("25"))
        saida = self.usar_menu(["5", "0"])
        self.assertIn("Total geral: R$ 25,00", saida)

    def test_resumo_do_mes_mostra_o_total_do_mes(self):
        self.capturar_saida(adicionar, "Almoço", Decimal("25"))
        mes = date.today().month
        saida = self.usar_menu(["6", str(mes), "0"])
        self.assertIn(f"Total de {MESES[mes]}: R$ 25,00", saida)

    def test_resumo_do_mes_pergunta_de_novo_se_o_mes_for_invalido(self):
        saida = self.usar_menu(["6", "13", "1", "0"])
        self.assertIn("O mês precisa ser de 1 a 12.", saida)
        self.assertIn("Total de janeiro", saida)


class TesteTelaDoMenu(TesteComArquivoTemporario):
    """Confere o limpar tela e a pausa do menu."""

    def test_limpar_tela_chama_o_comando_do_sistema(self):
        with patch("app.menu.os.system") as comando:
            limpar_tela()
        comando.assert_called_once()

    def test_menu_limpa_a_tela_antes_de_mostrar_as_opcoes(self):
        with (
            patch("builtins.input", side_effect=["0"]),
            patch("app.menu.limpar_tela") as limpar,
        ):
            self.capturar_saida(menu)
        self.assertTrue(limpar.called)

    def test_menu_pausa_depois_de_uma_opcao(self):
        # Respostas: opção 2, Enter da pausa e opção 0 para sair.
        with (
            patch("builtins.input", side_effect=["2", "", "0"]),
            patch("app.menu.limpar_tela"),
        ):
            saida = self.capturar_saida(menu)
        self.assertIn("Nenhum gasto cadastrado.", saida)
        self.assertIn("Até logo!", saida)

    def test_sair_nao_pede_enter(self):
        with (
            patch("builtins.input", side_effect=["0"]),
            patch("app.menu.limpar_tela"),
            patch("app.menu.pausar") as pausa,
        ):
            self.capturar_saida(menu)
        pausa.assert_not_called()


if __name__ == "__main__":
    unittest.main()

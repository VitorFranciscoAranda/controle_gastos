"""Testes do comando resumo."""

import unittest
from datetime import date

from app.armazenamento import salvar_gastos
from app.gastos import resumo
from tests.base import TesteComArquivoTemporario


class TesteResumo(TesteComArquivoTemporario):
    """Confere a função resumo."""

    def setUp(self):
        """Além do arquivo temporário, começa cada teste com 4 gastos.

        Três são do ano atual (dois em março, um em abril).
        Um é de março do ano passado.
        """
        super().setUp()
        ano = date.today().year
        salvar_gastos([
            {"id": 1, "data": f"{ano}-03-05", "descricao": "Almoço",
             "valor": "0.10"},
            {"id": 2, "data": f"{ano}-03-20", "descricao": "Ônibus",
             "valor": "0.20"},
            {"id": 3, "data": f"{ano}-04-01", "descricao": "Aluguel",
             "valor": "1200.00"},
            {"id": 4, "data": f"{ano - 1}-03-10", "descricao": "Antigo",
             "valor": "50.00"},
        ])

    def test_total_geral_soma_todos_os_gastos(self):
        saida = self.capturar_saida(resumo)
        self.assertIn("Total geral: R$ 1250,30", saida)

    def test_total_do_mes_soma_so_aquele_mes(self):
        saida = self.capturar_saida(resumo, 4)
        self.assertIn("Total de abril: R$ 1200,00", saida)

    def test_soma_com_decimal_nao_tem_erro_de_arredondamento(self):
        # Com float, 0.10 + 0.20 daria 0.30000000000000004.
        saida = self.capturar_saida(resumo, 3)
        self.assertIn("Total de março: R$ 0,30", saida)

    def test_total_do_mes_ignora_gastos_de_outro_ano(self):
        saida = self.capturar_saida(resumo, 3)
        self.assertNotIn("50", saida)

    def test_mes_sem_gastos_mostra_zero(self):
        saida = self.capturar_saida(resumo, 12)
        self.assertIn("Total de dezembro: R$ 0,00", saida)

    def test_sem_nenhum_gasto_mostra_zero(self):
        salvar_gastos([])
        saida = self.capturar_saida(resumo)
        self.assertIn("Total geral: R$ 0,00", saida)


if __name__ == "__main__":
    unittest.main()

"""Testes de ler e salvar o arquivo JSON."""

import unittest

from app import armazenamento
from app.armazenamento import carregar_gastos, salvar_gastos
from tests.base import TesteComArquivoTemporario


class TesteArmazenamento(TesteComArquivoTemporario):
    """Confere as funções carregar_gastos e salvar_gastos."""

    def test_carregar_sem_arquivo_devolve_lista_vazia(self):
        self.assertEqual(carregar_gastos(), [])

    def test_salvar_e_carregar_devolve_os_mesmos_gastos(self):
        gastos = [
            {
                "id": 1,
                "data": "2026-11-11",
                "descricao": "Almoço",
                "valor": "25.00",
            }
        ]
        salvar_gastos(gastos)
        self.assertEqual(carregar_gastos(), gastos)

    def test_salvar_cria_o_arquivo(self):
        salvar_gastos([])
        self.assertTrue(armazenamento.CAMINHO_ARQUIVO.exists())

    def test_acentos_ficam_legiveis_no_arquivo(self):
        salvar_gastos([{"id": 1, "descricao": "Pão de açúcar"}])
        texto = armazenamento.CAMINHO_ARQUIVO.read_text(encoding="utf-8")
        self.assertIn("Pão de açúcar", texto)


if __name__ == "__main__":
    unittest.main()

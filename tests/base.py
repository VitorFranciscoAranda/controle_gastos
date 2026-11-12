"""Código que todos os testes usam em comum."""

import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from app import armazenamento


class TesteComArquivoTemporario(unittest.TestCase):
    """Faz cada teste usar um arquivo de gastos temporário.

    Assim os testes nunca mexem no dados/gastos.json de verdade.
    """

    def setUp(self):
        """Roda antes de cada teste: troca o caminho do arquivo."""
        self.pasta_temporaria = tempfile.TemporaryDirectory()
        self.caminho_original = armazenamento.CAMINHO_ARQUIVO
        armazenamento.CAMINHO_ARQUIVO = (
            Path(self.pasta_temporaria.name) / "gastos.json"
        )

    def tearDown(self):
        """Roda depois de cada teste: desfaz a troca e apaga a pasta."""
        armazenamento.CAMINHO_ARQUIVO = self.caminho_original
        self.pasta_temporaria.cleanup()

    def capturar_saida(self, funcao, *argumentos):
        """Executa a função e devolve o texto que ela mostrou com print."""
        saida = io.StringIO()
        with redirect_stdout(saida):
            funcao(*argumentos)
        return saida.getvalue()

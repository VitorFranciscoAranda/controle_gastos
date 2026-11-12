"""Lê e salva os gastos no arquivo JSON."""

import json
from pathlib import Path

# Caminho do arquivo onde os gastos ficam salvos.
CAMINHO_ARQUIVO = Path("dados") / "gastos.json"


def carregar_gastos():
    """Devolve a lista de gastos salva no arquivo.

    Se o arquivo ainda não existe, devolve uma lista vazia.
    """
    if not CAMINHO_ARQUIVO.exists():
        return []
    with open(CAMINHO_ARQUIVO, encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_gastos(gastos):
    """Grava a lista de gastos no arquivo, criando a pasta se precisar."""
    CAMINHO_ARQUIVO.parent.mkdir(exist_ok=True)
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(gastos, arquivo, ensure_ascii=False, indent=2)

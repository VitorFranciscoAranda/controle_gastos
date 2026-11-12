# Controle de gastos

Programa de terminal para anotar gastos do dia a dia, feito em Python usando
só a biblioteca padrão.

Projeto de estudo baseado no desafio
[Expense Tracker](https://roadmap.sh/projects/expense-tracker) do roadmap.sh.

## O que ele faz

- Adiciona um gasto com descrição e valor.
- Lista todos os gastos em forma de tabela.
- Altera a descrição ou o valor de um gasto.
- Apaga um gasto pelo ID.
- Mostra o total geral ou o total de um mês.

Dá para usar de dois jeitos: por um menu interativo ou por comandos diretos.

Os gastos ficam salvos no arquivo `dados/gastos.json`.

## Requisitos

- Python 3.11 ou mais novo.
- Nenhuma biblioteca para instalar.

## Como baixar

```
git clone https://github.com/VitorFranciscoAranda/controle_gastos.git
cd controle_gastos
```

## Como usar pelo menu

Abra o terminal dentro da pasta do projeto e rode:

```
python -m app
```

```
=== Controle de gastos ===

  1 - Adicionar gasto
  2 - Listar gastos
  3 - Alterar gasto
  4 - Apagar gasto
  5 - Resumo geral
  6 - Resumo de um mês
  0 - Sair

Escolha uma opção:
```

Digite o número da opção e responda às perguntas. A tela é limpa a cada opção,
para mostrar uma coisa de cada vez. No Windows, também dá para
abrir o menu com dois cliques no arquivo `abrir-menu.bat`.

## Como usar por comandos

### Adicionar um gasto

```
python -m app adicionar --descricao "Almoço" --valor 25.00
```

```
Gasto adicionado (ID 1)
```

O valor aceita ponto ou vírgula (`25.00` ou `25,00`).

### Listar os gastos

```
python -m app listar
```

```
ID   Data       Descrição                        Valor
1    2026-11-11 Almoço                        R$ 25,00
2    2026-11-11 Ônibus                         R$ 4,50
```

### Alterar um gasto

Informe `--descricao`, `--valor` ou os dois:

```
python -m app alterar --id 1 --valor 30
```

```
Gasto alterado (ID 1)
```

### Apagar um gasto

```
python -m app apagar --id 2
```

```
Gasto apagado (ID 2)
```

### Ver o resumo

Total de todos os gastos:

```
python -m app resumo
```

```
Total geral: R$ 29,50
```

Total de um mês do ano atual (de 1 a 12):

```
python -m app resumo --mes 11
```

```
Total de novembro: R$ 29,50
```

### Ajuda

```
python -m app --help
python -m app adicionar --help
```

## Estrutura do projeto

```
controle_gastos/
├── app/
│   ├── __init__.py         # faz de "app" um pacote
│   ├── __main__.py         # ponto de entrada (python -m app)
│   ├── cli.py              # comandos do terminal (argparse)
│   ├── menu.py             # menu interativo
│   ├── gastos.py           # regras: adicionar, listar, alterar, apagar, resumo
│   └── armazenamento.py    # lê e salva o arquivo JSON
├── dados/                  # onde fica o gastos.json
├── tests/                  # testes automáticos
├── abrir-menu.bat          # abre o menu com dois cliques (Windows)
└── README.md
```

## Testes

O projeto tem 69 testes automáticos feitos com `unittest`. Para rodar:

```
python -m unittest
```

Os testes usam um arquivo temporário e não mexem nos gastos de verdade.

## O que eu pratiquei

- `argparse` com subcomandos, para ler os comandos do terminal.
- `Decimal` para dinheiro, evitando os erros de arredondamento do `float`.
- `json` para salvar e ler os dados.
- `pathlib` para montar caminhos que funcionam em qualquer sistema.
- `unittest` para os testes automáticos, com `mock` para simular o que o usuário digita.
- `input` e `while` para montar um menu interativo.
- Separar o código por responsabilidade: comandos, menu, regras e arquivo de dados ficam cada um no seu arquivo.

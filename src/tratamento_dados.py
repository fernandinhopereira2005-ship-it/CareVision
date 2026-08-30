# -*- coding: utf-8 -*-

# ============================================================
# CAREVISION
# PIPELINE DE TRATAMENTO, INTEGRAÇÃO E ANÁLISE DOS DADOS
# ============================================================

# Este script realiza todo o processamento utilizado
# para construção da base analítica final do CareVision.
#
# Fluxo geral:
#
# SIH/SUS -> internações
# CNES    -> leitos SUS
# IBGE    -> população
#
#              ↓
#
# limpeza e padronização
#
#              ↓
#
# integração das bases
#
#              ↓
#
# criação de indicadores
#
#              ↓
#
# Índice de Pressão Hospitalar
#
#              ↓
#
# carevision_base_final.csv


# ============================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================

# Pandas será utilizado para leitura, tratamento,
# integração e manipulação das bases.
import pandas as pd

# NumPy será utilizado como apoio para operações numéricas.
import numpy as np


# ============================================================
# 2. DEFINIÇÃO DOS CAMINHOS DAS BASES BRUTAS
# ============================================================

# As bases originais estão armazenadas dentro da pasta
# data/raw do repositório.

arquivo_sih = "data/raw/01_internacoes_sih.csv"

arquivo_cnes = "data/raw/02_leitos_cnes.csv"

arquivo_ibge = "data/raw/03_populacao_ibge.xlsx"


# ============================================================
# 3. TRATAMENTO DA BASE SIH/SUS
# ============================================================

# ------------------------------------------------------------
# 3.1 CARREGAMENTO DA BASE
# ------------------------------------------------------------

# Lê o arquivo exportado pelo DATASUS.
#
# sep=";" -> separador utilizado no arquivo.
# encoding="latin1" -> preserva caracteres acentuados.
# skiprows=3 -> ignora as linhas extras adicionadas pelo TABNET.
# engine="python" -> oferece maior flexibilidade na leitura.

sih = pd.read_csv(
    arquivo_sih,
    sep=";",
    encoding="latin1",
    skiprows=3,
    engine="python"
)


# ------------------------------------------------------------
# 3.2 FILTRO DAS 27 UNIDADES DA FEDERAÇÃO
# ------------------------------------------------------------

# Mantém somente linhas que começam com:
# dois números + espaço.
#
# Isso remove linhas de totalização e notas do DATASUS.

sih = sih[
    sih["Unidade da Federação"]
    .astype(str)
    .str.match(r"^\d{2}\s")
].copy()


# ------------------------------------------------------------
# 3.3 CÓDIGO E NOME DA UF
# ------------------------------------------------------------

# Extrai os dois primeiros caracteres como código da UF.
#
# Exemplo:
# "35 São Paulo" -> 35

sih["codigo_uf"] = (
    sih["Unidade da Federação"]
    .str[:2]
    .astype(int)
)

# Mantém somente o nome da UF.
#
# Exemplo:
# "35 São Paulo" -> "São Paulo"

sih["uf"] = (
    sih["Unidade da Federação"]
    .str[3:]
    .str.strip()
)


# ------------------------------------------------------------
# 3.4 IDENTIFICAÇÃO DAS COLUNAS MENSAIS
# ------------------------------------------------------------

# Os períodos estão no formato:
# "2025/Jun", "2025/Jul", etc.

colunas_meses = [
    coluna
    for coluna in sih.columns
    if "/" in coluna
]


# ------------------------------------------------------------
# 3.5 TRANSFORMAÇÃO DO FORMATO WIDE PARA LONG
# ------------------------------------------------------------

# Transforma as várias colunas mensais em registros.
#
# Estrutura final:
# codigo_uf | uf | periodo | internacoes

sih_long = sih.melt(
    id_vars=["codigo_uf", "uf"],
    value_vars=colunas_meses,
    var_name="periodo",
    value_name="internacoes"
)


# ------------------------------------------------------------
# 3.6 CONVERSÃO DAS INTERNAÇÕES PARA FORMATO NUMÉRICO
# ------------------------------------------------------------

# Valores inválidos são transformados em NaN
# em vez de provocar erro no processamento.

sih_long["internacoes"] = pd.to_numeric(
    sih_long["internacoes"],
    errors="coerce"
)


# ============================================================
# 4. PADRONIZAÇÃO TEMPORAL
# ============================================================

# Dicionário utilizado para converter
# abreviações dos meses para números.

meses = {
    "Jan": "01",
    "Fev": "02",
    "Mar": "03",
    "Abr": "04",
    "Mai": "05",
    "Jun": "06",
    "Jul": "07",
    "Ago": "08",
    "Set": "09",
    "Out": "10",
    "Nov": "11",
    "Dez": "12"
}


# Separa ano e mês.

sih_long[["ano", "mes"]] = (
    sih_long["periodo"]
    .str.split("/", expand=True)
)

# Converte o mês para número.

sih_long["mes_numero"] = (
    sih_long["mes"]
    .map(meses)
)

# Cria uma coluna de data utilizando
# o primeiro dia de cada mês.

sih_long["data"] = pd.to_datetime(
    sih_long["ano"]
    + "-"
    + sih_long["mes_numero"]
    + "-01"
)


# ============================================================
# 5. TRATAMENTO DA BASE CNES
# ============================================================

# ------------------------------------------------------------
# 5.1 CARREGAMENTO
# ------------------------------------------------------------

cnes = pd.read_csv(
    arquivo_cnes,
    sep=";",
    encoding="latin1",
    skiprows=3,
    engine="python"
)


# ------------------------------------------------------------
# 5.2 FILTRO DAS UFs
# ------------------------------------------------------------

cnes = cnes[
    cnes["Unidade da Federação"]
    .astype(str)
    .str.match(r"^\d{2}\s")
].copy()


# ------------------------------------------------------------
# 5.3 CÓDIGO E NOME DA UF
# ------------------------------------------------------------

cnes["codigo_uf"] = (
    cnes["Unidade da Federação"]
    .str[:2]
    .astype(int)
)

cnes["uf"] = (
    cnes["Unidade da Federação"]
    .str[3:]
    .str.strip()
)


# ------------------------------------------------------------
# 5.4 IDENTIFICAÇÃO DAS COLUNAS MENSAIS
# ------------------------------------------------------------

colunas_meses_cnes = [
    coluna
    for coluna in cnes.columns
    if "/" in coluna
]


# ------------------------------------------------------------
# 5.5 TRANSFORMAÇÃO PARA FORMATO LONGO
# ------------------------------------------------------------

cnes_long = cnes.melt(
    id_vars=["codigo_uf", "uf"],
    value_vars=colunas_meses_cnes,
    var_name="periodo",
    value_name="leitos_sus"
)


# ------------------------------------------------------------
# 5.6 CONVERSÃO PARA FORMATO NUMÉRICO
# ------------------------------------------------------------

cnes_long["leitos_sus"] = pd.to_numeric(
    cnes_long["leitos_sus"],
    errors="coerce"
)


# ------------------------------------------------------------
# 5.7 CRIAÇÃO DAS COLUNAS TEMPORAIS
# ------------------------------------------------------------

cnes_long[["ano", "mes"]] = (
    cnes_long["periodo"]
    .str.split("/", expand=True)
)

cnes_long["mes_numero"] = (
    cnes_long["mes"]
    .map(meses)
)

cnes_long["data"] = pd.to_datetime(
    cnes_long["ano"]
    + "-"
    + cnes_long["mes_numero"]
    + "-01"
)


# ============================================================
# 6. TRATAMENTO DA BASE POPULACIONAL DO IBGE
# ============================================================

# ------------------------------------------------------------
# 6.1 LEITURA DA PLANILHA
# ------------------------------------------------------------

# A segunda linha contém os nomes reais das colunas.

ibge = pd.read_excel(
    arquivo_ibge,
    sheet_name="BRASIL E UFs",
    header=1
)


# ------------------------------------------------------------
# 6.2 SELEÇÃO DAS COLUNAS NECESSÁRIAS
# ------------------------------------------------------------

# Mantém somente as colunas de UF e população.

ibge = ibge.iloc[:, :2].copy()

ibge.columns = [
    "uf",
    "populacao"
]


# ------------------------------------------------------------
# 6.3 FILTRO DAS 27 UFs
# ------------------------------------------------------------

# Utiliza as UFs já validadas no SIH
# para remover Brasil e regiões agregadas.

ufs_validas = sih_long["uf"].unique()

ibge = ibge[
    ibge["uf"].isin(ufs_validas)
].copy()


# ------------------------------------------------------------
# 6.4 CONVERSÃO DA POPULAÇÃO
# ------------------------------------------------------------

ibge["populacao"] = pd.to_numeric(
    ibge["populacao"],
    errors="coerce"
)


# ------------------------------------------------------------
# 6.5 ADIÇÃO DO CÓDIGO DA UF
# ------------------------------------------------------------

mapa_uf = (
    sih_long[
        ["codigo_uf", "uf"]
    ]
    .drop_duplicates()
)

ibge = ibge.merge(
    mapa_uf,
    on="uf",
    how="left"
)


# Organiza as colunas.

ibge = (
    ibge[
        ["codigo_uf", "uf", "populacao"]
    ]
    .sort_values("codigo_uf")
    .reset_index(drop=True)
)


# ============================================================
# 7. INTEGRAÇÃO DAS TRÊS BASES
# ============================================================

# Parte da base de internações.

base_final = sih_long[
    [
        "codigo_uf",
        "uf",
        "periodo",
        "data",
        "internacoes"
    ]
].copy()


# ------------------------------------------------------------
# 7.1 INTEGRAÇÃO COM CNES
# ------------------------------------------------------------

base_final = base_final.merge(
    cnes_long[
        [
            "codigo_uf",
            "periodo",
            "leitos_sus"
        ]
    ],
    on=["codigo_uf", "periodo"],
    how="left"
)


# ------------------------------------------------------------
# 7.2 INTEGRAÇÃO COM IBGE
# ------------------------------------------------------------

base_final = base_final.merge(
    ibge[
        [
            "codigo_uf",
            "populacao"
        ]
    ],
    on="codigo_uf",
    how="left"
)


# Organiza cronologicamente os registros.

base_final = (
    base_final
    .sort_values(["codigo_uf", "data"])
    .reset_index(drop=True)
)


# ============================================================
# 8. CRIAÇÃO DOS INDICADORES ANALÍTICOS
# ============================================================

# ------------------------------------------------------------
# 8.1 INTERNAÇÕES POR 100 MIL HABITANTES
# ------------------------------------------------------------

base_final["internacoes_100mil"] = (
    base_final["internacoes"]
    /
    base_final["populacao"]
) * 100000


# ------------------------------------------------------------
# 8.2 LEITOS SUS POR 100 MIL HABITANTES
# ------------------------------------------------------------

base_final["leitos_100mil"] = (
    base_final["leitos_sus"]
    /
    base_final["populacao"]
) * 100000


# ------------------------------------------------------------
# 8.3 INTERNAÇÕES POR LEITO
# ------------------------------------------------------------

# Este indicador é utilizado como proxy de carga hospitalar.
#
# IMPORTANTE:
# Não representa taxa de ocupação.

base_final["internacoes_por_leito"] = (
    base_final["internacoes"]
    /
    base_final["leitos_sus"]
)


# Arredonda os indicadores.

base_final[
    [
        "internacoes_100mil",
        "leitos_100mil",
        "internacoes_por_leito"
    ]
] = (
    base_final[
        [
            "internacoes_100mil",
            "leitos_100mil",
            "internacoes_por_leito"
        ]
    ]
    .round(2)
)


# ============================================================
# 9. VARIAÇÃO MENSAL DAS INTERNAÇÕES
# ============================================================

# Garante a ordem cronológica.

base_final = (
    base_final
    .sort_values(["codigo_uf", "data"])
    .reset_index(drop=True)
)


# ------------------------------------------------------------
# 9.1 INTERNAÇÕES DO MÊS ANTERIOR
# ------------------------------------------------------------

base_final["internacoes_mes_anterior"] = (
    base_final
    .groupby("codigo_uf")["internacoes"]
    .shift(1)
)


# ------------------------------------------------------------
# 9.2 VARIAÇÃO ABSOLUTA
# ------------------------------------------------------------

base_final["variacao_internacoes"] = (
    base_final["internacoes"]
    -
    base_final["internacoes_mes_anterior"]
)


# ------------------------------------------------------------
# 9.3 VARIAÇÃO PERCENTUAL
# ------------------------------------------------------------

base_final["variacao_percentual"] = (
    (
        base_final["internacoes"]
        -
        base_final["internacoes_mes_anterior"]
    )
    /
    base_final["internacoes_mes_anterior"]
) * 100

base_final["variacao_percentual"] = (
    base_final["variacao_percentual"]
    .round(2)
)


# ============================================================
# 10. ÍNDICE DE PRESSÃO HOSPITALAR
# ============================================================

# ------------------------------------------------------------
# 10.1 DEMANDA EM RELAÇÃO À CAPACIDADE
# ------------------------------------------------------------

# Compara internações por leito entre as UFs
# dentro de cada período.

base_final["score_demanda_capacidade"] = (
    base_final
    .groupby("periodo")["internacoes_por_leito"]
    .rank(pct=True)
)


# ------------------------------------------------------------
# 10.2 DEMANDA EM RELAÇÃO À POPULAÇÃO
# ------------------------------------------------------------

base_final["score_demanda_populacao"] = (
    base_final
    .groupby("periodo")["internacoes_100mil"]
    .rank(pct=True)
)


# ------------------------------------------------------------
# 10.3 TENDÊNCIA DAS INTERNAÇÕES
# ------------------------------------------------------------

base_final["score_tendencia"] = (
    base_final
    .groupby("periodo")["variacao_percentual"]
    .rank(pct=True)
)


# ------------------------------------------------------------
# 10.4 TRATAMENTO DO PRIMEIRO PERÍODO
# ------------------------------------------------------------

# No primeiro mês não existe histórico anterior.
#
# Utilizamos 0.5 como valor neutro para a tendência.

primeiro_periodo = base_final["data"].min()

base_final.loc[
    base_final["data"] == primeiro_periodo,
    "score_tendencia"
] = 0.5


# ------------------------------------------------------------
# 10.5 CÁLCULO DO IPH
# ------------------------------------------------------------

# Pesos definidos para o MVP:
#
# 50% -> demanda em relação à capacidade
# 30% -> demanda em relação à população
# 20% -> tendência recente

base_final["indice_pressao"] = (
    (
        base_final["score_demanda_capacidade"] * 0.50
        +
        base_final["score_demanda_populacao"] * 0.30
        +
        base_final["score_tendencia"] * 0.20
    )
    * 100
).round(2)


# ============================================================
# 11. CLASSIFICAÇÃO DO NÍVEL DE PRESSÃO
# ============================================================

def classificar_pressao(valor):

    # Caso o índice não tenha sido calculado,
    # mantém a informação como "Sem dado".

    if pd.isna(valor):
        return "Sem dado"

    elif valor < 25:
        return "Baixa"

    elif valor < 50:
        return "Moderada"

    elif valor < 75:
        return "Alta"

    else:
        return "Crítica"


base_final["nivel_pressao"] = (
    base_final["indice_pressao"]
    .apply(classificar_pressao)
)


# ============================================================
# 12. RANKING MENSAL DE PRESSÃO
# ============================================================

# Ranking 1 representa a maior pressão relativa
# dentro daquele período.

base_final["ranking_pressao"] = (
    base_final
    .groupby("periodo")["indice_pressao"]
    .rank(
        method="min",
        ascending=False
    )
)

# Int64 permite armazenar valores inteiros
# e também valores ausentes.

base_final["ranking_pressao"] = (
    base_final["ranking_pressao"]
    .astype("Int64")
)


# ============================================================
# 13. VALIDAÇÃO DA BASE FINAL
# ============================================================

print("==============================================")
print("CAREVision - VALIDAÇÃO DA BASE FINAL")
print("==============================================")

# Dimensões esperadas:
# 27 UFs × 13 meses = 351 registros.

print("\nDimensões:")
print(base_final.shape)


# Verifica duplicidades.

duplicados = base_final.duplicated(
    subset=["codigo_uf", "periodo"]
).sum()

print("\nDuplicidades por UF/período:")
print(duplicados)


# Verifica valores ausentes.

print("\nValores ausentes:")
print(base_final.isna().sum())


# Estatísticas do Índice de Pressão.

print("\nEstatísticas do Índice de Pressão:")
print(
    base_final["indice_pressao"]
    .describe()
)


# Distribuição das classificações.

print("\nDistribuição dos níveis de pressão:")
print(
    base_final["nivel_pressao"]
    .value_counts(dropna=False)
)


# ============================================================
# 14. EXPORTAÇÃO DA BASE ANALÍTICA FINAL
# ============================================================

# Exporta a base utilizada pelo dashboard.
#
# O arquivo permanece na raiz do repositório porque
# o app.py atualmente utiliza esse caminho diretamente.

base_final.to_csv(
    "carevision_base_final.csv",
    index=False,
    encoding="utf-8-sig"
)


# ============================================================
# 15. CONFIRMAÇÃO DA EXPORTAÇÃO
# ============================================================

print("\nBase final exportada com sucesso!")
print("Arquivo: carevision_base_final.csv")
print("Dimensões:", base_final.shape)


# ============================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================

# Streamlit será utilizado para construir a interface.
import streamlit as st

# Pandas será utilizado para carregar e filtrar os dados.
import pandas as pd


# ============================================================
# 2. CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="CareVision",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# 3. CARREGAMENTO DA BASE
# ============================================================

# ============================================================
# CARREGAMENTO DA BASE ANALÍTICA
# ============================================================

# No Streamlit Cloud, o arquivo CSV está no mesmo diretório
# do app.py dentro do repositório do GitHub.
#
# Por isso, usamos apenas o nome do arquivo,
# sem o caminho "/content/" que era específico do Google Colab.
dados = pd.read_csv(
    "carevision_base_final.csv",
    encoding="utf-8-sig"
)

# Converte a coluna de data para o formato datetime.
dados["data"] = pd.to_datetime(
    dados["data"],
    errors="coerce"
)


# ============================================================
# 4. CABEÇALHO
# ============================================================

st.title("🏥 CareVision")

st.markdown(
    """
    ### Monitoramento Analítico de Pressão Hospitalar

    Acompanhamento da demanda hospitalar, capacidade de leitos
    e pressão relativa sobre o sistema hospitalar brasileiro.
    """
)

# Linha divisória.
st.divider()


# ============================================================
# 5. BARRA LATERAL - FILTROS
# ============================================================

st.sidebar.title("🔎 Filtros")

st.sidebar.write(
    "Selecione o período e a Unidade da Federação "
    "que deseja analisar."
)


# ------------------------------------------------------------
# FILTRO DE PERÍODO
# ------------------------------------------------------------

# Criamos uma lista com os períodos disponíveis,
# mantendo a ordem cronológica pela coluna de data.

periodos = (
    dados[["periodo", "data"]]
    .drop_duplicates()
    .sort_values("data")["periodo"]
    .tolist()
)

# Por padrão, selecionamos o período mais recente.
periodo_selecionado = st.sidebar.selectbox(
    "Período",
    options=periodos,
    index=len(periodos) - 1
)


# ------------------------------------------------------------
# FILTRO DE UF
# ------------------------------------------------------------

# Criamos uma lista alfabética com todas as UFs.
ufs = sorted(dados["uf"].unique())

uf_selecionada = st.sidebar.selectbox(
    "Unidade da Federação",
    options=ufs
)


# ============================================================
# 6. FILTRAGEM DOS DADOS
# ============================================================

# Selecionamos somente a linha correspondente
# à UF e ao período escolhidos pelo usuário.

dados_filtrados = dados[
    (dados["periodo"] == periodo_selecionado) &
    (dados["uf"] == uf_selecionada)
]


# Como existe apenas um registro para cada combinação
# UF + período, pegamos a primeira linha encontrada.

registro = dados_filtrados.iloc[0]


# ============================================================
# 7. IDENTIFICAÇÃO DA ANÁLISE
# ============================================================

st.subheader(
    f"📍 {uf_selecionada} — {periodo_selecionado}"
)


# ============================================================
# 8. CARDS / KPIs
# ============================================================

# Criamos cinco colunas para exibir os principais
# indicadores do CareVision.

col1, col2, col3, col4, col5 = st.columns(5)


# ------------------------------------------------------------
# KPI 1 - INTERNAÇÕES
# ------------------------------------------------------------

# Verifica se existe valor de internações.
if pd.notna(registro["internacoes"]):
    valor_internacoes = f'{registro["internacoes"]:,.0f}'
else:
    valor_internacoes = "Sem dado"

col1.metric(
    label="Internações",
    value=valor_internacoes
)


# ------------------------------------------------------------
# KPI 2 - LEITOS SUS
# ------------------------------------------------------------

col2.metric(
    label="Leitos SUS",
    value=f'{registro["leitos_sus"]:,.0f}'
)


# ------------------------------------------------------------
# KPI 3 - INTERNAÇÕES POR LEITO
# ------------------------------------------------------------

if pd.notna(registro["internacoes_por_leito"]):
    valor_por_leito = f'{registro["internacoes_por_leito"]:.2f}'
else:
    valor_por_leito = "Sem dado"

col3.metric(
    label="Internações / leito",
    value=valor_por_leito,
    help=(
        "Proxy de carga hospitalar. "
        "Não representa taxa de ocupação."
    )
)


# ------------------------------------------------------------
# KPI 4 - ÍNDICE DE PRESSÃO
# ------------------------------------------------------------

if pd.notna(registro["indice_pressao"]):
    valor_indice = f'{registro["indice_pressao"]:.1f}'
else:
    valor_indice = "Sem dado"

col4.metric(
    label="Índice de Pressão",
    value=valor_indice
)


# ------------------------------------------------------------
# KPI 5 - NÍVEL DE PRESSÃO
# ------------------------------------------------------------

col5.metric(
    label="Nível de Pressão",
    value=registro["nivel_pressao"]
)


# ============================================================
# 9. VARIAÇÃO MENSAL
# ============================================================

st.divider()

st.subheader("📈 Variação das internações")


# Verifica se existe uma variação percentual calculada.
if pd.notna(registro["variacao_percentual"]):

    variacao = registro["variacao_percentual"]

    st.metric(
        label="Variação em relação ao mês anterior",
        value=f"{variacao:.2f}%"
    )

else:

    st.info(
        "Não há informação suficiente para calcular "
        "a variação em relação ao mês anterior."
    )


# ============================================================
# 10. OBSERVAÇÃO METODOLÓGICA
# ============================================================

st.divider()

st.caption(
    "O Índice de Pressão Hospitalar é um indicador analítico "
    "experimental desenvolvido para o MVP CareVision. "
    "Internações por leito é utilizada como proxy de carga "
    "hospitalar e não representa taxa de ocupação."
)

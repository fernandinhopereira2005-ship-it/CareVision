# -*- coding: utf-8 -*-

# ============================================================
# CAREVISION
# DASHBOARD DE MONITORAMENTO ANALÍTICO DE PRESSÃO HOSPITALAR
# ============================================================

# Este arquivo contém a interface principal do MVP CareVision.
#
# A aplicação consome a base analítica consolidada gerada pelo
# pipeline de tratamento e disponibiliza indicadores, gráficos,
# ranking e comparações entre as Unidades da Federação.


# ============================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================

# Streamlit:
# construção da interface web.
import streamlit as st

# Pandas:
# leitura, organização e filtragem dos dados.
import pandas as pd

# Plotly Express:
# construção dos gráficos interativos.
import plotly.express as px

# Dedent:
# remove a indentação extra existente nas strings HTML
# multilinha antes de enviá-las ao Streamlit.
from textwrap import dedent


# ============================================================
# 2. CONFIGURAÇÃO DA PÁGINA
# ============================================================

# layout="wide" utiliza melhor o espaço horizontal da tela,
# característica importante para dashboards analíticos.

st.set_page_config(
    page_title="CareVision | Pressão Hospitalar",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 3. IDENTIDADE VISUAL / CSS
# ============================================================

# O Streamlit possui uma aparência padrão bastante simples.
#
# O CSS abaixo cria uma identidade visual própria para o
# CareVision, mantendo uma aparência limpa e profissional.

st.markdown(
    dedent(
        """
        <style>

        /* ===================================================
           CONFIGURAÇÃO GERAL DA PÁGINA
           =================================================== */

        .stApp {
            background-color: #F5F7FA;
        }

        .block-container {
            max-width: 1450px;
            padding-top: 1.5rem;
            padding-bottom: 3rem;
        }


        /* ===================================================
           SIDEBAR
           =================================================== */

        [data-testid="stSidebar"] {
            background-color: #0D2948;
        }

        [data-testid="stSidebar"] * {
            color: #FFFFFF;
        }

        [data-testid="stSidebar"] label {
            font-weight: 600;
        }


        /* ===================================================
           CABEÇALHO PRINCIPAL
           =================================================== */

        .carevision-header {
            background:
                linear-gradient(
                    120deg,
                    #0D2948 0%,
                    #12476F 55%,
                    #087F8C 100%
                );

            padding: 28px 34px;
            border-radius: 18px;
            margin-bottom: 24px;

            box-shadow:
                0px 8px 24px rgba(13, 41, 72, 0.14);
        }

        .carevision-brand {
            color: #FFFFFF;
            font-size: 34px;
            font-weight: 750;
            margin: 0;
            letter-spacing: -0.5px;
        }

        .carevision-subtitle {
            color: #D9EAF3;
            font-size: 17px;
            margin-top: 6px;
            margin-bottom: 0px;
        }

        .carevision-source {
            color: #AFC8DA;
            font-size: 13px;
            margin-top: 12px;
            margin-bottom: 0px;
        }


        /* ===================================================
           TÍTULOS DAS SEÇÕES
           =================================================== */

        .section-label {
            color: #087F8C;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 1.3px;
            text-transform: uppercase;
            margin-bottom: 3px;
        }

        .section-title {
            color: #102A43;
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 4px;
        }

        .section-description {
            color: #68798A;
            font-size: 14px;
            margin-bottom: 18px;
        }


        /* ===================================================
           CARDS DOS INDICADORES
           =================================================== */

        .kpi-card {
            background-color: #FFFFFF;
            border: 1px solid #E7ECF1;
            border-radius: 15px;

            padding: 19px 20px;
            min-height: 126px;

            box-shadow:
                0px 3px 12px rgba(22, 45, 66, 0.06);
        }

        .kpi-label {
            color: #718096;
            font-size: 12px;
            font-weight: 650;
            letter-spacing: 0.6px;
            text-transform: uppercase;
            margin-bottom: 9px;
        }

        .kpi-value {
            color: #102A43;
            font-size: 27px;
            font-weight: 750;
            margin-bottom: 4px;
        }

        .kpi-description {
            color: #98A6B3;
            font-size: 11px;
        }


        /* ===================================================
           CARD DE STATUS DO IPH
           =================================================== */

        .status-card {
            border-radius: 15px;
            padding: 20px 24px;
            min-height: 126px;

            box-shadow:
                0px 3px 12px rgba(22, 45, 66, 0.06);
        }

        .status-label {
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.7px;
            margin-bottom: 7px;
        }

        .status-value {
            font-size: 25px;
            font-weight: 800;
            margin-bottom: 4px;
        }

        .status-description {
            font-size: 11px;
            opacity: 0.80;
        }


        /* ===================================================
           CARDS DE CONTEXTO
           =================================================== */

        .context-card {
            background-color: #FFFFFF;
            border: 1px solid #E7ECF1;
            border-radius: 14px;

            padding: 16px 18px;

            box-shadow:
                0px 2px 10px rgba(22, 45, 66, 0.05);
        }

        .context-label {
            color: #718096;
            font-size: 11px;
            font-weight: 650;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .context-value {
            color: #102A43;
            font-size: 21px;
            font-weight: 750;
            margin-top: 4px;
        }

        .context-caption {
            color: #98A6B3;
            font-size: 11px;
            margin-top: 3px;
        }


        /* ===================================================
           CONTAINERS E GRÁFICOS
           =================================================== */

        [data-testid="stPlotlyChart"] {
            background-color: #FFFFFF;
            border: 1px solid #E7ECF1;
            border-radius: 16px;
            padding: 7px;

            box-shadow:
                0px 3px 12px rgba(22, 45, 66, 0.05);
        }


        /* ===================================================
           DATAFRAME
           =================================================== */

        [data-testid="stDataFrame"] {
            background-color: #FFFFFF;
            border-radius: 14px;

            box-shadow:
                0px 3px 12px rgba(22, 45, 66, 0.05);
        }


        /* ===================================================
           DIVISORES
           =================================================== */

        hr {
            border: none;
            border-top: 1px solid #E7ECF1;
            margin-top: 28px;
            margin-bottom: 28px;
        }


        /* ===================================================
           RODAPÉ
           =================================================== */

        .carevision-footer {
            text-align: center;
            color: #8291A1;
            font-size: 12px;
            padding-top: 15px;
            padding-bottom: 10px;
        }

        </style>
        """
    ),
    unsafe_allow_html=True
)


# ============================================================
# 4. CARREGAMENTO DA BASE ANALÍTICA
# ============================================================

# No Streamlit Cloud, o arquivo CSV encontra-se na raiz
# do repositório, junto ao app.py.

dados = pd.read_csv(
    "carevision_base_final.csv",
    encoding="utf-8-sig"
)

# Converte a coluna de data para datetime.
#
# errors="coerce" transforma valores inválidos em NaT,
# evitando erro durante a execução da aplicação.

dados["data"] = pd.to_datetime(
    dados["data"],
    errors="coerce"
)


# ============================================================
# 5. FUNÇÕES AUXILIARES
# ============================================================

def formatar_inteiro(valor):
    """
    Formata valores inteiros utilizando ponto como
    separador de milhar no padrão brasileiro.
    """

    if pd.isna(valor):
        return "Sem dado"

    return f"{valor:,.0f}".replace(",", ".")


def formatar_decimal(valor, casas=2):
    """
    Formata valores decimais utilizando vírgula
    como separador decimal.
    """

    if pd.isna(valor):
        return "Sem dado"

    return f"{valor:.{casas}f}".replace(".", ",")


def obter_estilo_pressao(nivel):
    """
    Define as cores utilizadas no card de classificação
    de acordo com o nível de pressão hospitalar.
    """

    estilos = {

        "Baixa": {
            "fundo": "#E8F7EF",
            "borda": "#B9E5CD",
            "texto": "#18794E"
        },

        "Moderada": {
            "fundo": "#FFF7DD",
            "borda": "#F3D98B",
            "texto": "#986A00"
        },

        "Alta": {
            "fundo": "#FFF0E1",
            "borda": "#F4C28F",
            "texto": "#B45309"
        },

        "Crítica": {
            "fundo": "#FDECEC",
            "borda": "#F3B7B7",
            "texto": "#B42318"
        },

        "Sem dado": {
            "fundo": "#EEF1F4",
            "borda": "#D6DCE2",
            "texto": "#5F6B76"
        }
    }

    return estilos.get(
        nivel,
        estilos["Sem dado"]
    )


def renderizar_html(conteudo):
    """
    Renderiza blocos HTML personalizados no Streamlit.

    O dedent remove a indentação existente nas strings
    multilinha, evitando que o Streamlit interprete
    o HTML como um bloco de código Markdown.
    """

    st.markdown(
        dedent(conteudo),
        unsafe_allow_html=True
    )


# ============================================================
# 6. CABEÇALHO PRINCIPAL
# ============================================================

# Utilizamos HTML personalizado para criar um cabeçalho
# mais profissional do que o título padrão do Streamlit.

renderizar_html(
    """
    <div class="carevision-header">

        <p class="carevision-brand">
            🏥 CareVision
        </p>

        <p class="carevision-subtitle">
            Monitoramento Analítico de Pressão Hospitalar
        </p>

        <p class="carevision-source">
            Dados públicos • SIH/SUS • CNES • IBGE
        </p>

    </div>
    """
)


# ============================================================
# 7. BARRA LATERAL
# ============================================================

# A barra lateral concentra os filtros para liberar
# espaço na área principal do dashboard.

st.sidebar.markdown(
    """
    ## CareVision

    **Painel de análise hospitalar**

    Utilize os filtros abaixo para explorar os indicadores.
    """
)

st.sidebar.divider()


# ------------------------------------------------------------
# FILTRO DE PERÍODO
# ------------------------------------------------------------

# Criamos uma lista cronologicamente ordenada.

periodos = (
    dados[
        ["periodo", "data"]
    ]
    .drop_duplicates()
    .sort_values("data")["periodo"]
    .tolist()
)

# O período mais recente aparece selecionado por padrão.

periodo_selecionado = st.sidebar.selectbox(
    "📅 Período",
    options=periodos,
    index=len(periodos) - 1
)


# ------------------------------------------------------------
# FILTRO DE UF
# ------------------------------------------------------------

# Lista as UFs em ordem alfabética.

ufs = sorted(
    dados["uf"]
    .dropna()
    .unique()
)

uf_selecionada = st.sidebar.selectbox(
    "📍 Unidade da Federação",
    options=ufs
)


# ------------------------------------------------------------
# INFORMAÇÃO METODOLÓGICA NA SIDEBAR
# ------------------------------------------------------------

st.sidebar.divider()

st.sidebar.markdown(
    """
    **Sobre o índice**

    O IPH varia de **0 a 100** e compara a pressão relativa
    entre as UFs dentro de cada período.

    🟢 Baixa  
    🟡 Moderada  
    🟠 Alta  
    🔴 Crítica
    """
)

st.sidebar.divider()

st.sidebar.caption(
    "MVP acadêmico • Dados públicos brasileiros"
)


# ============================================================
# 8. FILTRAGEM DOS DADOS
# ============================================================

# Selecionamos a combinação escolhida pelo usuário.

dados_filtrados = dados[
    (dados["periodo"] == periodo_selecionado)
    &
    (dados["uf"] == uf_selecionada)
]


# Existe uma linha para cada combinação UF + período.

registro = dados_filtrados.iloc[0]


# ============================================================
# 9. PREPARAÇÃO DO RANKING DO PERÍODO
# ============================================================

# Selecionamos todas as UFs disponíveis no mesmo período
# para calcular o contexto nacional.

ranking_periodo = dados[
    dados["periodo"] == periodo_selecionado
].copy()

# Registros sem IPH não entram no ranking.

ranking_valido = ranking_periodo.dropna(
    subset=["indice_pressao"]
).copy()

# Ordenação do maior para o menor IPH.

ranking_valido = ranking_valido.sort_values(
    "indice_pressao",
    ascending=False
).reset_index(drop=True)

# Criamos uma posição sequencial apenas para exibição.

ranking_valido["posicao_dashboard"] = range(
    1,
    len(ranking_valido) + 1
)


# ------------------------------------------------------------
# POSIÇÃO DA UF SELECIONADA
# ------------------------------------------------------------

posicao_uf = ranking_valido[
    ranking_valido["uf"] == uf_selecionada
]["posicao_dashboard"]


if len(posicao_uf) > 0:

    posicao_uf = int(
        posicao_uf.iloc[0]
    )

    valor_ranking = (
        f"{posicao_uf}º de "
        f"{len(ranking_valido)}"
    )

else:

    valor_ranking = "Sem dado"


# ============================================================
# 10. IDENTIFICAÇÃO DA ANÁLISE
# ============================================================

renderizar_html(
    """
    <div class="section-label">
        VISÃO GERAL
    </div>
    """
)

renderizar_html(
    f"""
    <div class="section-title">
        {uf_selecionada} • {periodo_selecionado}
    </div>
    """
)

renderizar_html(
    """
    <div class="section-description">
        Indicadores hospitalares e posição relativa
        no período selecionado.
    </div>
    """
)


# ============================================================
# 11. PREPARAÇÃO DOS VALORES DOS KPIs
# ============================================================

valor_internacoes = formatar_inteiro(
    registro["internacoes"]
)

valor_leitos = formatar_inteiro(
    registro["leitos_sus"]
)

valor_por_leito = formatar_decimal(
    registro["internacoes_por_leito"],
    2
)

valor_indice = formatar_decimal(
    registro["indice_pressao"],
    1
)

nivel_pressao = registro["nivel_pressao"]

estilo_pressao = obter_estilo_pressao(
    nivel_pressao
)


# ============================================================
# 12. CARDS PRINCIPAIS
# ============================================================

# Utilizamos quatro indicadores numéricos e um card
# específico para a classificação de pressão.

col1, col2, col3, col4, col5 = st.columns(
    [1, 1, 1, 1, 1.15]
)


# ------------------------------------------------------------
# INTERNAÇÕES
# ------------------------------------------------------------

with col1:

    renderizar_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Internações
            </div>

            <div class="kpi-value">
                {valor_internacoes}
            </div>

            <div class="kpi-description">
                Volume registrado no período
            </div>

        </div>
        """
    )


# ------------------------------------------------------------
# LEITOS SUS
# ------------------------------------------------------------

with col2:

    renderizar_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Leitos SUS
            </div>

            <div class="kpi-value">
                {valor_leitos}
            </div>

            <div class="kpi-description">
                Capacidade registrada
            </div>

        </div>
        """
    )


# ------------------------------------------------------------
# INTERNAÇÕES POR LEITO
# ------------------------------------------------------------

with col3:

    renderizar_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Internações / leito
            </div>

            <div class="kpi-value">
                {valor_por_leito}
            </div>

            <div class="kpi-description">
                Proxy de carga hospitalar
            </div>

        </div>
        """
    )


# ------------------------------------------------------------
# ÍNDICE DE PRESSÃO
# ------------------------------------------------------------

with col4:

    renderizar_html(
        f"""
        <div class="kpi-card">

            <div class="kpi-label">
                Índice de Pressão
            </div>

            <div class="kpi-value">
                {valor_indice}
            </div>

            <div class="kpi-description">
                Escala analítica de 0 a 100
            </div>

        </div>
        """
    )


# ------------------------------------------------------------
# CLASSIFICAÇÃO
# ------------------------------------------------------------

with col5:

    renderizar_html(
        f"""
        <div
            class="status-card"
            style="
                background-color: {estilo_pressao['fundo']};
                border: 1px solid {estilo_pressao['borda']};
                color: {estilo_pressao['texto']};
            "
        >

            <div class="status-label">
                Nível de Pressão
            </div>

            <div class="status-value">
                {nivel_pressao}
            </div>

            <div class="status-description">
                Classificação do IPH
            </div>

        </div>
        """
    )


# ============================================================
# 13. CONTEXTO DO PERÍODO
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

contexto1, contexto2, contexto3 = st.columns(3)


# ------------------------------------------------------------
# VARIAÇÃO MENSAL
# ------------------------------------------------------------

with contexto1:

    if pd.notna(
        registro["variacao_percentual"]
    ):

        variacao = registro[
            "variacao_percentual"
        ]

        sinal = "+" if variacao > 0 else ""

        valor_variacao = (
            f"{sinal}"
            f"{formatar_decimal(variacao, 2)}%"
        )

    else:

        valor_variacao = "Sem dado"

    renderizar_html(
        f"""
        <div class="context-card">

            <div class="context-label">
                Variação mensal
            </div>

            <div class="context-value">
                {valor_variacao}
            </div>

            <div class="context-caption">
                Em relação ao mês anterior
            </div>

        </div>
        """
    )


# ------------------------------------------------------------
# RANKING NACIONAL
# ------------------------------------------------------------

with contexto2:

    renderizar_html(
        f"""
        <div class="context-card">

            <div class="context-label">
                Posição nacional
            </div>

            <div class="context-value">
                {valor_ranking}
            </div>

            <div class="context-caption">
                Ranking de pressão no período
            </div>

        </div>
        """
    )


# ------------------------------------------------------------
# COBERTURA DA ANÁLISE
# ------------------------------------------------------------

with contexto3:

    quantidade_ufs_validas = len(
        ranking_valido
    )

    renderizar_html(
        f"""
        <div class="context-card">

            <div class="context-label">
                UFs com IPH calculado
            </div>

            <div class="context-value">
                {quantidade_ufs_validas}
            </div>

            <div class="context-caption">
                Registros válidos no período
            </div>

        </div>
        """
    )


# ============================================================
# 14. EVOLUÇÃO HISTÓRICA DAS INTERNAÇÕES
# ============================================================

st.divider()

renderizar_html(
    """
    <div class="section-label">
        EVOLUÇÃO TEMPORAL
    </div>
    """
)

renderizar_html(
    f"""
    <div class="section-title">
        Internações em {uf_selecionada}
    </div>
    """
)

renderizar_html(
    """
    <div class="section-description">
        Comportamento mensal das internações ao longo
        da série disponível.
    </div>
    """
)


# Seleciona todo o histórico da UF escolhida.

historico_uf = dados[
    dados["uf"] == uf_selecionada
].copy()

historico_uf = historico_uf.sort_values(
    "data"
)


# ------------------------------------------------------------
# GRÁFICO DE LINHA
# ------------------------------------------------------------

grafico_internacoes = px.line(
    historico_uf,
    x="data",
    y="internacoes",
    markers=True,

    labels={
        "data": "Período",
        "internacoes": "Internações"
    }
)


# Configuração visual.

grafico_internacoes.update_layout(

    title_text="",

    template="plotly_white",

    xaxis_title="",
    yaxis_title="Internações",

    hovermode="x unified",

    height=410,

    margin=dict(
        l=30,
        r=30,
        t=25,
        b=25
    ),

    showlegend=False,

    font=dict(
        family="Arial",
        size=12
    )
)


# Remove linhas visuais excessivas.

grafico_internacoes.update_xaxes(
    showgrid=False
)

grafico_internacoes.update_yaxes(
    gridcolor="#EDF1F5",
    zeroline=False
)


st.plotly_chart(
    grafico_internacoes,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)


# ============================================================
# 15. RANKING NACIONAL
# ============================================================

st.divider()

renderizar_html(
    """
    <div class="section-label">
        COMPARAÇÃO NACIONAL
    </div>
    """
)

renderizar_html(
    f"""
    <div class="section-title">
        UFs com maior pressão • {periodo_selecionado}
    </div>
    """
)

renderizar_html(
    """
    <div class="section-description">
        Top 10 Unidades da Federação segundo o
        Índice de Pressão Hospitalar.
    </div>
    """
)


# ------------------------------------------------------------
# TOP 10
# ------------------------------------------------------------

top_10 = (
    ranking_valido
    .head(10)
    .copy()
)

# Invertemos para colocar o maior valor
# no topo do gráfico horizontal.

top_10 = top_10.sort_values(
    "indice_pressao",
    ascending=True
)


# ------------------------------------------------------------
# CORES DAS CLASSIFICAÇÕES
# ------------------------------------------------------------

cores_pressao = {
    "Baixa": "#2CA66F",
    "Moderada": "#E5B52E",
    "Alta": "#E98532",
    "Crítica": "#D94A4A",
    "Sem dado": "#9AA5B1"
}


# ------------------------------------------------------------
# GRÁFICO DO RANKING
# ------------------------------------------------------------

grafico_ranking = px.bar(
    top_10,

    x="indice_pressao",
    y="uf",

    orientation="h",

    color="nivel_pressao",

    color_discrete_map=cores_pressao,

    hover_data={
        "internacoes": ":,.0f",
        "leitos_sus": ":,.0f",
        "internacoes_por_leito": ":.2f",
        "variacao_percentual": ":.2f",
        "indice_pressao": ":.1f"
    },

    labels={
        "indice_pressao":
            "Índice de Pressão",

        "uf":
            "UF",

        "nivel_pressao":
            "Nível",

        "internacoes":
            "Internações",

        "leitos_sus":
            "Leitos SUS",

        "internacoes_por_leito":
            "Internações / leito",

        "variacao_percentual":
            "Variação mensal (%)"
    }
)


grafico_ranking.update_layout(

    title_text="",

    template="plotly_white",

    xaxis_title="Índice de Pressão Hospitalar",
    yaxis_title="",

    legend_title_text="Nível de pressão",

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),

    height=500,

    margin=dict(
        l=30,
        r=30,
        t=50,
        b=30
    ),

    font=dict(
        family="Arial",
        size=12
    )
)


# O IPH possui escala de 0 a 100.

grafico_ranking.update_xaxes(
    range=[0, 100],
    gridcolor="#EDF1F5",
    zeroline=False
)

grafico_ranking.update_yaxes(
    showgrid=False
)


st.plotly_chart(
    grafico_ranking,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)


# ============================================================
# 16. TABELA ANALÍTICA NACIONAL
# ============================================================

st.divider()

renderizar_html(
    """
    <div class="section-label">
        DETALHAMENTO
    </div>
    """
)

renderizar_html(
    f"""
    <div class="section-title">
        Visão Analítica Nacional • {periodo_selecionado}
    </div>
    """
)

renderizar_html(
    """
    <div class="section-description">
        Indicadores consolidados das Unidades da Federação
        no período selecionado.
    </div>
    """
)


# ------------------------------------------------------------
# PREPARAÇÃO DOS DADOS
# ------------------------------------------------------------

tabela_nacional = dados[
    dados["periodo"] == periodo_selecionado
][
    [
        "uf",
        "internacoes",
        "leitos_sus",
        "internacoes_por_leito",
        "variacao_percentual",
        "indice_pressao",
        "nivel_pressao"
    ]
].copy()


# Ordena do maior para o menor IPH.

tabela_nacional = tabela_nacional.sort_values(
    "indice_pressao",
    ascending=False,
    na_position="last"
)


# Renomeia as colunas.

tabela_nacional = tabela_nacional.rename(
    columns={
        "uf": "UF",
        "internacoes": "Internações",
        "leitos_sus": "Leitos SUS",
        "internacoes_por_leito":
            "Internações / leito",
        "variacao_percentual":
            "Variação mensal (%)",
        "indice_pressao":
            "Índice de Pressão",
        "nivel_pressao":
            "Nível de Pressão"
    }
)


# ------------------------------------------------------------
# TABELA
# ------------------------------------------------------------

st.dataframe(
    tabela_nacional,

    use_container_width=True,

    hide_index=True,

    height=480,

    column_config={

        "Internações":
            st.column_config.NumberColumn(
                "Internações",
                format="%.0f"
            ),

        "Leitos SUS":
            st.column_config.NumberColumn(
                "Leitos SUS",
                format="%.0f"
            ),

        "Internações / leito":
            st.column_config.NumberColumn(
                "Internações / leito",
                format="%.2f"
            ),

        "Variação mensal (%)":
            st.column_config.NumberColumn(
                "Variação mensal (%)",
                format="%.2f"
            ),

        "Índice de Pressão":
            st.column_config.ProgressColumn(
                "Índice de Pressão",
                help=(
                    "Índice experimental do CareVision "
                    "em escala de 0 a 100."
                ),
                min_value=0,
                max_value=100,
                format="%.1f"
            )
    }
)


# ============================================================
# 17. METODOLOGIA E LIMITAÇÕES
# ============================================================

st.divider()

with st.expander(
    "ℹ️ Metodologia e limitações do CareVision"
):

    st.markdown(
        """
        **Índice de Pressão Hospitalar (IPH)**

        O índice combina três componentes:

        - **50%** — demanda em relação à capacidade;
        - **30%** — demanda em relação à população;
        - **20%** — tendência mensal das internações.

        Os componentes são comparados entre as UFs dentro
        de cada período e combinados em uma escala de 0 a 100.

        **Importante:** o IPH é um indicador analítico
        experimental desenvolvido para o MVP CareVision.

        A relação **internações por leito** é utilizada como
        proxy de carga hospitalar e **não representa taxa de
        ocupação hospitalar**.

        Os dados de internações são provenientes do SIH/SUS,
        os dados de leitos do CNES e a população utilizada
        corresponde às estimativas do IBGE.
        """
    )


# ============================================================
# 18. RODAPÉ
# ============================================================

renderizar_html(
    """
    <div class="carevision-footer">

        CareVision • Monitoramento Analítico de Pressão Hospitalar
        <br>

        SIH/SUS • CNES • IBGE

    </div>
    """
)

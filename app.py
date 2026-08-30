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
# utilizado para construir a interface web.
import streamlit as st

# Pandas:
# utilizado para leitura, organização e filtragem dos dados.
import pandas as pd

# Plotly Express:
# utilizado para construção dos gráficos interativos.
import plotly.express as px

# Dedent:
# remove a indentação extra de strings multilinha.
from textwrap import dedent


# ============================================================
# 2. CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="CareVision | Pressão Hospitalar",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 3. IDENTIDADE VISUAL / CSS
# ============================================================

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
           GRÁFICOS
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
           TABELA
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

dados = pd.read_csv(
    "carevision_base_final.csv",
    encoding="utf-8-sig"
)

# Converte a coluna de data para datetime.
dados["data"] = pd.to_datetime(
    dados["data"],
    errors="coerce"
)


# ============================================================
# 5. FUNÇÕES AUXILIARES
# ============================================================

def formatar_inteiro(valor):
    """
    Formata valores inteiros utilizando ponto
    como separador de milhar no padrão brasileiro.
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
    Renderiza os componentes HTML personalizados
    utilizados na interface do CareVision.
    """

    conteudo_limpo = dedent(conteudo)

    st.html(conteudo_limpo)


# ============================================================
# 6. CABEÇALHO PRINCIPAL
# ============================================================

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

st.sidebar.markdown(
    """
    ## 🏥 CareVision

    **Painel de análise hospitalar**

    Utilize os filtros abaixo para explorar os indicadores.
    """
)

st.sidebar.divider()


# ============================================================
# 8. FILTRO DE PERÍODO
# ============================================================

periodos = (
    dados[
        ["periodo", "data"]
    ]
    .drop_duplicates()
    .sort_values("data")["periodo"]
    .tolist()
)

periodo_selecionado = st.sidebar.selectbox(
    "📅 Período",
    options=periodos,
    index=len(periodos) - 1
)


# ============================================================
# 9. FILTRO DE UF
# ============================================================

ufs = sorted(
    dados["uf"]
    .dropna()
    .unique()
)

# Define São Paulo como UF padrão, caso esteja disponível.
#
# Isso evita que Acre apareça inicialmente em junho de 2026,
# período no qual não existe valor de internações disponível
# para cálculo do IPH.

indice_uf_padrao = (
    ufs.index("São Paulo")
    if "São Paulo" in ufs
    else 0
)

uf_selecionada = st.sidebar.selectbox(
    "📍 Unidade da Federação",
    options=ufs,
    index=indice_uf_padrao
)


# ============================================================
# 10. INFORMAÇÕES METODOLÓGICAS NA SIDEBAR
# ============================================================

st.sidebar.divider()

st.sidebar.markdown(
    """
    **Sobre o IPH**

    O Índice de Pressão Hospitalar varia de **0 a 100**
    e compara a pressão relativa entre as UFs dentro
    de cada período.

    🟢 **Baixa:** abaixo de 25  
    🟡 **Moderada:** 25 a abaixo de 50  
    🟠 **Alta:** 50 a abaixo de 75  
    🔴 **Crítica:** 75 a 100
    """
)

st.sidebar.divider()

st.sidebar.caption(
    "MVP acadêmico • Dados públicos brasileiros"
)


# ============================================================
# 11. FILTRAGEM DOS DADOS
# ============================================================

dados_filtrados = dados[
    (dados["periodo"] == periodo_selecionado)
    &
    (dados["uf"] == uf_selecionada)
]

registro = dados_filtrados.iloc[0]


# ============================================================
# 12. PREPARAÇÃO DO RANKING
# ============================================================

ranking_periodo = dados[
    dados["periodo"] == periodo_selecionado
].copy()

ranking_valido = ranking_periodo.dropna(
    subset=["indice_pressao"]
).copy()

ranking_valido = ranking_valido.sort_values(
    "indice_pressao",
    ascending=False
).reset_index(drop=True)

ranking_valido["posicao_dashboard"] = range(
    1,
    len(ranking_valido) + 1
)


# ============================================================
# 13. POSIÇÃO DA UF SELECIONADA
# ============================================================

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
# 14. IDENTIFICAÇÃO DA ANÁLISE
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
# 15. PREPARAÇÃO DOS KPIs
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

# Caso exista algum valor ausente inesperado.
if pd.isna(nivel_pressao):
    nivel_pressao = "Sem dado"

estilo_pressao = obter_estilo_pressao(
    nivel_pressao
)


# ============================================================
# 16. CARDS PRINCIPAIS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(
    [1, 1, 1, 1, 1.15]
)


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
# 17. CONTEXTO DO PERÍODO
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

contexto1, contexto2, contexto3 = st.columns(3)


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
# 18. EVOLUÇÃO HISTÓRICA DAS INTERNAÇÕES
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
        da série histórica disponível.
    </div>
    """
)


historico_uf = dados[
    dados["uf"] == uf_selecionada
].copy()

historico_uf = historico_uf.sort_values(
    "data"
)


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
# 19. RANKING NACIONAL
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


# ============================================================
# 20. AVISO DE INTERPRETAÇÃO DO RANKING
# ============================================================

# Este aviso é importante porque o IPH não mede qualidade geral
# do sistema de saúde, vulnerabilidade socioeconômica ou toda
# a estrutura hospitalar existente em cada estado.
#
# A análise utiliza internações registradas no SIH/SUS e
# leitos SUS registrados no CNES.

st.info(
    """
    **Como interpretar o ranking**

    O CareVision analisa **internações registradas no SIH/SUS**
    e **leitos SUS registrados no CNES**.

    Por isso, o Índice de Pressão Hospitalar representa a
    **pressão relativa observada na rede analisada**, e não um
    indicador geral de vulnerabilidade social, qualidade da saúde
    ou da situação hospitalar completa de cada estado.

    Assim, estados com menor infraestrutura ou maior
    vulnerabilidade não necessariamente aparecerão nas primeiras
    posições do ranking.
    """
)


# ============================================================
# 21. TOP 10 NACIONAL
# ============================================================

top_10 = (
    ranking_valido
    .head(10)
    .copy()
)


# Invertemos a ordem para que o maior valor fique no topo
# do gráfico horizontal.

top_10 = top_10.sort_values(
    "indice_pressao",
    ascending=True
)


# ============================================================
# 22. CORES DAS CLASSIFICAÇÕES
# ============================================================

cores_pressao = {

    "Baixa": "#2CA66F",

    "Moderada": "#E5B52E",

    "Alta": "#E98532",

    "Crítica": "#D94A4A",

    "Sem dado": "#9AA5B1"
}


# ============================================================
# 23. GRÁFICO DO RANKING
# ============================================================

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
# 24. TABELA ANALÍTICA NACIONAL
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


tabela_nacional = tabela_nacional.sort_values(
    "indice_pressao",
    ascending=False,
    na_position="last"
)


tabela_nacional = tabela_nacional.rename(
    columns={

        "uf":
            "UF",

        "internacoes":
            "Internações",

        "leitos_sus":
            "Leitos SUS",

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
# 25. METODOLOGIA E LIMITAÇÕES
# ============================================================

st.divider()

with st.expander(
    "ℹ️ Metodologia e limitações do CareVision"
):

    st.markdown(
        """
        ### Índice de Pressão Hospitalar

        O **Índice de Pressão Hospitalar (IPH)** é um indicador
        experimental desenvolvido para o MVP CareVision.

        Ele combina três componentes:

        - **50% — demanda em relação à capacidade:** baseada
          na relação entre internações e leitos SUS;

        - **30% — demanda em relação à população:** baseada
          no número de internações por 100 mil habitantes;

        - **20% — tendência recente:** baseada na variação
          percentual das internações em relação ao mês anterior.

        Os componentes são comparados entre as UFs dentro
        de cada período e combinados em uma escala de
        **0 a 100**.

        ### Classificação

        - **Baixa:** IPH abaixo de 25;
        - **Moderada:** IPH de 25 até abaixo de 50;
        - **Alta:** IPH de 50 até abaixo de 75;
        - **Crítica:** IPH de 75 a 100.

        ### Interpretação dos dados

        O CareVision utiliza **internações registradas no
        SIH/SUS** e **leitos SUS registrados no CNES**.

        Portanto, o ranking não representa toda a estrutura
        hospitalar existente no território brasileiro.

        Um estado com maior vulnerabilidade social, menor
        disponibilidade geral de serviços ou outras dificuldades
        assistenciais não necessariamente apresentará o maior IPH.

        ### Limitações

        A relação **internações por leito** é utilizada como
        proxy de carga hospitalar e **não representa taxa
        de ocupação hospitalar**.

        Para calcular uma taxa real de ocupação seriam
        necessários dados operacionais adicionais, como
        leitos-dia disponíveis e pacientes-dia.

        Os dados de internações utilizados são provenientes
        do **SIH/SUS** e representam internações registradas
        e financiadas pelo Sistema Único de Saúde.

        Os dados de leitos são provenientes do **CNES**.

        A população utilizada corresponde às estimativas
        populacionais do **IBGE**.

        O IPH não é um indicador oficial do Ministério da Saúde,
        DATASUS, CNES ou IBGE e não possui finalidade clínica.
        """
    )


# ============================================================
# 26. RODAPÉ
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

# -*- coding: utf-8 -*-

# ============================================================
# CAREVISION
# DASHBOARD DE MONITORAMENTO ANALÍTICO DE PRESSÃO HOSPITALAR
# ============================================================

# Este arquivo contém a interface principal do MVP CareVision.
#
# A aplicação utiliza a base analítica consolidada gerada
# pelo pipeline de tratamento de dados e apresenta:
#
# - indicadores hospitalares;
# - evolução temporal;
# - Índice de Pressão Hospitalar;
# - ranking nacional;
# - mapa do Brasil;
# - comparações entre UFs;
# - análises de demanda e capacidade;
# - tendências recentes;
# - tabela analítica nacional.


# ============================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================

# Streamlit:
# construção da aplicação web.
import streamlit as st

# Pandas:
# leitura, organização e filtragem dos dados.
import pandas as pd

# Plotly Express:
# criação de gráficos interativos.
import plotly.express as px

# JSON:
# leitura do arquivo GeoJSON utilizado no mapa do Brasil.
import json

# Path:
# facilita a manipulação e validação dos caminhos dos arquivos.
from pathlib import Path

# Dedent:
# remove indentação extra de strings HTML multilinha.
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
           CONFIGURAÇÃO GERAL
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

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label {
            color: #FFFFFF;
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
           CARDS DOS KPIs
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
           CARD DE STATUS
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
           DATAFRAME
           =================================================== */

        [data-testid="stDataFrame"] {
            background-color: #FFFFFF;
            border-radius: 14px;

            box-shadow:
                0px 3px 12px rgba(22, 45, 66, 0.05);
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
# 4. CAMINHOS DOS ARQUIVOS
# ============================================================

# Base analítica utilizada pelo dashboard.
CAMINHO_BASE = Path("carevision_base_final.csv")

# Arquivo geográfico dos estados brasileiros.
CAMINHO_GEOJSON = Path(
    "data/geo/estados_brasil.geojson"
)


# ============================================================
# 5. CARREGAMENTO DA BASE
# ============================================================

dados = pd.read_csv(
    CAMINHO_BASE,
    encoding="utf-8-sig"
)

# Converte a coluna de data para datetime.
dados["data"] = pd.to_datetime(
    dados["data"],
    errors="coerce"
)


# ============================================================
# 6. CARREGAMENTO DO GEOJSON
# ============================================================

# Inicializamos a variável como None.
# Assim, caso o arquivo não seja encontrado, o restante
# do dashboard continua funcionando normalmente.

geojson_estados = None


if CAMINHO_GEOJSON.exists():

    try:

        # Abre o arquivo GeoJSON utilizando UTF-8.
        with open(
            CAMINHO_GEOJSON,
            "r",
            encoding="utf-8"
        ) as arquivo_geo:

            geojson_estados = json.load(
                arquivo_geo
            )


        # ----------------------------------------------------
        # PADRONIZAÇÃO DO NOME DAS UFs
        # ----------------------------------------------------
        #
        # Para que o mapa consiga relacionar cada polígono
        # do GeoJSON com a coluna "uf" da nossa base,
        # criamos uma propriedade padronizada chamada:
        #
        # carevision_uf
        #
        # O código procura automaticamente algumas
        # nomenclaturas comuns utilizadas em GeoJSONs.

        propriedades_possiveis = [

            "nome",
            "name",
            "NM_UF",
            "nm_uf",
            "estado",
            "Estado"
        ]


        for feature in geojson_estados.get(
            "features",
            []
        ):

            propriedades = feature.get(
                "properties",
                {}
            )

            nome_encontrado = None


            for propriedade in propriedades_possiveis:

                if propriedade in propriedades:

                    nome_encontrado = propriedades[
                        propriedade
                    ]

                    break


            # Cria uma nova propriedade padronizada.
            propriedades[
                "carevision_uf"
            ] = nome_encontrado


    except Exception as erro:

        geojson_estados = None

        st.warning(
            "O arquivo do mapa foi encontrado, mas não pôde "
            f"ser carregado. Detalhes: {erro}"
        )


# ============================================================
# 7. FUNÇÕES AUXILIARES
# ============================================================

def formatar_inteiro(valor):

    """
    Formata valores inteiros utilizando ponto
    como separador de milhar.
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
    Retorna as cores associadas a cada nível
    de pressão hospitalar.
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
    Renderiza elementos HTML personalizados.
    """

    conteudo_limpo = dedent(
        conteudo
    )

    st.html(
        conteudo_limpo
    )


# ============================================================
# 8. CORES DOS NÍVEIS DE PRESSÃO
# ============================================================

cores_pressao = {

    "Baixa": "#2CA66F",

    "Moderada": "#E5B52E",

    "Alta": "#E98532",

    "Crítica": "#D94A4A",

    "Sem dado": "#9AA5B1"
}


# ============================================================
# 9. CABEÇALHO
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
# 10. SIDEBAR
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
# 11. FILTRO DE PERÍODO
# ============================================================

periodos = (

    dados[
        [
            "periodo",
            "data"
        ]
    ]

    .drop_duplicates()

    .sort_values(
        "data"
    )["periodo"]

    .tolist()
)


periodo_selecionado = st.sidebar.selectbox(

    "📅 Período",

    options=periodos,

    index=len(periodos) - 1
)


# ============================================================
# 12. FILTRO DE UF
# ============================================================

ufs = sorted(

    dados[
        "uf"
    ]

    .dropna()

    .unique()
)


# São Paulo é utilizado como visualização inicial.
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
# 13. INFORMAÇÕES DO IPH NA SIDEBAR
# ============================================================

st.sidebar.divider()

st.sidebar.markdown(
    """
    **Sobre o IPH**

    O Índice de Pressão Hospitalar varia de **0 a 100**
    e representa a posição relativa das UFs dentro
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
# 14. FILTRAGEM DA UF SELECIONADA
# ============================================================

dados_filtrados = dados[

    (
        dados["periodo"]
        == periodo_selecionado
    )

    &

    (
        dados["uf"]
        == uf_selecionada
    )

]


registro = dados_filtrados.iloc[0]


# ============================================================
# 15. PREPARAÇÃO DO RANKING DO PERÍODO
# ============================================================

ranking_periodo = dados[

    dados["periodo"]
    == periodo_selecionado

].copy()


# Garante que valores ausentes tenham classificação
# explícita para gráficos e mapa.
ranking_periodo[
    "nivel_pressao"
] = ranking_periodo[
    "nivel_pressao"
].fillna(
    "Sem dado"
)


ranking_valido = ranking_periodo.dropna(

    subset=[
        "indice_pressao"
    ]

).copy()


ranking_valido = ranking_valido.sort_values(

    "indice_pressao",

    ascending=False

).reset_index(
    drop=True
)


ranking_valido[
    "posicao_dashboard"
] = range(

    1,

    len(ranking_valido) + 1
)


# ============================================================
# 16. POSIÇÃO NACIONAL DA UF
# ============================================================

posicao_uf = ranking_valido[

    ranking_valido[
        "uf"
    ] == uf_selecionada

][
    "posicao_dashboard"
]


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
# 17. VISÃO GERAL
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
# 18. PREPARAÇÃO DOS KPIs
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


nivel_pressao = registro[
    "nivel_pressao"
]


if pd.isna(
    nivel_pressao
):

    nivel_pressao = "Sem dado"


estilo_pressao = obter_estilo_pressao(
    nivel_pressao
)


# ============================================================
# 19. CARDS PRINCIPAIS
# ============================================================

col1, col2, col3, col4, col5 = st.columns(
    [
        1,
        1,
        1,
        1,
        1.15
    ]
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
# 20. CONTEXTO DA UF
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

contexto1, contexto2, contexto3 = st.columns(
    3
)


with contexto1:

    if pd.notna(
        registro[
            "variacao_percentual"
        ]
    ):

        variacao = registro[
            "variacao_percentual"
        ]

        sinal = (
            "+"
            if variacao > 0
            else ""
        )

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
# 21. EVOLUÇÃO DAS INTERNAÇÕES
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

    dados[
        "uf"
    ] == uf_selecionada

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

    template="plotly_white",

    title_text="",

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

    showlegend=False
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
# 22. EVOLUÇÃO DO IPH
# ============================================================

st.divider()

renderizar_html(
    """
    <div class="section-label">
        EVOLUÇÃO DA PRESSÃO
    </div>
    """
)

renderizar_html(
    f"""
    <div class="section-title">
        Evolução do IPH em {uf_selecionada}
    </div>
    """
)

renderizar_html(
    """
    <div class="section-description">
        Histórico do Índice de Pressão Hospitalar
        ao longo dos períodos disponíveis.
    </div>
    """
)


historico_iph = historico_uf.dropna(

    subset=[
        "indice_pressao"
    ]

).copy()


grafico_iph = px.line(

    historico_iph,

    x="data",

    y="indice_pressao",

    markers=True,

    labels={
        "data": "Período",
        "indice_pressao": "Índice de Pressão"
    }
)


grafico_iph.update_layout(

    template="plotly_white",

    title_text="",

    xaxis_title="",

    yaxis_title="Índice de Pressão Hospitalar",

    hovermode="x unified",

    height=400,

    margin=dict(
        l=30,
        r=30,
        t=25,
        b=25
    ),

    showlegend=False
)


grafico_iph.update_yaxes(

    range=[
        0,
        100
    ],

    gridcolor="#EDF1F5",

    zeroline=False
)


grafico_iph.update_xaxes(
    showgrid=False
)


# Adicionamos linhas de referência para ajudar na
# interpretação das faixas do IPH.
grafico_iph.add_hline(
    y=25,
    line_dash="dot"
)

grafico_iph.add_hline(
    y=50,
    line_dash="dot"
)

grafico_iph.add_hline(
    y=75,
    line_dash="dot"
)


st.plotly_chart(

    grafico_iph,

    use_container_width=True,

    config={
        "displayModeBar": False
    }
)


# ============================================================
# 23. RANKING NACIONAL
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
# 24. AVISO DE INTERPRETAÇÃO
# ============================================================

st.info(
    """
    **Como interpretar o ranking**

    O CareVision analisa **internações registradas no SIH/SUS**
    e **leitos SUS registrados no CNES**.

    Dessa forma, o IPH representa a pressão relativa observada
    na rede analisada e não um indicador geral de vulnerabilidade
    social, qualidade da saúde ou da situação hospitalar completa
    de cada estado.

    Por isso, estados com menor infraestrutura ou maior
    vulnerabilidade não necessariamente aparecerão nas primeiras
    posições do ranking.
    """
)


# ============================================================
# 25. TOP 10
# ============================================================

top_10 = (

    ranking_valido

    .head(10)

    .copy()
)


top_10 = top_10.sort_values(

    "indice_pressao",

    ascending=True
)


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

    template="plotly_white",

    title_text="",

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
    )
)


grafico_ranking.update_xaxes(

    range=[
        0,
        100
    ],

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
# 26. MAPA DO BRASIL
# ============================================================

st.divider()

renderizar_html(
    """
    <div class="section-label">
        DISTRIBUIÇÃO ESPACIAL
    </div>
    """
)

renderizar_html(
    f"""
    <div class="section-title">
        Mapa da Pressão Hospitalar • {periodo_selecionado}
    </div>
    """
)

renderizar_html(
    """
    <div class="section-description">
        Distribuição geográfica do nível de pressão hospitalar
        entre as Unidades da Federação.
    </div>
    """
)


# ============================================================
# 27. PREPARAÇÃO DOS DADOS DO MAPA
# ============================================================

# O mapa utiliza todos os estados do período selecionado.
dados_mapa = ranking_periodo.copy()


# Substitui classificações ausentes por "Sem dado".
#
# Isso é especialmente importante em períodos nos quais
# alguma UF não possui informações suficientes para
# o cálculo do IPH.
dados_mapa[
    "nivel_pressao"
] = dados_mapa[
    "nivel_pressao"
].fillna(
    "Sem dado"
)


# ============================================================
# 28. CONSTRUÇÃO DO MAPA
# ============================================================

if geojson_estados is not None:

    grafico_mapa = px.choropleth(

        dados_mapa,

        # Arquivo com os polígonos dos estados.
        geojson=geojson_estados,

        # A coluna "uf" contém o nome completo dos estados.
        locations="uf",

        # Dentro do GeoJSON criamos anteriormente a
        # propriedade padronizada "carevision_uf".
        featureidkey=
            "properties.carevision_uf",

        # O mapa é colorido de acordo com o nível
        # de pressão hospitalar.
        color="nivel_pressao",

        # Mantemos exatamente as mesmas cores utilizadas
        # nos demais gráficos do dashboard.
        color_discrete_map=cores_pressao,

        # Ao passar o mouse sobre um estado, o nome da UF
        # aparece em destaque.
        hover_name="uf",

        # Informações adicionais exibidas no tooltip.
        hover_data={

            "indice_pressao": ":.1f",

            "internacoes": ":,.0f",

            "leitos_sus": ":,.0f",

            "internacoes_por_leito": ":.2f",

            "internacoes_100mil": ":.2f",

            "leitos_100mil": ":.2f",

            "nivel_pressao": True
        },

        labels={

            "uf":
                "UF",

            "indice_pressao":
                "Índice de Pressão",

            "nivel_pressao":
                "Nível de Pressão",

            "internacoes":
                "Internações",

            "leitos_sus":
                "Leitos SUS",

            "internacoes_por_leito":
                "Internações / leito",

            "internacoes_100mil":
                "Internações / 100 mil",

            "leitos_100mil":
                "Leitos SUS / 100 mil"
        },

        # Ordem lógica da legenda.
        category_orders={

            "nivel_pressao": [

                "Baixa",

                "Moderada",

                "Alta",

                "Crítica",

                "Sem dado"
            ]
        }
    )


    # ========================================================
    # AJUSTES GEOGRÁFICOS
    # ========================================================

    grafico_mapa.update_geos(

        # Ajusta automaticamente a visualização aos
        # polígonos presentes no GeoJSON.
        fitbounds="locations",

        # Remove o mapa-múndi ao redor,
        # deixando apenas o Brasil em destaque.
        visible=False,

        # Fundo transparente/claro.
        bgcolor="rgba(0,0,0,0)"
    )


    # ========================================================
    # AJUSTES VISUAIS
    # ========================================================

    grafico_mapa.update_layout(

        template="plotly_white",

        title_text="",

        height=650,

        margin=dict(
            l=0,
            r=0,
            t=50,
            b=0
        ),

        legend_title_text=
            "Nível de pressão",

        legend=dict(

            orientation="h",

            yanchor="bottom",

            y=1.01,

            xanchor="center",

            x=0.5
        ),

        paper_bgcolor=
            "rgba(0,0,0,0)",

        plot_bgcolor=
            "rgba(0,0,0,0)"
    )


    # Deixa as divisões entre estados um pouco mais visíveis.
    grafico_mapa.update_traces(

        marker_line_color="#FFFFFF",

        marker_line_width=1.2
    )


    st.plotly_chart(

        grafico_mapa,

        use_container_width=True,

        config={
            "displayModeBar": False
        }
    )


    st.caption(
        "As cores representam a classificação do IPH no período "
        "selecionado. UFs sem informações suficientes para o cálculo "
        "do índice são apresentadas em cinza."
    )


else:

    st.warning(
        """
        O mapa não pôde ser carregado.

        Verifique se o arquivo
        `data/geo/estados_brasil.geojson`
        está presente no repositório.
        """
    )


# ============================================================
# 29. EXPLICABILIDADE DO IPH
# ============================================================

st.divider()

renderizar_html(
    """
    <div class="section-label">
        EXPLICABILIDADE DO MODELO
    </div>
    """
)

renderizar_html(
    f"""
    <div class="section-title">
        O que influencia o IPH de {uf_selecionada}?
    </div>
    """
)

renderizar_html(
    """
    <div class="section-description">
        Componentes utilizados na construção do
        Índice de Pressão Hospitalar.
    </div>
    """
)


# ============================================================
# 30. IDENTIFICAÇÃO DOS COMPONENTES DO IPH
# ============================================================

coluna_score_capacidade = None
coluna_score_populacao = None
coluna_score_tendencia = None


possiveis_capacidade = [

    "score_demanda_capacidade",

    "score_internacoes_por_leito",

    "score_capacidade"
]


possiveis_populacao = [

    "score_demanda_populacao",

    "score_internacoes_100mil",

    "score_populacao"
]


possiveis_tendencia = [

    "score_tendencia",

    "score_variacao",

    "score_variacao_percentual"
]


for coluna in possiveis_capacidade:

    if coluna in dados.columns:

        coluna_score_capacidade = coluna

        break


for coluna in possiveis_populacao:

    if coluna in dados.columns:

        coluna_score_populacao = coluna

        break


for coluna in possiveis_tendencia:

    if coluna in dados.columns:

        coluna_score_tendencia = coluna

        break


# ============================================================
# 31. GRÁFICO DOS COMPONENTES
# ============================================================

if (
    coluna_score_capacidade is not None
    and coluna_score_populacao is not None
    and coluna_score_tendencia is not None
):

    valor_capacidade = registro[
        coluna_score_capacidade
    ]

    valor_populacao = registro[
        coluna_score_populacao
    ]

    valor_tendencia = registro[
        coluna_score_tendencia
    ]


    valores_scores = [

        valor_capacidade,

        valor_populacao,

        valor_tendencia
    ]


    # Caso os scores estejam na escala 0–1,
    # convertemos para escala 0–100 apenas
    # para facilitar a leitura visual.
    if max(
        [
            valor
            for valor in valores_scores
            if pd.notna(valor)
        ],
        default=0
    ) <= 1:

        valores_scores = [

            valor * 100
            if pd.notna(valor)
            else valor

            for valor in valores_scores
        ]


    dados_componentes = pd.DataFrame(
        {

            "Componente": [

                "Demanda / capacidade",

                "Demanda / população",

                "Tendência recente"
            ],

            "Score": valores_scores,

            "Peso": [

                "50%",

                "30%",

                "20%"
            ]
        }
    )


    grafico_componentes = px.bar(

        dados_componentes,

        x="Componente",

        y="Score",

        text="Peso",

        labels={

            "Score":
                "Score relativo",

            "Componente":
                ""
        }
    )


    grafico_componentes.update_traces(

        texttemplate=
            "Peso: %{text}",

        textposition=
            "outside"
    )


    grafico_componentes.update_layout(

        template="plotly_white",

        title_text="",

        yaxis_title=
            "Score relativo",

        xaxis_title="",

        height=410,

        margin=dict(
            l=30,
            r=30,
            t=45,
            b=30
        ),

        showlegend=False
    )


    grafico_componentes.update_yaxes(

        range=[
            0,
            110
        ],

        gridcolor="#EDF1F5",

        zeroline=False
    )


    st.plotly_chart(

        grafico_componentes,

        use_container_width=True,

        config={
            "displayModeBar": False
        }
    )


    st.caption(
        "Os componentes mostram a posição relativa da UF "
        "em cada dimensão utilizada pelo índice. Os pesos "
        "de 50%, 30% e 20% representam a participação de "
        "cada dimensão no cálculo do IPH."
    )


else:

    st.info(
        """
        Os componentes intermediários utilizados no cálculo
        do IPH não estão disponíveis nesta versão da base
        carregada pelo dashboard.

        O IPH continua sendo calculado com 50% de
        demanda/capacidade, 30% de demanda/população e
        20% de tendência recente.
        """
    )


# ============================================================
# 32. DEMANDA × CAPACIDADE
# ============================================================

st.divider()

renderizar_html(
    """
    <div class="section-label">
        DEMANDA E CAPACIDADE
    </div>
    """
)

renderizar_html(
    """
    <div class="section-title">
        Demanda hospitalar × disponibilidade de leitos
    </div>
    """
)

renderizar_html(
    f"""
    <div class="section-description">
        Comparação entre as UFs em {periodo_selecionado}
        considerando indicadores normalizados pela população.
    </div>
    """
)


dados_dispersao = ranking_periodo.dropna(

    subset=[

        "internacoes_100mil",

        "leitos_100mil",

        "indice_pressao"
    ]

).copy()


grafico_dispersao = px.scatter(

    dados_dispersao,

    x="leitos_100mil",

    y="internacoes_100mil",

    size="indice_pressao",

    color="nivel_pressao",

    hover_name="uf",

    color_discrete_map=
        cores_pressao,

    size_max=35,

    labels={

        "leitos_100mil":
            "Leitos SUS por 100 mil habitantes",

        "internacoes_100mil":
            "Internações por 100 mil habitantes",

        "indice_pressao":
            "IPH",

        "nivel_pressao":
            "Nível"
    }
)


grafico_dispersao.update_layout(

    template="plotly_white",

    title_text="",

    height=500,

    xaxis_title=
        "Leitos SUS por 100 mil habitantes",

    yaxis_title=
        "Internações por 100 mil habitantes",

    legend_title_text=
        "Nível de pressão",

    margin=dict(
        l=30,
        r=30,
        t=30,
        b=30
    )
)


grafico_dispersao.update_xaxes(

    gridcolor="#EDF1F5",

    zeroline=False
)


grafico_dispersao.update_yaxes(

    gridcolor="#EDF1F5",

    zeroline=False
)


st.plotly_chart(

    grafico_dispersao,

    use_container_width=True,

    config={
        "displayModeBar": False
    }
)


st.caption(
    "Cada ponto representa uma UF. O eixo horizontal mostra "
    "a disponibilidade relativa de leitos SUS e o eixo vertical "
    "mostra as internações por 100 mil habitantes. O tamanho "
    "dos pontos representa o IPH."
)


# ============================================================
# 33. DISTRIBUIÇÃO DAS CLASSIFICAÇÕES
# ============================================================

st.divider()

renderizar_html(
    """
    <div class="section-label">
        PANORAMA NACIONAL
    </div>
    """
)

renderizar_html(
    f"""
    <div class="section-title">
        Distribuição dos níveis de pressão • {periodo_selecionado}
    </div>
    """
)

renderizar_html(
    """
    <div class="section-description">
        Quantidade de UFs em cada faixa do
        Índice de Pressão Hospitalar.
    </div>
    """
)


distribuicao_pressao = (

    ranking_periodo[
        "nivel_pressao"
    ]

    .fillna(
        "Sem dado"
    )

    .value_counts()

    .reindex(
        [

            "Baixa",

            "Moderada",

            "Alta",

            "Crítica",

            "Sem dado"
        ],

        fill_value=0
    )

    .reset_index()
)


distribuicao_pressao.columns = [

    "Nível",

    "Quantidade"
]


grafico_distribuicao = px.bar(

    distribuicao_pressao,

    x="Nível",

    y="Quantidade",

    color="Nível",

    color_discrete_map=
        cores_pressao,

    text="Quantidade"
)


grafico_distribuicao.update_traces(
    textposition="outside"
)


grafico_distribuicao.update_layout(

    template="plotly_white",

    title_text="",

    height=400,

    xaxis_title="",

    yaxis_title=
        "Quantidade de UFs",

    showlegend=False,

    margin=dict(
        l=30,
        r=30,
        t=30,
        b=30
    )
)


grafico_distribuicao.update_xaxes(
    showgrid=False
)


grafico_distribuicao.update_yaxes(

    gridcolor="#EDF1F5",

    zeroline=False
)


st.plotly_chart(

    grafico_distribuicao,

    use_container_width=True,

    config={
        "displayModeBar": False
    }
)


# ============================================================
# 34. TENDÊNCIA RECENTE
# ============================================================

st.divider()

renderizar_html(
    """
    <div class="section-label">
        TENDÊNCIA RECENTE
    </div>
    """
)

renderizar_html(
    f"""
    <div class="section-title">
        Maiores mudanças nas internações • {periodo_selecionado}
    </div>
    """
)

renderizar_html(
    """
    <div class="section-description">
        UFs com maiores aumentos e reduções percentuais
        de internações em relação ao mês anterior.
    </div>
    """
)


variacoes_validas = ranking_periodo.dropna(

    subset=[
        "variacao_percentual"
    ]

).copy()


# ============================================================
# 35. TOP 5 AUMENTOS
# ============================================================

maiores_aumentos = (

    variacoes_validas

    .sort_values(
        "variacao_percentual",
        ascending=False
    )

    .head(5)

    .sort_values(
        "variacao_percentual",
        ascending=True
    )
)


# ============================================================
# 36. TOP 5 REDUÇÕES
# ============================================================

maiores_quedas = (

    variacoes_validas

    .sort_values(
        "variacao_percentual",
        ascending=True
    )

    .head(5)

    .sort_values(
        "variacao_percentual",
        ascending=False
    )
)


col_aumento, col_queda = st.columns(
    2
)


# ============================================================
# 37. GRÁFICO DE AUMENTOS
# ============================================================

with col_aumento:

    st.markdown(
        "#### 📈 Maiores aumentos"
    )

    grafico_aumentos = px.bar(

        maiores_aumentos,

        x="variacao_percentual",

        y="uf",

        orientation="h",

        text="variacao_percentual",

        labels={

            "variacao_percentual":
                "Variação (%)",

            "uf":
                ""
        }
    )


    grafico_aumentos.update_traces(

        texttemplate=
            "%{text:.1f}%",

        textposition=
            "outside"
    )


    grafico_aumentos.update_layout(

        template="plotly_white",

        title_text="",

        xaxis_title=
            "Variação mensal (%)",

        yaxis_title="",

        height=350,

        showlegend=False,

        margin=dict(
            l=20,
            r=50,
            t=10,
            b=20
        )
    )


    grafico_aumentos.update_xaxes(

        gridcolor="#EDF1F5",

        zeroline=False
    )


    grafico_aumentos.update_yaxes(
        showgrid=False
    )


    st.plotly_chart(

        grafico_aumentos,

        use_container_width=True,

        config={
            "displayModeBar": False
        }
    )


# ============================================================
# 38. GRÁFICO DE REDUÇÕES
# ============================================================

with col_queda:

    st.markdown(
        "#### 📉 Maiores reduções"
    )

    grafico_quedas = px.bar(

        maiores_quedas,

        x="variacao_percentual",

        y="uf",

        orientation="h",

        text="variacao_percentual",

        labels={

            "variacao_percentual":
                "Variação (%)",

            "uf":
                ""
        }
    )


    grafico_quedas.update_traces(

        texttemplate=
            "%{text:.1f}%",

        textposition=
            "outside"
    )


    grafico_quedas.update_layout(

        template="plotly_white",

        title_text="",

        xaxis_title=
            "Variação mensal (%)",

        yaxis_title="",

        height=350,

        showlegend=False,

        margin=dict(
            l=20,
            r=50,
            t=10,
            b=20
        )
    )


    grafico_quedas.update_xaxes(

        gridcolor="#EDF1F5",

        zeroline=False
    )


    grafico_quedas.update_yaxes(
        showgrid=False
    )


    st.plotly_chart(

        grafico_quedas,

        use_container_width=True,

        config={
            "displayModeBar": False
        }
    )


# ============================================================
# 39. TABELA ANALÍTICA NACIONAL
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

    dados[
        "periodo"
    ] == periodo_selecionado

][

    [

        "uf",

        "internacoes",

        "leitos_sus",

        "internacoes_100mil",

        "leitos_100mil",

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

        "internacoes_100mil":
            "Internações / 100 mil",

        "leitos_100mil":
            "Leitos SUS / 100 mil",

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

    height=500,

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


        "Internações / 100 mil":

            st.column_config.NumberColumn(

                "Internações / 100 mil",

                format="%.2f"
            ),


        "Leitos SUS / 100 mil":

            st.column_config.NumberColumn(

                "Leitos SUS / 100 mil",

                format="%.2f"
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
                    "Índice experimental do "
                    "CareVision em escala de 0 a 100."
                ),

                min_value=0,

                max_value=100,

                format="%.1f"
            )
    }
)


# ============================================================
# 40. DOWNLOAD DA TABELA
# ============================================================

csv_download = tabela_nacional.to_csv(

    index=False,

    encoding="utf-8-sig"
)


st.download_button(

    label=
        "⬇️ Baixar dados do período",

    data=
        csv_download,

    file_name=
        f"carevision_{periodo_selecionado.replace('/', '_')}.csv",

    mime=
        "text/csv"
)


# ============================================================
# 41. METODOLOGIA E LIMITAÇÕES
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

        **50% — demanda em relação à capacidade**

        Relação entre internações hospitalares registradas
        e leitos SUS disponíveis.

        **30% — demanda em relação à população**

        Internações hospitalares registradas por
        100 mil habitantes.

        **20% — tendência recente**

        Variação percentual das internações em relação
        ao mês anterior.

        Os componentes são comparados entre as UFs dentro
        de cada período e combinados em uma escala de
        **0 a 100**.

        ---

        ### Classificação

        🟢 **Baixa:** abaixo de 25

        🟡 **Moderada:** 25 a abaixo de 50

        🟠 **Alta:** 50 a abaixo de 75

        🔴 **Crítica:** 75 a 100

        ---

        ### Interpretação dos resultados

        O CareVision utiliza internações registradas no
        **SIH/SUS** e leitos SUS registrados no **CNES**.

        Portanto, o IPH representa a pressão relativa observada
        na rede analisada e não deve ser interpretado como um
        indicador geral de qualidade da saúde, vulnerabilidade
        social ou situação hospitalar completa de um estado.

        Estados com menor infraestrutura hospitalar ou maior
        vulnerabilidade social não necessariamente apresentarão
        maior IPH.

        ---

        ### Limitações

        A relação **internações por leito** é utilizada como
        uma proxy de carga hospitalar.

        Ela **não representa a taxa real de ocupação hospitalar**.

        Para calcular ocupação seriam necessários dados
        adicionais como pacientes-dia e leitos-dia disponíveis.

        As internações utilizadas são provenientes do
        **SIH/SUS** e representam registros vinculados ao
        Sistema Único de Saúde.

        Os dados de leitos são provenientes do **CNES**.

        A população utilizada corresponde às estimativas
        populacionais do **IBGE**.

        A estimativa populacional de 2025 também foi utilizada
        nos meses de 2026 como simplificação metodológica do MVP.

        O IPH é um indicador desenvolvido especificamente para
        o CareVision e **não corresponde a um índice oficial**
        do Ministério da Saúde, DATASUS, CNES ou IBGE.

        O índice também não possui finalidade clínica.
        """
    )


# ============================================================
# 42. RODAPÉ
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

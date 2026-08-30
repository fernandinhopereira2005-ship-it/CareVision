
# ============================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================

# Streamlit será utilizado para construir a interface.
import streamlit as st

# Pandas será utilizado para carregar e filtrar os dados.
import pandas as pd

# Plotly Express será utilizado para criar
# os gráficos interativos do CareVision.
import plotly.express as px


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
# 10. EVOLUÇÃO HISTÓRICA DAS INTERNAÇÕES
# ============================================================

# Selecionamos todos os meses disponíveis para a UF
# escolhida pelo usuário no filtro lateral.
historico_uf = dados[
    dados["uf"] == uf_selecionada
].copy()

# Organizamos os registros em ordem cronológica.
historico_uf = historico_uf.sort_values("data")


# ------------------------------------------------------------
# TÍTULO DO GRÁFICO
# ------------------------------------------------------------

st.divider()

st.subheader(
    f"📊 Evolução das internações — {uf_selecionada}"
)


# ------------------------------------------------------------
# CRIAÇÃO DO GRÁFICO
# ------------------------------------------------------------

# Criamos um gráfico de linha interativo.
#
# Cada ponto representa o número de internações
# registrado em determinado mês.

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


# ------------------------------------------------------------
# CONFIGURAÇÃO DO GRÁFICO
# ------------------------------------------------------------

# O modo "x unified" permite visualizar os valores
# ao passar o mouse sobre determinado período.

# ============================================================
# CONFIGURAÇÃO VISUAL DO GRÁFICO
# ============================================================

# Configuramos os elementos visuais do gráfico.
grafico_internacoes.update_layout(

    # Remove qualquer título interno do Plotly.
    # O título da seção já aparece acima pelo Streamlit.
    title_text="",

    # Define os nomes dos eixos.
    xaxis_title="Período",
    yaxis_title="Internações",

    # Exibe as informações agrupadas ao passar
    # o mouse sobre determinado período.
    hovermode="x unified"
)


# ------------------------------------------------------------
# EXIBIÇÃO NO DASHBOARD
# ------------------------------------------------------------

# Exibe o gráfico utilizando toda a largura
# disponível na página do CareVision.

st.plotly_chart(
    grafico_internacoes,
    use_container_width=True
)
# ============================================================
# 11. RANKING NACIONAL DE PRESSÃO HOSPITALAR
# ============================================================

# Vamos comparar todas as UFs dentro do período
# selecionado pelo usuário na barra lateral.
#
# Diferente do gráfico histórico, que usa apenas uma UF,
# este ranking considera todas as UFs disponíveis naquele mês.

ranking_periodo = dados[
    dados["periodo"] == periodo_selecionado
].copy()


# ------------------------------------------------------------
# REMOÇÃO DE REGISTROS SEM ÍNDICE
# ------------------------------------------------------------

# Alguns registros podem não possuir Índice de Pressão
# calculado, como acontece quando faltam dados de internações.
#
# Para o ranking, utilizamos somente registros com
# indice_pressao válido.

ranking_periodo = ranking_periodo.dropna(
    subset=["indice_pressao"]
)


# ------------------------------------------------------------
# ORDENAÇÃO DO RANKING
# ------------------------------------------------------------

# Ordenamos da maior para a menor pressão hospitalar.

ranking_periodo = ranking_periodo.sort_values(
    "indice_pressao",
    ascending=False
)


# ------------------------------------------------------------
# SELEÇÃO DAS 10 UFs COM MAIOR ÍNDICE
# ------------------------------------------------------------

# Para manter o dashboard visualmente claro,
# mostramos apenas as 10 UFs com maior Índice de Pressão.

top_10 = ranking_periodo.head(10).copy()


# ------------------------------------------------------------
# ORGANIZAÇÃO PARA O GRÁFICO HORIZONTAL
# ------------------------------------------------------------

# Invertemos a ordem das 10 UFs para que
# a maior pontuação apareça no topo do gráfico horizontal.

top_10 = top_10.sort_values(
    "indice_pressao",
    ascending=True
)


# ------------------------------------------------------------
# TÍTULO DA SEÇÃO
# ------------------------------------------------------------

st.divider()

st.subheader(
    f"🏆 Ranking de Pressão Hospitalar — {periodo_selecionado}"
)

st.caption(
    "Top 10 Unidades da Federação com maior Índice de Pressão "
    "Hospitalar no período selecionado."
)


# ------------------------------------------------------------
# CRIAÇÃO DO GRÁFICO
# ------------------------------------------------------------

# Criamos um gráfico horizontal.
#
# Eixo X:
# Índice de Pressão Hospitalar.
#
# Eixo Y:
# Unidade da Federação.
#
# A classificação de pressão também será utilizada
# para diferenciar visualmente as barras.

grafico_ranking = px.bar(
    top_10,
    x="indice_pressao",
    y="uf",
    orientation="h",
    color="nivel_pressao",

    # Informações adicionais exibidas quando
    # o usuário passa o mouse sobre uma barra.
    hover_data={
        "internacoes": ":,.0f",
        "leitos_sus": ":,.0f",
        "internacoes_por_leito": ":.2f",
        "variacao_percentual": ":.2f",
        "indice_pressao": ":.1f"
    },

    labels={
        "indice_pressao": "Índice de Pressão",
        "uf": "UF",
        "nivel_pressao": "Nível de Pressão",
        "internacoes": "Internações",
        "leitos_sus": "Leitos SUS",
        "internacoes_por_leito": "Internações / leito",
        "variacao_percentual": "Variação mensal (%)"
    }
)


# ------------------------------------------------------------
# CONFIGURAÇÃO VISUAL
# ------------------------------------------------------------

grafico_ranking.update_layout(

    # Remove o título interno.
    # Já usamos um título do Streamlit acima.
    title_text="",

    # Define os nomes dos eixos.
    xaxis_title="Índice de Pressão Hospitalar",
    yaxis_title="",

    # Posiciona a legenda acima do gráfico.
    legend_title_text="Nível de Pressão"
)


# ------------------------------------------------------------
# ESCALA DO ÍNDICE
# ------------------------------------------------------------

# Como o IPH varia de 0 a 100,
# fixamos o eixo X nessa mesma escala.
#
# Isso facilita a comparação visual entre períodos.

grafico_ranking.update_xaxes(
    range=[0, 100]
)


# ------------------------------------------------------------
# EXIBIÇÃO DO GRÁFICO
# ------------------------------------------------------------

st.plotly_chart(
    grafico_ranking,
    use_container_width=True
)
# ============================================================
# 12. TABELA ANALÍTICA NACIONAL
# ============================================================

# A tabela permite visualizar todas as Unidades da Federação
# no período selecionado, não apenas as 10 primeiras do ranking.
#
# Ela complementa o gráfico e ajuda o usuário a analisar
# os indicadores de forma mais detalhada.

st.divider()

st.subheader(
    f"📋 Visão Analítica Nacional — {periodo_selecionado}"
)


# ------------------------------------------------------------
# PREPARAÇÃO DOS DADOS
# ------------------------------------------------------------

# Selecionamos apenas as colunas mais importantes
# para a análise dentro do dashboard.

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


# ------------------------------------------------------------
# ORDENAÇÃO
# ------------------------------------------------------------

# Ordenamos da maior para a menor pressão hospitalar.
#
# Os registros sem índice, quando existirem,
# aparecerão ao final da tabela.

tabela_nacional = tabela_nacional.sort_values(
    "indice_pressao",
    ascending=False,
    na_position="last"
)


# ------------------------------------------------------------
# RENOMEAÇÃO DAS COLUNAS
# ------------------------------------------------------------

# Renomeamos as colunas para deixar os títulos
# mais amigáveis para o usuário do dashboard.

tabela_nacional = tabela_nacional.rename(
    columns={
        "uf": "UF",
        "internacoes": "Internações",
        "leitos_sus": "Leitos SUS",
        "internacoes_por_leito": "Internações / leito",
        "variacao_percentual": "Variação mensal (%)",
        "indice_pressao": "Índice de Pressão",
        "nivel_pressao": "Nível de Pressão"
    }
)


# ------------------------------------------------------------
# EXIBIÇÃO DA TABELA
# ------------------------------------------------------------

# O dataframe do Streamlit permite rolagem e ordenação
# diretamente pelo usuário.
#
# hide_index=True:
# remove a coluna numérica de índice do Pandas.
#
# use_container_width=True:
# utiliza toda a largura disponível.

st.dataframe(
    tabela_nacional,
    use_container_width=True,
    hide_index=True
)
# ============================================================
# 13. OBSERVAÇÃO METODOLÓGICA
# ============================================================

st.divider()

st.caption(
    "O Índice de Pressão Hospitalar é um indicador analítico "
    "experimental desenvolvido para o MVP CareVision. "
    "Internações por leito é utilizada como proxy de carga "
    "hospitalar e não representa taxa de ocupação."
)

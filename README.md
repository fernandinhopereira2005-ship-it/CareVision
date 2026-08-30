# 🏥 CareVision

## Monitoramento Analítico de Pressão Hospitalar

O **CareVision** é um MVP de apoio à análise e à tomada de decisão na área da saúde, desenvolvido a partir da integração de dados públicos brasileiros.

A solução permite acompanhar indicadores relacionados à demanda hospitalar e à disponibilidade de leitos SUS nas Unidades da Federação, oferecendo uma visão comparativa da pressão relativa sobre o sistema hospitalar.

O projeto utiliza dados públicos do **DATASUS (SIH/SUS e CNES)** e estimativas populacionais do **IBGE**.

---

## 🎯 Problema

Gestores e profissionais envolvidos no planejamento da saúde precisam analisar diferentes informações para compreender a relação entre demanda hospitalar e capacidade disponível.

Esses dados podem estar distribuídos em diferentes bases públicas, dificultando sua integração e interpretação.

O CareVision busca contribuir para esse problema através da consolidação dos dados em uma solução analítica única e interativa.

---

## 💡 Solução proposta

O CareVision integra informações sobre:

- internações hospitalares;
- leitos SUS disponíveis;
- população estimada;
- evolução mensal das internações;
- internações por 100 mil habitantes;
- leitos por 100 mil habitantes;
- relação entre internações e leitos;
- Índice de Pressão Hospitalar;
- classificação do nível de pressão.

Essas informações são disponibilizadas através de um **dashboard interativo desenvolvido em Streamlit**.

---

## 📊 Funcionalidades do MVP

O dashboard atualmente permite:

- selecionar o período de análise;
- selecionar uma Unidade da Federação;
- visualizar o número de internações;
- visualizar a quantidade de leitos SUS;
- acompanhar a relação entre internações e leitos;
- visualizar o Índice de Pressão Hospitalar;
- identificar o nível de pressão;
- acompanhar a variação mensal das internações;
- analisar a evolução histórica das internações;
- comparar as UFs através de um ranking nacional;
- consultar uma tabela analítica com os indicadores das Unidades da Federação.

---

## 🗂️ Fontes de dados

### SIH/SUS — Sistema de Informações Hospitalares

Utilizado para obtenção dos dados de internações hospitalares financiadas pelo SUS.

Fonte: DATASUS — Ministério da Saúde.

### CNES — Cadastro Nacional de Estabelecimentos de Saúde

Utilizado para obtenção da quantidade de leitos SUS.

Fonte: DATASUS — Ministério da Saúde.

### IBGE — Instituto Brasileiro de Geografia e Estatística

Utilizado para obtenção das estimativas populacionais de 2025 das Unidades da Federação.

---

## 🏗️ Arquitetura da solução

O fluxo simplificado do CareVision é:

```text
DATASUS - SIH/SUS
        │
        ├─────────────┐
        │             │
DATASUS - CNES        │
        │             │
        ├─────────────┤
        │             ▼
IBGE ─────────> Coleta dos dados
                      │
                      ▼
              Tratamento em Python
                      │
                      ▼
          Padronização e integração
                      │
                      ▼
             Cálculo de indicadores
                      │
                      ▼
       Índice de Pressão Hospitalar
                      │
                      ▼
          Base analítica consolidada
                      │
                      ▼
            Dashboard Streamlit
                      │
                      ▼
           Apoio à análise gerencial
```

---

## 🔄 Pipeline de dados

O pipeline desenvolvido para o MVP segue as seguintes etapas:

1. coleta dos dados públicos;
2. importação das bases para ambiente Python;
3. limpeza e padronização;
4. transformação dos dados para formato analítico;
5. integração das bases através da Unidade da Federação e período;
6. tratamento de valores ausentes;
7. cálculo dos indicadores;
8. construção do Índice de Pressão Hospitalar;
9. geração da base analítica final;
10. consumo dos dados pelo dashboard.

---

## 📈 Indicadores utilizados

### Internações por 100 mil habitantes

Permite comparar a demanda hospitalar entre estados com populações diferentes.

```text
Internações por 100 mil =
(Internações / População) × 100.000
```

### Leitos SUS por 100 mil habitantes

Representa a disponibilidade relativa de leitos SUS em relação à população.

```text
Leitos por 100 mil =
(Leitos SUS / População) × 100.000
```

### Internações por leito

Utilizado no MVP como uma **proxy de carga hospitalar**.

```text
Internações por leito =
Internações / Leitos SUS
```

> **Importante:** este indicador não representa taxa de ocupação hospitalar.

### Variação mensal das internações

Permite identificar crescimento ou redução da demanda em relação ao mês anterior.

```text
Variação (%) =
((Internações atuais - Internações anteriores)
 / Internações anteriores) × 100
```

---

## 🧠 Índice de Pressão Hospitalar

O CareVision utiliza um **Índice de Pressão Hospitalar (IPH)** desenvolvido especificamente para o MVP.

O indicador combina dimensões relacionadas a:

- demanda em relação à capacidade;
- demanda em relação à população;
- tendência mensal das internações.

O resultado é normalizado em uma escala de:

```text
0 ─────────────────────────────── 100
Menor pressão              Maior pressão
```

A partir do índice, as UFs são classificadas em níveis de pressão:

- 🟢 Baixa
- 🟡 Moderada
- 🟠 Alta
- 🔴 Crítica
- ⚪ Sem dado

O índice possui finalidade **analítica e experimental** e não representa um indicador clínico oficialmente validado.

---

## 🖥️ Tecnologias utilizadas

- Python
- Pandas
- Plotly
- Streamlit
- Google Colab
- GitHub

---

## 📁 Estrutura do repositório

```text
CareVision/
│
├── app.py
│   └── Aplicação principal do dashboard
│
├── carevision_base_final.csv
│   └── Base analítica utilizada pelo MVP
│
├── requirements.txt
│   └── Dependências necessárias para execução
│
└── README.md
    └── Documentação do projeto
```

---

## ▶️ Executando o projeto

Clone o repositório:

```bash
git clone <URL-DO-REPOSITORIO>
```

Entre na pasta:

```bash
cd CareVision
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Execute a aplicação:

```bash
streamlit run app.py
```

---

## 📦 Dependências

As principais dependências estão registradas no arquivo `requirements.txt`:

```text
streamlit
pandas
plotly
```

---

## ⚠️ Limitações do MVP

O projeto possui algumas limitações importantes.

Os dados de internações utilizados são provenientes do **SIH/SUS**, portanto representam internações registradas no âmbito do sistema utilizado e não necessariamente todas as internações realizadas no Brasil.

A relação **internações por leito** é utilizada somente como proxy de carga hospitalar e não deve ser interpretada como taxa de ocupação.

A população utilizada corresponde à estimativa populacional de **2025 do IBGE** e foi mantida como referência populacional durante o período analisado no MVP.

O Índice de Pressão Hospitalar é um indicador experimental desenvolvido para fins analíticos e acadêmicos e não substitui indicadores oficiais, avaliações clínicas ou sistemas operacionais de gestão hospitalar.

---

## 🚀 Próximas evoluções

Entre possíveis evoluções futuras do CareVision estão:

- mapa interativo do Brasil com nível de pressão por UF;
- inclusão de novas séries históricas;
- análise regional;
- novos indicadores de capacidade hospitalar;
- automatização da atualização dos dados;
- modelos preditivos de demanda;
- alertas para alterações relevantes nos indicadores.

---

## 🎓 Contexto acadêmico

Projeto desenvolvido como MVP para a **Sprint 2 do Enterprise Challenge**, com foco na construção de uma solução baseada em dados, contemplando coleta, processamento, análise, visualização e disponibilização da solução.

---

## 📌 Observação

O CareVision é um protótipo acadêmico de apoio analítico.

Os resultados apresentados devem ser interpretados considerando as limitações das bases públicas utilizadas e da metodologia experimental desenvolvida para o MVP.

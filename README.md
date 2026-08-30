# 🏥 CareVision

## Monitoramento Analítico de Pressão Hospitalar

O **CareVision** é um MVP de apoio à análise e à tomada de decisão na área da saúde, desenvolvido a partir da integração, tratamento e visualização de dados públicos brasileiros.

A solução busca transformar diferentes bases públicas de saúde em informações analíticas de fácil interpretação, permitindo acompanhar indicadores relacionados à demanda hospitalar e à disponibilidade de leitos SUS nas Unidades da Federação.

O projeto utiliza dados do **DATASUS**, por meio do **SIH/SUS** e do **CNES**, combinados com estimativas populacionais do **IBGE**.

A partir dessas informações, o CareVision constrói indicadores comparativos e um **Índice de Pressão Hospitalar (IPH)** experimental, disponibilizando os resultados em um dashboard interativo desenvolvido em **Streamlit**.

---

# 🎯 Problema

A análise da situação hospitalar exige a combinação de diferentes informações, como volume de internações, disponibilidade de leitos e população atendida.

Embora essas informações estejam disponíveis em bases públicas, elas são disponibilizadas por diferentes sistemas e formatos, o que pode dificultar sua integração, comparação e interpretação.

Nesse contexto, surge a necessidade de uma solução capaz de:

- integrar diferentes fontes públicas;
- padronizar os dados;
- construir indicadores comparáveis;
- acompanhar a evolução da demanda;
- identificar situações de maior pressão relativa;
- disponibilizar as informações de maneira visual e interativa.

O **CareVision** foi desenvolvido como uma proposta de solução para esse problema.

---

# 💡 Solução proposta

O CareVision implementa um pipeline de dados responsável por coletar, tratar, integrar e transformar informações provenientes de três fontes principais:

- **SIH/SUS:** internações hospitalares;
- **CNES:** quantidade de leitos SUS;
- **IBGE:** população estimada das Unidades da Federação.

Após o processamento, essas informações são consolidadas em uma única base analítica.

A partir dela são calculados indicadores relacionados à demanda, capacidade hospitalar, população e tendência mensal das internações.

Os resultados são disponibilizados através de um **dashboard interativo**, permitindo explorar os dados por período e Unidade da Federação.

---

# 📊 Funcionalidades do MVP

O dashboard do CareVision permite:

- selecionar o período de análise;
- selecionar uma Unidade da Federação;
- visualizar o número de internações;
- visualizar a quantidade de leitos SUS;
- acompanhar a relação entre internações e leitos;
- visualizar o Índice de Pressão Hospitalar;
- identificar o nível de pressão da UF;
- acompanhar a variação mensal das internações;
- analisar a evolução histórica das internações;
- comparar as UFs através de um ranking nacional;
- visualizar as UFs com maior pressão relativa;
- consultar uma tabela analítica nacional;
- comparar indicadores entre as diferentes Unidades da Federação.

---

# 🗂️ Fontes de dados

## 1. SIH/SUS — Sistema de Informações Hospitalares

A base do **SIH/SUS**, disponibilizada pelo DATASUS, foi utilizada para obtenção do número de internações hospitalares registradas no período analisado.

**Fonte:** DATASUS — Ministério da Saúde.

**Variável principal utilizada:**

```text
Internações hospitalares por Unidade da Federação e período
```

---

## 2. CNES — Cadastro Nacional de Estabelecimentos de Saúde

A base do **CNES** foi utilizada para obtenção da quantidade de leitos SUS disponível em cada Unidade da Federação.

**Fonte:** DATASUS — Ministério da Saúde.

**Variável principal utilizada:**

```text
Quantidade de leitos SUS por Unidade da Federação e período
```

---

## 3. IBGE — Instituto Brasileiro de Geografia e Estatística

As estimativas populacionais do **IBGE para 2025** foram utilizadas para permitir a construção de indicadores proporcionais à população.

**Variável principal utilizada:**

```text
População estimada por Unidade da Federação
```

---

# 📅 Período analisado

O MVP utiliza dados mensais compreendidos entre:

```text
Junho de 2025
      ↓
Junho de 2026
```

Isso corresponde a:

```text
27 Unidades da Federação × 13 meses = 351 registros
```

A estimativa populacional de 2025 do IBGE é utilizada como referência populacional ao longo do período analisado no MVP.

---

# 🏗️ Arquitetura da solução

A arquitetura do CareVision foi estruturada para representar todo o fluxo entre as fontes de dados e o consumo das informações pelo usuário.

```text
┌─────────────────────┐
│      SIH/SUS        │
│     Internações     │
└──────────┬──────────┘
           │
           │
┌──────────▼──────────┐
│        CNES         │
│     Leitos SUS      │
└──────────┬──────────┘
           │
           │
┌──────────▼──────────┐
│        IBGE         │
│      População      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Bases de dados    │
│       brutas        │
│      data/raw       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      Python +       │
│       Pandas        │
│                     │
│ tratamento_dados.py │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Limpeza e           │
│ padronização        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Integração das      │
│ três fontes         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Cálculo dos         │
│ indicadores         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Índice de Pressão   │
│ Hospitalar — IPH    │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────┐
│ carevision_base_final.csv│
└──────────┬───────────────┘
           │
           ▼
┌─────────────────────┐
│       app.py        │
│ Streamlit + Plotly  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Streamlit Cloud    │
│      Deploy         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Dashboard CareVision│
│                     │
│ Apoio à análise     │
└─────────────────────┘
```

---

# 🔄 Pipeline de dados

O pipeline desenvolvido para o MVP é executado pelo arquivo:

```text
src/tratamento_dados.py
```

O processamento segue o seguinte fluxo:

```text
Bases públicas
      │
      ▼
Armazenamento dos dados brutos
      │
      ▼
Leitura das bases
      │
      ▼
Limpeza
      │
      ▼
Padronização
      │
      ▼
Transformação Wide → Long
      │
      ▼
Padronização temporal
      │
      ▼
Integração SIH + CNES + IBGE
      │
      ▼
Validação
      │
      ▼
Criação dos indicadores
      │
      ▼
Cálculo da variação mensal
      │
      ▼
Índice de Pressão Hospitalar
      │
      ▼
Classificação da pressão
      │
      ▼
Ranking mensal
      │
      ▼
Base analítica consolidada
      │
      ▼
Dashboard
```

---

# 🧹 Tratamento dos dados

Durante o processamento foram realizadas diferentes etapas de preparação das bases.

Entre elas:

- remoção de linhas extras provenientes das exportações do DATASUS;
- identificação das 27 Unidades da Federação;
- separação do código e nome das UFs;
- transformação das bases do formato largo para o formato longo;
- conversão dos valores para formatos numéricos;
- padronização dos períodos;
- criação de uma variável temporal;
- seleção das informações populacionais;
- integração das três fontes;
- verificação de valores ausentes;
- verificação de duplicidades;
- ordenação cronológica;
- construção dos indicadores analíticos.

A base integrada possui uma observação para cada combinação de:

```text
Unidade da Federação + período
```

---

# 📈 Indicadores utilizados

## Internações por 100 mil habitantes

Permite comparar o volume de internações entre UFs com diferentes tamanhos populacionais.

```text
Internações por 100 mil =
(Internações / População) × 100.000
```

---

## Leitos SUS por 100 mil habitantes

Representa a disponibilidade relativa de leitos SUS em relação ao tamanho da população.

```text
Leitos SUS por 100 mil =
(Leitos SUS / População) × 100.000
```

---

## Internações por leito SUS

Relaciona o volume mensal de internações com a quantidade de leitos SUS registrada para a UF.

```text
Internações por leito =
Internações / Leitos SUS
```

Esse indicador é utilizado pelo CareVision como uma **proxy de carga ou pressão relativa sobre a capacidade hospitalar**.

> ⚠️ **Importante:** internações por leito não representa uma taxa de ocupação hospitalar.

Uma taxa de ocupação exigiria informações adicionais, como permanência dos pacientes e utilização efetiva dos leitos ao longo do período.

---

# 📉 Variação mensal das internações

O CareVision também calcula a evolução da demanda em relação ao mês anterior.

Primeiro é identificada a quantidade de internações do período anterior da mesma UF.

Em seguida é calculada a variação absoluta:

```text
Variação absoluta =
Internações atuais - Internações do mês anterior
```

E a variação percentual:

```text
Variação (%) =

((Internações atuais - Internações anteriores)
 / Internações anteriores) × 100
```

Valores positivos representam crescimento das internações em relação ao mês anterior.

Valores negativos representam redução.

---

# 🧠 Índice de Pressão Hospitalar — IPH

Para facilitar a comparação entre as Unidades da Federação, o CareVision utiliza um indicador composto denominado:

## Índice de Pressão Hospitalar (IPH)

O IPH foi desenvolvido especificamente para o MVP e combina três dimensões analíticas.

### 1. Demanda em relação à capacidade — 50%

Utiliza:

```text
Internações por leito SUS
```

Representa a relação entre a demanda hospitalar registrada e a capacidade disponível utilizada no modelo.

---

### 2. Demanda em relação à população — 30%

Utiliza:

```text
Internações por 100 mil habitantes
```

Permite comparar a intensidade relativa das internações considerando diferenças populacionais entre as UFs.

---

### 3. Tendência recente — 20%

Utiliza:

```text
Variação percentual mensal das internações
```

Esse componente permite incorporar ao índice a direção recente da demanda hospitalar.

---

# 🧮 Fórmula do IPH

Para tornar indicadores com escalas diferentes comparáveis, cada componente é transformado em um **ranking percentual entre as UFs dentro do mesmo período**.

Em seguida, os componentes são combinados utilizando os pesos definidos para o MVP:

```text
IPH = [
      0,50 × Score(Demanda / Capacidade)
    + 0,30 × Score(Demanda / População)
    + 0,20 × Score(Tendência)
] × 100
```

O resultado é apresentado em uma escala aproximadamente compreendida entre:

```text
0 ───────────────────────────────────────── 100

Menor pressão relativa          Maior pressão relativa
```

No primeiro período da série histórica não existe um mês anterior para calcular a tendência.

Nesse caso, o componente de tendência recebe o valor **0,5**, utilizado como posição neutra no MVP.

---

# 🚦 Classificação dos níveis de pressão

Após o cálculo do IPH, cada observação é classificada de acordo com as seguintes faixas:

| Índice | Classificação |
|---|---|
| Menor que 25 | 🟢 Baixa |
| 25 até menor que 50 | 🟡 Moderada |
| 50 até menor que 75 | 🟠 Alta |
| 75 até 100 | 🔴 Crítica |
| Índice indisponível | ⚪ Sem dado |

Essas classificações foram definidas para facilitar a interpretação visual dos resultados no MVP.

> ⚠️ As faixas não correspondem a classificações clínicas ou oficiais do Ministério da Saúde.

---

# 🏆 Ranking de pressão

Para cada período, as Unidades da Federação são classificadas de acordo com o Índice de Pressão Hospitalar.

```text
Ranking 1
   ↓
UF com maior pressão relativa no período
```

O dashboard apresenta um **Top 10 nacional**, permitindo identificar rapidamente as UFs com maiores índices no mês selecionado.

O ranking é comparativo e deve ser interpretado como uma ferramenta analítica, e não como diagnóstico da situação hospitalar de uma UF.

---

# 📋 Tabela Analítica Nacional

Além dos indicadores individuais e do ranking, o dashboard apresenta uma tabela consolidada contendo as Unidades da Federação para o período selecionado.

A tabela permite consultar informações como:

- UF;
- internações;
- leitos SUS;
- internações por leito;
- variação mensal;
- Índice de Pressão Hospitalar;
- nível de pressão.

Os registros são organizados do maior para o menor Índice de Pressão Hospitalar.

---

# 🖥️ Dashboard

A interface do CareVision foi construída utilizando **Streamlit** e **Plotly**.

O dashboard utiliza a base:

```text
carevision_base_final.csv
```

e disponibiliza filtros interativos para:

```text
Período
Unidade da Federação
```

A partir desses filtros, o usuário pode explorar os indicadores e acompanhar a evolução dos dados.

---

# 🛠️ Tecnologias utilizadas

| Tecnologia | Utilização |
|---|---|
| Python | Linguagem principal |
| Pandas | Tratamento, integração e análise dos dados |
| OpenPyXL | Leitura da planilha Excel do IBGE |
| Streamlit | Desenvolvimento do dashboard |
| Plotly | Visualizações interativas |
| Google Colab | Desenvolvimento e exploração inicial |
| Git | Versionamento |
| GitHub | Repositório e documentação |
| Streamlit Cloud | Deploy do MVP |

---

# 📁 Estrutura do repositório

```text
CareVision/
│
├── app.py
│   └── Aplicação principal do dashboard Streamlit
│
├── carevision_base_final.csv
│   └── Base analítica consolidada utilizada pelo dashboard
│
├── requirements.txt
│   └── Dependências necessárias para execução do projeto
│
├── data/
│   │
│   └── raw/
│       │
│       ├── 01_internacoes_sih.csv
│       │   └── Base bruta de internações do SIH/SUS
│       │
│       ├── 02_leitos_cnes.csv
│       │   └── Base bruta de leitos SUS do CNES
│       │
│       └── 03_populacao_ibge.xlsx
│           └── Estimativa populacional do IBGE
│
├── src/
│   │
│   └── tratamento_dados.py
│       └── Pipeline de limpeza, integração,
│           criação dos indicadores e exportação
│           da base analítica
│
└── README.md
    └── Documentação técnica do projeto
```

---

# ▶️ Como executar o projeto

## 1. Clonar o repositório

```bash
git clone <URL-DO-REPOSITORIO>
```

---

## 2. Entrar na pasta do projeto

```bash
cd CareVision
```

---

## 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

## 4. Executar o pipeline de tratamento

Caso seja necessário reconstruir a base analítica a partir dos dados brutos:

```bash
python src/tratamento_dados.py
```

O script irá gerar:

```text
carevision_base_final.csv
```

---

## 5. Executar o dashboard

```bash
streamlit run app.py
```

O Streamlit iniciará a aplicação e disponibilizará o dashboard no navegador.

---

# 📦 Dependências

As dependências utilizadas pelo projeto estão registradas no arquivo:

```text
requirements.txt
```

Atualmente:

```text
streamlit
pandas
plotly
openpyxl
```

---

# 🔎 Validação dos dados

O pipeline também executa verificações antes da geração da base final.

Entre as validações realizadas estão:

- dimensões da base integrada;
- quantidade de registros;
- duplicidades por UF e período;
- valores ausentes;
- estatísticas do Índice de Pressão;
- distribuição das classificações.

Para o período completo utilizado no MVP, a estrutura esperada é:

```text
27 UFs × 13 períodos = 351 registros
```

---

# ⚠️ Tratamento de dados ausentes

Valores ausentes provenientes das fontes originais não são automaticamente transformados em zero.

Essa decisão é importante porque:

```text
Ausência de informação ≠ valor igual a zero
```

Quando não existem dados suficientes para calcular o Índice de Pressão Hospitalar, o registro recebe:

```text
Sem dado
```

evitando produzir uma interpretação artificial de baixa pressão.

---

# ⚠️ Limitações do MVP

O CareVision possui limitações que devem ser consideradas na interpretação dos resultados.

### Cobertura das internações

Os dados utilizados são provenientes do **SIH/SUS**.

Portanto, representam as internações registradas no âmbito dessa base e não necessariamente todas as internações realizadas no Brasil.

### Internações por leito

A relação entre internações e leitos é utilizada como uma **proxy analítica de carga hospitalar**.

Ela não representa taxa de ocupação.

### População

A população utilizada corresponde à estimativa populacional de **2025 do IBGE**.

Essa população é utilizada como referência também para os meses de 2026 presentes no MVP.

### Índice de Pressão Hospitalar

O IPH é um indicador experimental desenvolvido para o projeto.

Os pesos:

```text
50% — demanda/capacidade
30% — demanda/população
20% — tendência
```

fazem parte da metodologia analítica proposta para o MVP.

O índice não possui validação clínica e não corresponde a um indicador oficial do DATASUS, Ministério da Saúde ou IBGE.

### Uso da solução

O CareVision deve ser interpretado como uma ferramenta de:

```text
apoio analítico
```

e não como sistema clínico, instrumento diagnóstico ou substituto de sistemas oficiais de gestão hospitalar.

---

# 🚀 Próximas evoluções

Como continuidade do projeto, algumas funcionalidades poderão ser incorporadas futuramente:

- mapa interativo do Brasil com pressão hospitalar por UF;
- ampliação da série histórica;
- atualização automatizada das bases;
- análises por região;
- análises por município;
- inclusão de novos indicadores hospitalares;
- análise de especialidades;
- modelos preditivos de demanda;
- detecção automática de alterações relevantes;
- alertas de pressão hospitalar;
- evolução da metodologia do IPH;
- validação dos pesos utilizados no índice.

---

# 🎓 Contexto acadêmico

O CareVision foi desenvolvido como um **MVP para a Sprint 2 do Enterprise Challenge**.

A solução busca demonstrar a construção de um produto de dados completo, contemplando:

```text
Problema
   ↓
Coleta
   ↓
Tratamento
   ↓
Integração
   ↓
Análise
   ↓
Indicadores
   ↓
Visualização
   ↓
Deploy
   ↓
MVP funcional
```

O projeto apresenta evidências da construção da solução através do código-fonte, bases utilizadas, pipeline de processamento, metodologia analítica, dashboard e aplicação publicada.

---

# 📌 Observação metodológica

O **CareVision é um protótipo acadêmico de apoio analítico**.

O Índice de Pressão Hospitalar e suas classificações foram desenvolvidos especificamente para o MVP e devem ser interpretados considerando as limitações das bases públicas e da metodologia utilizada.

Os resultados apresentados não devem ser utilizados isoladamente para decisões clínicas ou operacionais.

---

# 🏥 CareVision

**Dados públicos transformados em informação para apoiar a análise da pressão hospitalar.**

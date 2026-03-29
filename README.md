# 📊 Painel Interativo COVID-19 - Espírito Santo (BI)

🌍 **Confira o resultado do deploy do projeto clicando no link:** [https://painel-covid-es.streamlit.app/](https://painel-covid-es.streamlit.app/)

Este projeto foi desenvolvido para a disciplina de **Business Intelligence (BI)**. O objetivo é aplicar técnicas de análise exploratória de dados (EDA) e visualização interativa utilizando os microdados reais de COVID-19 do estado do Espírito Santo, transformando dados brutos em informações para tomada de decisão.

O pipeline do projeto está dividido em três frentes principais:
1. **ETL (Extração, Transformação e Carga):** Processamento automatizado via script Python de uma base de microdados gigantesca (~1.9GB). O script filtra exclusivamente notificações do Espírito Santo e realiza agregações sem perda de valor analítico, resultando em uma base rápida (alguns KBs) perfeitamente otimizada para o Dashboard e para o GitHub.
2. **Análise de Dados (Jupyter Notebook):** Ambiente acadêmico focado em limpeza, tratamento preliminar, cruzamento de variáveis e modelagens analíticas das métricas de COVID.
3. **Dashboard Interativo (Streamlit):** Uma interface profissional e de alta performance que permite aos usuários explorar os dados visualmente e aplicar filtros em tempo real por município ou classificação.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

* **Linguagem:** Python
* **Análise e Manipulação de Dados:** Pandas
* **Visualização:** Plotly Express, Matplotlib
* **Ambiente Exploratório:** Jupyter Notebook
* **Interface/Dashboard:** Streamlit
* **Gerenciamento de Dependências:** `requirements.txt`

---

## 📂 Estrutura do Projeto

```text
├── data/
│   ├── MICRODADOS.csv          # Arquivo de dados brutos (não versionado no GitHub por ser muito pesado)
│   ├── dados_agregados.csv     # Base sumarizada, gerada via ETL e consumida pelo Dashboard
│   └── metadados.json          # Informações estruturais da base original (tipos, nulos, qtd. linhas)
├── notebooks/
│   └── PainelCovidBI.ipynb     # Notebook com a análise exploratória e preparação inicial
├── scripts/
│   └── gerar_agregados.py      # Script de ETL: Transforma a base gigante em base otimizada do ES
├── .gitignore                  # Arquivos e pastas ignorados pelo Git (ex: cache, datasets massivos)
├── brasao_es.jpg               # Imagem estática do brasão utilizada no painel
├── painel_covid19.py           # Código-fonte principal do Dashboard em Streamlit
├── requirements.txt            # Lista das bibliotecas e dependências do projeto
└── README.md                   # Documentação abrangente do projeto
```

---

## 🚀 Como Rodar o Projeto Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/J-Emanoel/painel-covid-es.git
cd painel-covid-es
```

### 2. Instalar as dependências
É recomendável a utilização de um ambiente virtual (venv). Execute:
```bash
pip install -r requirements.txt
```

### 3. Iniciar o Dashboard de BI interativo
Como a base agregada (`dados_agregados.csv`) já fica versionada e otimizada no repositório, você pode subir o painel imediatamente sem precisar ter um arquivo de 1.9GB:
```bash
streamlit run painel_covid19.py
```
*O painel abrirá automaticamente no seu navegador.*

### 4. (Opcional) Como rodar o Script de ETL
Caso você deseje atualizar a base com os dados mais recentes do Governo do Estado do Espírito Santo:
1. Baixe o `MICRODADOS.csv` de 1.9GB e jogue-o na pasta `data/`.
2. Em seu terminal, execute o agregador criado:
```bash
python scripts/gerar_agregados.py
```
Isso recalculará os totais originais e montará novamente a base sumarizada de alta velocidade contendo apenas as cidades válidas do Espírito Santo.

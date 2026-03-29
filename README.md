# 📊 Painel Interativo COVID-19 - Espírito Santo (BI)

Este projeto foi desenvolvido para a disciplina de **Business Intelligence (BI)**. O objetivo é aplicar técnicas de análise exploratória de dados (EDA) e visualização interativa utilizando os microdados reais de COVID-19 do estado do Espírito Santo, transformando dados brutos em informações para tomada de decisão.

O pipeline do projeto está dividido em duas frentes principais:
1. **Análise de Dados (Jupyter Notebook):** Limpeza, tratamento, cruzamento de variáveis e extração de insights (como a evolução de casos, taxas de letalidade por município e análise de dados faltantes).
2. **Dashboard Interativo (Streamlit):** Uma interface dinâmica que permite aos usuários explorar os dados visualmente e aplicar filtros por município para análises direcionadas.

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

* **Linguagem:** Python
* **Análise e Manipulação de Dados:** Pandas
* **Visualização:** Plotly Express, Matplotlib
* **Ambiente de Desenvolvimento:** Jupyter Notebook
* **Criação do Dashboard:** Streamlit

---

## 📂 Estrutura do Projeto

```text
├── data/
│   └── MICRODADOS.csv          # Arquivo de dados brutos (não versionado no GitHub por ser muito pesado)
├── .gitignore                  # Arquivos e pastas ignorados pelo Git (ex: dados, ambientes virtuais)
├── PainelCovidBI.ipynb         # Notebook com a análise exploratória detalhada
├── brasao_es.jpg               # Imagem utilizada na barra lateral do painel
├── painel_covid19.py           # Código-fonte do dashboard em Streamlit
├── requirements.txt            # Lista de bibliotecas e dependências do projeto
└── README.md                   # Documentação principal do projeto
````

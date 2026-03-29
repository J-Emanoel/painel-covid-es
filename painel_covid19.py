import streamlit as st
import pandas as pd
import plotly.express as px
import json

# Configuração da página
st.set_page_config(page_title="Painel COVID-19 ES", layout="wide")

# Exibindo o brasão do ES na barra lateral
st.sidebar.image("brasao_es.jpg", use_container_width=True)

st.title("Painel Interativo COVID-19 - Espírito Santo")
st.markdown("Dashboard dinâmico temático baseado na análise exploratória dos microdados de COVID-19 do estado do Espírito Santo.")

# Carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv('data/dados_agregados.csv')
    with open('data/metadados.json', 'r', encoding='utf-8') as f:
        meta = json.load(f)
    return df, meta

with st.spinner("Carregando os dados... (Isso pode demorar um pouco)"):
    df, meta = load_data()

st.sidebar.header("Filtros")

# Filtro de Município
municipios = ["Todos"] + list(df['Municipio'].dropna().unique())
municipio_selecionado = st.sidebar.selectbox("Selecione um Município", municipios)

# Aplicar filtros
df_filtrado = df.copy()
if municipio_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Municipio'] == municipio_selecionado]

# Filtro de Classificação
classificacoes = ["Todas"] + list(df_filtrado['Classificacao'].dropna().unique())
classificacao_selecionada = st.sidebar.selectbox("Classificação", classificacoes)

if classificacao_selecionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado['Classificacao'] == classificacao_selecionada]


# 1. Visão Geral
st.header("1. Visão Geral do Dataset Original")

if municipio_selecionado == "Todos":
    st.info("📍 Exibindo metadados da **Base Completa (Todos os Municípios)**")
else:
    st.info(f"📍 Filtro ativo para o Município: **{municipio_selecionado}** (Nota: Metadados abaixo referem-se à base completa original)")

col1, col2 = st.columns(2)
with col1:
    st.metric("Total de Notificações (Filtrado)", f"{df_filtrado['Quantidade'].sum():,}")
with col2:
    st.metric("Total de Colunas Originais", meta['total_colunas'])

with st.expander("Ver Tipos de Dados e Nulos (Base Original Completa)"):
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Tipos de Dados:**")
        df_dtypes = pd.DataFrame(list(meta['dtypes'].items()), columns=['Coluna', 'Tipo'])
        st.dataframe(df_dtypes)
    with col_b:
        st.write("**Valores Nulos por Coluna:**")
        if meta['nulos']:
            df_nulos = pd.DataFrame(list(meta['nulos'].items()), columns=['Coluna', 'Quantidade Nulos'])
            df_nulos['Percentual (%)'] = (df_nulos['Quantidade Nulos'] / meta['total_linhas']) * 100
            df_nulos = df_nulos.sort_values(by='Quantidade Nulos', ascending=False)
            st.dataframe(df_nulos)
        else:
            st.write("Sem valores nulos.")

st.divider()

col3, col4 = st.columns(2)

# 2. Distribuição por Classificação
with col3:
    st.header("2. Distribuição por Classificação")
    freq_abs = df_filtrado.groupby('Classificacao')['Quantidade'].sum().reset_index()
    fig_class = px.bar(freq_abs, y='Classificacao', x='Quantidade', orientation='h', title='Notificações por Classificação', color_discrete_sequence=['#4CA1E0'])
    fig_class.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_class, use_container_width=True)

# 3. Distribuição por Sexo
with col4:
    st.header("3. Distribuição por Sexo")
    freq_sexo = df_filtrado.groupby('Sexo')['Quantidade'].sum().reset_index()
    fig_sexo = px.pie(freq_sexo, names='Sexo', values='Quantidade', title='Distribuição por Sexo', hole=0.4, color='Sexo', color_discrete_map={'F': '#F7A8B8', 'M': '#4CA1E0', 'I': '#D3D3D3', 'Não Informado': '#888888'})
    st.plotly_chart(fig_sexo, use_container_width=True)

st.divider()

col5, col6 = st.columns(2)

# 4. Top 10 Municípios
with col5:
    st.header("4. Top 10 Municípios com Mais Notificações")
    if municipio_selecionado == "Todos":
        top_10_mun = df_filtrado.groupby('Municipio')['Quantidade'].sum().nlargest(10).reset_index()
        fig_mun = px.bar(top_10_mun, y='Municipio', x='Quantidade', orientation='h', title='Top 10 Municípios', color_discrete_sequence=['#F7A8B8'])
        fig_mun.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_mun, use_container_width=True)
    else:
        st.info("Filtro de município ativo. Para ver o Top 10 geral, selecione 'Todos'.")

# 5. Dados Faltantes em Datas Importantes
with col6:
    st.header("5. Análise de Dados Faltantes")
    st.markdown("Comparativo de valores ausentes por Status de Notificação")
    
    if 'StatusNotificacao' in df_filtrado.columns and 'DataEncerramento_Nula' in df_filtrado.columns and 'DataObito_Nula' in df_filtrado.columns:
        nulos_status = df_filtrado.groupby('StatusNotificacao')[['DataEncerramento_Nula', 'DataObito_Nula']].sum().reset_index()
        nulos_status = nulos_status.rename(columns={'DataEncerramento_Nula': 'DataEncerramento Nula', 'DataObito_Nula': 'DataObito Nula'})
        
        df_nulos_melted = nulos_status.melt(id_vars='StatusNotificacao', var_name='Tipo de Dado Faltante', value_name='Quantidade')
        
        fig_nulos = px.bar(df_nulos_melted, x='StatusNotificacao', y='Quantidade', color='Tipo de Dado Faltante', barmode='group', title='Valores Nulos em Datas por Status', color_discrete_sequence=['#4CA1E0', '#F7A8B8'])
        st.plotly_chart(fig_nulos, use_container_width=True)
    else:
        st.warning("Colunas necessárias para esta análise não estão disponíveis no dataset filtrado.")

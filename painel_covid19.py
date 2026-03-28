import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Painel COVID-19 ES", layout="wide")

# Exibindo o brasão do ES na barra lateral
st.sidebar.image("brasao_es.jpg", use_container_width=True)

st.title("Painel Interativo COVID-19 - Espírito Santo")
st.markdown("Dashboard dinâmico temático baseado na análise exploratória dos microdados de COVID-19 do estado do Espírito Santo.")

# Carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv('data/MICRODADOS.csv', sep=';', encoding='latin-1', low_memory=False)
    # Tentar converter a coluna de data principal se existir para uso em filtros
    if 'DataNotificacao' in df.columns:
        df['DataNotificacao'] = pd.to_datetime(df['DataNotificacao'], errors='coerce')
    return df

with st.spinner("Carregando os dados... (Isso pode demorar um pouco)"):
    df = load_data()

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
st.header("1. Visão Geral do Dataset")

if municipio_selecionado == "Todos":
    st.info("📍 Exibindo dados de **Todos os Municípios**")
else:
    st.info(f"📍 Exibindo dados exclusivamente para o Município: **{municipio_selecionado}**")

col1, col2 = st.columns(2)
with col1:
    st.metric("Total de Notificações", f"{df_filtrado.shape[0]:,}")
with col2:
    st.metric("Total de Colunas", df_filtrado.shape[1])

with st.expander("Ver Tipos de Dados e Nulos"):
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Tipos de Dados:**")
        st.dataframe(df_filtrado.dtypes.astype(str).reset_index().rename(columns={'index': 'Coluna', 0: 'Tipo'}))
    with col_b:
        st.write("**Valores Nulos por Coluna:**")
        nulos = df_filtrado.isnull().sum()
        nulos = nulos[nulos > 0]
        if not nulos.empty:
            perc_nulos = (nulos / df_filtrado.shape[0]) * 100
            nulos_df = pd.DataFrame({'Quantidade Nulos': nulos, 'Percentual (%)': perc_nulos}).sort_values(by='Quantidade Nulos', ascending=False)
            st.dataframe(nulos_df)
        else:
            st.write("Sem valores nulos.")

st.divider()

col3, col4 = st.columns(2)

# 2. Distribuição por Classificação
with col3:
    st.header("2. Distribuição por Classificação")
    freq_abs = df_filtrado['Classificacao'].value_counts().reset_index()
    freq_abs.columns = ['Classificacao', 'Quantidade']
    fig_class = px.bar(freq_abs, y='Classificacao', x='Quantidade', orientation='h', title='Notificações por Classificação', color_discrete_sequence=['#4CA1E0'])
    fig_class.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_class, use_container_width=True)

# 3. Distribuição por Sexo
with col4:
    st.header("3. Distribuição por Sexo")
    freq_sexo = df_filtrado['Sexo'].value_counts().reset_index()
    freq_sexo.columns = ['Sexo', 'Quantidade']
    fig_sexo = px.pie(freq_sexo, names='Sexo', values='Quantidade', title='Distribuição por Sexo', hole=0.4, color='Sexo', color_discrete_map={'F': '#F7A8B8', 'M': '#4CA1E0', 'I': '#D3D3D3'})
    st.plotly_chart(fig_sexo, use_container_width=True)

st.divider()

col5, col6 = st.columns(2)

# 4. Top 10 Municípios
with col5:
    st.header("4. Top 10 Municípios com Mais Notificações")
    if municipio_selecionado == "Todos":
        top_10_mun = df_filtrado['Municipio'].value_counts().head(10).reset_index()
        top_10_mun.columns = ['Municipio', 'Quantidade']
        fig_mun = px.bar(top_10_mun, y='Municipio', x='Quantidade', orientation='h', title='Top 10 Municípios', color_discrete_sequence=['#F7A8B8'])
        fig_mun.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_mun, use_container_width=True)
    else:
        st.info("Filtro de município ativo. Para ver o Top 10 geral, selecione 'Todos'.")

# 5. Dados Faltantes em Datas Importantes
with col6:
    st.header("5. Análise de Dados Faltantes")
    st.markdown("Comparativo de valores ausentes por Status de Notificação")
    
    if 'StatusNotificacao' in df_filtrado.columns and 'DataEncerramento' in df_filtrado.columns and 'DataObito' in df_filtrado.columns:
        nulos_enc = df_filtrado.groupby('StatusNotificacao')['DataEncerramento'].apply(lambda x: x.isnull().sum()).rename('DataEncerramento Nula')
        nulos_obi = df_filtrado.groupby('StatusNotificacao')['DataObito'].apply(lambda x: x.isnull().sum()).rename('DataObito Nula')
        
        df_nulos_status = pd.concat([nulos_enc, nulos_obi], axis=1).reset_index()
        df_nulos_melted = df_nulos_status.melt(id_vars='StatusNotificacao', var_name='Tipo de Dado Faltante', value_name='Quantidade')
        
        fig_nulos = px.bar(df_nulos_melted, x='StatusNotificacao', y='Quantidade', color='Tipo de Dado Faltante', barmode='group', title='Valores Nulos em Datas por Status', color_discrete_sequence=['#4CA1E0', '#F7A8B8'])
        st.plotly_chart(fig_nulos, use_container_width=True)
    else:
        st.warning("Colunas necessárias para esta análise não estão disponíveis no dataset filtrado.")

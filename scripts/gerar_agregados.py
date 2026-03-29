import pandas as pd
import json

print("Carregando 1.9GB CSV...")
df = pd.read_csv('data/MICRODADOS.csv', sep=';', encoding='latin-1', low_memory=False)

print("Filtrando apenas os 78 municípios do Espírito Santo...")
municipios_es = [
    'AFONSO CLAUDIO', 'AGUA DOCE DO NORTE', 'AGUIA BRANCA', 'ALEGRE', 'ALFREDO CHAVES',
    'ALTO RIO NOVO', 'ANCHIETA', 'APIACA', 'ARACRUZ', 'ATILIO VIVACQUA', 'BAIXO GUANDU',
    'BARRA DE SAO FRANCISCO', 'BOA ESPERANCA', 'BOM JESUS DO NORTE', 'BREJETUBA',
    'CACHOEIRO DE ITAPEMIRIM', 'CARIACICA', 'CASTELO', 'COLATINA', 'CONCEICAO DA BARRA',
    'CONCEICAO DO CASTELO', 'DIVINO DE SAO LOURENCO', 'DOMINGOS MARTINS', 'DORES DO RIO PRETO',
    'ECOPORANGA', 'FUNDAO', 'GOVERNADOR LINDENBERG', 'GUACUI', 'GUARAPARI', 'IBATIBA',
    'IBIRACU', 'IBITIRAMA', 'ICONHA', 'IRUPI', 'ITAGUACU', 'ITAPEMIRIM', 'ITARANA', 'IUNA',
    'JAGUARE', 'JERONIMO MONTEIRO', 'JOAO NEIVA', 'LARANJA DA TERRA', 'LINHARES',
    'MANTENOPOLIS', 'MARATAIZES', 'MARECHAL FLORIANO', 'MARILANDIA', 'MIMOSO DO SUL',
    'MONTANHA', 'MUCURICI', 'MUNIZ FREIRE', 'MUQUI', 'NOVA VENECIA', 'PANCAS',
    'PEDRO CANARIO', 'PINHEIROS', 'PIUMA', 'PONTO BELO', 'PRESIDENTE KENNEDY',
    'RIO BANANAL', 'RIO NOVO DO SUL', 'SANTA LEOPOLDINA', 'SANTA MARIA DE JETIBA',
    'SANTA TERESA', 'SAO DOMINGOS DO NORTE', 'SAO GABRIEL DA PALHA', 'SAO JOSE DO CALCADO',
    'SAO MATEUS', 'SAO ROQUE DO CANAA', 'SERRA', 'SOORETAMA', 'VARGEM ALTA',
    'VENDA NOVA DO IMIGRANTE', 'VIANA', 'VILA PAVAO', 'VILA VALERIO', 'VILA VELHA', 'VITORIA'
]
df = df[df['Municipio'].isin(municipios_es)]

print("Gerando metadados...")
# Para a visão geral do dataset
metadados = {
    'total_linhas': int(df.shape[0]),
    'total_colunas': int(df.shape[1]),
    'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()},
    'nulos': {col: int(null_count) for col, null_count in df.isnull().sum().items() if null_count > 0}
}
with open('data/metadados.json', 'w', encoding='utf-8') as f:
    json.dump(metadados, f, ensure_ascii=False, indent=2)

print("Processando flags de nulos...")
if 'DataEncerramento' in df.columns:
    df['DataEncerramento_Nula'] = df['DataEncerramento'].isnull().astype(int)
else:
    df['DataEncerramento_Nula'] = 0

if 'DataObito' in df.columns:
    df['DataObito_Nula'] = df['DataObito'].isnull().astype(int)
else:
    df['DataObito_Nula'] = 0

df['Quantidade'] = 1

colunas_groupby = ['Municipio', 'Classificacao', 'Sexo', 'StatusNotificacao']

print("Preenchendo NA nas colunas de agrupamento...")
for col in colunas_groupby:
    if col in df.columns:
        df[col] = df[col].fillna("Não Informado")

agg_funcs = {
    'Quantidade': 'sum',
    'DataEncerramento_Nula': 'sum',
    'DataObito_Nula': 'sum'
}

print("Agregando base...")
df_agg = df.groupby(colunas_groupby, as_index=False).agg(agg_funcs)

print(f"Salvando dados agregados (total de linhas: {df_agg.shape[0]})...")
df_agg.to_csv('data/dados_agregados.csv', index=False)
print("Concluído!")

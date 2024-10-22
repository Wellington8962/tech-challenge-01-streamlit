# Bibliotecas usadas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import sys
import warnings
import requests
warnings.filterwarnings("ignore")

import matplotlib.ticker as ticker
import numpy as np
from io import StringIO
from datetime import date
from matplotlib.ticker import FuncFormatter

# Importando as funções encapsuladas
from funcoes_analise import carregar_dados, preparar_dados_exportacao, gerar_grafico_valor_exportado, gerar_grafico_quantidade_exportada, gerar_grafico_exportacao_pais, gerar_tabela_descritiva

# Título principal
titulo_principal = '''
<h1 style="color: #5e9ca0;"><span style="background-color: #ffffff; color: #993366;">Clube Wine S.A.</span></h1>
<h2><span style="background-color: #ffffff; color: #993366;">Departamento de Ci&ecirc;ncia de Dados</span></h2>
<h2><span style="background-color: #ffffff; color: #993366;">_________________________________</span></h2>
<p>&nbsp;</p>
<h1 style="color: #5e9ca0;"><span style="text-decoration: underline;">&Aacute;rea do Investidor</span> - An&aacute;lise da Viticultura do Rio Grande do Sul</h1>
<p>&nbsp;</p>
<pre style="color: #2e6c80;">Cientistas de Dados: Wellington, Andr&eacute;, Raphael, David, Lucas</pre>
'''
st.markdown(titulo_principal, unsafe_allow_html=True)

# Título da página
st.title('Aspectos Macroeconômicos das Exportações de Vinho no Brasil')
st.markdown("<br>", unsafe_allow_html=True)

# Objetivo da análise
objetivo = '''
Nesta análise, você vai ver a macroeconomia das exportações de vinho do Rio Grande do Sul. O intuito é identificar os principais países importadores do nosso produto, avaliar a influência da taxa de câmbio do dólar sobre as exportações e examinar as condições climáticas que justificam a posição dominante da nossa região, o Rio Grande do Sul, responsável por mais de 90% da produção de vinho no Brasil.
Por fim, responder: É ainda interessante investir em vinho no Brasil?
'''
st.write(objetivo)

st.subheader("Análise Econômica")

analise_economica = '''
O propósito desta análise é identificar os principais mercados que importam os vinhos do Brasil, destacando as nações que são consideradas nossos principais clientes.
'''
st.write(analise_economica)

# Carregando os dados utilizando a função encapsulada
caminhos = [
    "ExpVinho.csv", 
    "Consumo_Alcool_Paraguay_EUA.csv", 
    "Viticultura_brasileira.csv", 
    "import_vinhos_br.csv", 
    "TAXA_CAMBIO_HISTORICO.csv", 
    "analise_mediana_mensal.csv", 
    "analise_precipitacao_mensal.csv"
]
dados_vinho, df_consumo_alcool, df_br_estado_producao, dados_import_vinhos, dados_cambio, analise_mediana_mensal, analise_precipitacao_mensal = carregar_dados(caminhos)

# Preparando os dados de exportação
anos = list(range(2008, 2023))
total_vinho_pais, final_data_vinho = preparar_dados_exportacao(dados_vinho, anos)

# Ordenando os países pelo valor exportado
total_vinho_pais_sorted = total_vinho_pais.sort_values(by='ValorUSD', ascending=False)

# Exibindo a análise gráfica
st.subheader("Valores Acumulados para Exportação em Dólar e Volume (litros)")
valores_acumulados = '''
Com o objetivo de identificar os principais destinos das exportações dos produtos vitivinícolas brasileiros, elaborou-se um gráfico que representa o valor consolidado exportado em dólares para diferentes países durante o período de 2008 a 2022. Observa-se que Paraguai, Rússia, Estados Unidos e China destacam-se como os principais destinos, evidenciando a relevância dessas nações para o setor.
'''
st.write(valores_acumulados)

# Gerar o gráfico de valor exportado utilizando a função encapsulada
gerar_grafico_valor_exportado(total_vinho_pais_sorted)

# Continuar ajustando conforme as funções encapsuladas
# Ordenando os países pelo volume exportado
total_vinho_pais_sorted_by_volume = total_vinho_pais.sort_values(by='Quantidade', ascending=False)

st.subheader('Ranking de Países por Quantidade Exportada (litros) entre 2008-2022')

# Gerar o gráfico de quantidade exportada utilizando a função encapsulada
gerar_grafico_quantidade_exportada(total_vinho_pais_sorted_by_volume)

st.markdown("<br>", unsafe_allow_html=True)

# Lista dos cinco principais países por valor exportado
lista_paises = total_vinho_pais_sorted.head(5)['País'].tolist()
filtro_data_vinho = final_data_vinho[final_data_vinho['País'].isin(lista_paises)]

st.subheader('Exportação de Vinho Brasileiro para os 5 Principais Países (2008-2022)')

# Gerar gráfico de exportação por país utilizando a função encapsulada
gerar_grafico_exportacao_pais(filtro_data_vinho, 'ValorUSD', 'Valor de Exportação (USD)')
# Continuando a modularização para as próximas seções

# Exibindo a análise de volume exportado
st.subheader("Volume Total Exportado para Cada País (2008-2022)")
volume_total_exportado = '''
Da mesma forma, criou-se um gráfico que apresenta o volume total exportado para cada país, expresso em litros. Nota-se que Rússia, Paraguai, Estados Unidos e China mantêm-se no topo da lista. Dessa maneira, podemos categorizar esses países como os principais clientes, reforçando sua significativa importância no contexto das exportações de produtos vitivinícolas.
'''
st.write(volume_total_exportado)

# Gerando o gráfico de volume exportado utilizando a função encapsulada
gerar_grafico_quantidade_exportada(total_vinho_pais_sorted_by_volume)

# Exibindo a análise de exportação detalhada para os 5 principais países
st.subheader("Exportação Detalhada por País (2008-2022)")
montante_acumulado_anual = '''
Ao realizar uma análise mais detalhada dos dados relativos aos cinco principais países, com base no ranking de valor exportado em dólares, apresentamos o gráfico a seguir. Este gráfico ilustra o montante acumulado anual exportado em dólares para essas nações.
'''
st.write(montante_acumulado_anual)

# Selecionando os 5 principais países e filtrando os dados
lista_paises = total_vinho_pais_sorted.head(5)['País'].tolist()
filtro_data_vinho = final_data_vinho[final_data_vinho['País'].isin(lista_paises)]

# Gerando o gráfico de exportação por país para os 5 principais países
gerar_grafico_exportacao_pais(filtro_data_vinho, 'ValorUSD', 'Valor de Exportação (USD)')

# Análise dos principais países
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Análise dos Principais Países Exportadores")

# Paraguai
st.markdown("<div style='font-size: 23px; font-weight: bold;'>1. Paraguai</div>", unsafe_allow_html=True)
paraguai = '''
As exportações para o Paraguai têm aumentado consistentemente ao longo dos anos, com um pico notável em 2021.
Dado o crescimento sustentado nas exportações para o Paraguai, é recomendado fortalecer as relações comerciais e explorar oportunidades para diversificar a oferta de produtos.
'''
st.write(paraguai)

# Exportação Paraguai
filtro_data_paraguai = final_data_vinho[final_data_vinho['País'] == 'Paraguai']
gerar_grafico_exportacao_pais(filtro_data_paraguai, 'ValorUSD', 'Valor de Exportação (USD)')

# Estados Unidos
st.markdown("<div style='font-size: 23px; font-weight: bold;'>2. Estados Unidos</div>", unsafe_allow_html=True)
estados_unidos = '''
As exportações para os EUA têm mostrado uma oscilação, mas não uma tendência de crescimento neste mercado.
O mercado dos EUA tem potencial de crescimento. A recomendação é considerar campanhas de marketing e promoções para aumentar a visibilidade e aceitação do vinho brasileiro nos EUA.
'''
st.write(estados_unidos)

# Exportação EUA
filtro_data_eua = final_data_vinho[final_data_vinho['País'] == 'Estados Unidos']
gerar_grafico_exportacao_pais(filtro_data_eua, 'ValorUSD', 'Valor de Exportação (USD)')

# Rússia
st.markdown("<div style='font-size: 23px; font-weight: bold;'>3. Rússia</div>", unsafe_allow_html=True)
russia = '''
As exportações para a Rússia apresentam certa imprevisibilidade. Em 2013, aparentemente estávamos conquistando espaço no mercado, porém a partir de 2014 tivemos resultados ruins.
A partir de 2020 houve novas importações, porém ainda não muito promissoras.
'''
st.write(russia)

# Exportação Rússia
filtro_data_russia = final_data_vinho[final_data_vinho['País'] == 'Rússia']
gerar_grafico_exportacao_pais(filtro_data_russia, 'ValorUSD', 'Valor de Exportação (USD)')

# China
st.markdown("<div style='font-size: 23px; font-weight: bold;'>4. China</div>", unsafe_allow_html=True)
china = '''
Exportações para a China demonstração volatilidade e não apresenta tendência de crescimento. É um mercado que nunca passamos de US$ 642.177 (pico em 2012).
Este mercado tem potencial de crescimento. A recomendação é considerar campanhas de marketing e promoções para aumentar a visibilidade e aceitação do vinho brasileiro.
'''
st.write(china)

# Exportação China
filtro_data_china = final_data_vinho[final_data_vinho['País'] == 'China']
gerar_grafico_exportacao_pais(filtro_data_china, 'ValorUSD', 'Valor de Exportação (USD)')

# Reino Unido
st.markdown("<div style='font-size: 23px; font-weight: bold;'>5. Reino Unido</div>", unsafe_allow_html=True)
reino_unido = '''
A análise das exportações do Reino Unido revela uma ausência de tendência de crescimento. Até 2013, alcançamos um patamar superior a 250 mil, atingindo um pico em 2014 com 1,3 milhões. No entanto, nos anos subsequentes, as vendas não mantiveram esse ritmo de crescimento.
'''
st.write(reino_unido)

# Exportação Reino Unido
filtro_data_reino_unido = final_data_vinho[final_data_vinho['País'] == 'Reino Unido']
gerar_grafico_exportacao_pais(filtro_data_reino_unido, 'ValorUSD', 'Valor de Exportação (USD)')

st.subheader("Análise de correlação entre taxa de câmbio e valor exportado")

tendencia_anual = """
No 'Tendência Anual de Exportação de Vinho Brasileiro' vemos a tendência anual do valor exportado em dólar para os três principais importadores de produtos da viticultura brasileira: Estados Unidos, Paraguai e Rússia. Paraguai se destaca porque a partir de 2015 começa uma crescente de importação. Ano a ano há uma aumento, exceto em 2019 e 2020. Devido essa tendência crescente Paraguai é o nosso principal cliente.
"""
st.write(tendencia_anual)

# RENOMEANDO COLUNAS
primeira_coluna = dados_cambio.columns[0]
dados_cambio = dados_cambio.rename(columns={primeira_coluna: 'datas'})
segunda_coluna = dados_cambio.columns[1]
dados_cambio = dados_cambio.rename(columns={segunda_coluna: 'cambio'})
dados_cambio['datas'] = pd.to_datetime(dados_cambio['datas'], format='%d/%m/%Y')

# Converter a coluna 'cambio' para numérico, forçando valores inválidos a se tornarem NaN
dados_cambio['cambio'] = pd.to_numeric(dados_cambio['cambio'], errors='coerce')

# Remover valores NaN que possam ter surgido na conversão
dados_filtrados = dados_cambio.dropna(subset=['cambio'])

# Filtrando os dados para incluir apenas a partir de 2008
dados_filtrados = dados_filtrados[dados_filtrados['datas'].dt.year >= 2008]

# Extrair o ano da coluna 'datas'
dados_filtrados = dados_filtrados.copy()
dados_filtrados['ano'] = dados_filtrados['datas'].dt.year

# Calcular a média da coluna 'cambio' agrupando por ano
# Está escrito mediana_por_ano, mas é média
mediana_por_ano = dados_filtrados.groupby('ano')['cambio'].mean().reset_index()

# CRIANDO UM DATASET PARA TRAZER PAÍS, ANO, QUANTIDADE (L) E VALOR EXPORTADO (USD)
years = list(range(2008, 2023))

# Criando listas vazias
paises_vinho = []
anos_vinho = []
quantidades_vinho = []
valores_vinho = []

# Iterando pelos dados para preencher as listas
for index, row in dados_vinho.iterrows():
    for year in years:
        paises_vinho.append(row['País'])
        anos_vinho.append(year)
        quantidades_vinho.append(row[str(year)])
        valores_vinho.append(row[str(year) + '.1'])

# Criando o dataframe reformatado
final_data_vinho = pd.DataFrame({
    'País': paises_vinho,
    'Ano': anos_vinho,
    'Quantidade': quantidades_vinho,
    'ValorUSD': valores_vinho
})

top_paises_vinho = ['Paraguai', 'Rússia', 'Estados Unidos']
filtro_data_vinho = final_data_vinho[final_data_vinho['País'].isin(top_paises_vinho)]

# Plotando a tendência anual para os 3 principais países
fig, ax = plt.subplots(figsize=(5, 4))
sns.lineplot(data=filtro_data_vinho, x='Ano', y='ValorUSD', hue='País', marker="o", palette="viridis", linewidth=2.5, ax=ax)
ax.set_xlabel('Ano', fontsize=12)
ax.set_ylabel('Valor de Exportação (USD)', fontsize=12)
ax.tick_params(axis='x', labelrotation=45) 
ax.set_title('Tendência Anual de Exportação de Vinho Brasileiro', fontsize=12)
ax.legend(title='País', fontsize=12)
plt.tight_layout()

formatter = ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x).replace(',', '.'))
ax.yaxis.set_major_formatter(formatter)

ax.set_ylim(-2000000, 17000000)

# Adicionar linhas de grade
ax.grid(True, linestyle='--', alpha=0.7)

# Exibindo o gráfico
st.pyplot(fig)
st.markdown(
    "<div style='text-align: center; font-size: 13px;'>Fonte: Embrapa</div>",
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# Filtrar os dados para incluir apenas linhas onde a coluna 'País' é 
final_data_vinho_paraguai = final_data_vinho[final_data_vinho['País'] == 'Paraguai']
final_data_vinho_russia = final_data_vinho[final_data_vinho['País'] == 'Rússia']
final_data_vinho_eua = final_data_vinho[final_data_vinho['País'] == 'Estados Unidos']

# Renomear a coluna 'ano' em 'mediana_por_ano' para 'Ano' para coincidir com o nome da coluna em 'final_data_vinho_paraguai'
mediana_por_ano = mediana_por_ano.rename(columns={'ano': 'Ano'})

# Merge dos DataFrames com base na coluna 'Ano'
final_data_vinho_paraguai_dolar = pd.merge(final_data_vinho_paraguai, mediana_por_ano, on='Ano')
final_data_vinho_russia_dolar = pd.merge(final_data_vinho_russia, mediana_por_ano, on='Ano')
final_data_vinho_eua_dolar = pd.merge(final_data_vinho_eua, mediana_por_ano, on='Ano')

valor_medio_anual_dolar = "Fazendo uma correlação do valor médio anual do dólar com gŕafico 'Tendência Anual de Exportação de Vinho Brasileiro', para cada país, temos os seguintes valores."
st.write(valor_medio_anual_dolar)

correlacao_paraguai = final_data_vinho_paraguai_dolar['ValorUSD'].corr(final_data_vinho_paraguai_dolar['cambio'])
correlacao_russia = final_data_vinho_russia_dolar['ValorUSD'].corr(final_data_vinho_russia_dolar['cambio'])
correlacao_eua = final_data_vinho_eua_dolar['ValorUSD'].corr(final_data_vinho_eua_dolar['cambio'])

correlacao_paraguai = round(correlacao_paraguai, 4)
correlacao_russia = round(correlacao_russia, 4)
correlacao_eua = round(correlacao_eua, 4)
# print(f"CORR Paraguai: {correlacao_paraguai}")
# print(f"CORR Rússia: {correlacao_russia}")
# print(f"CORR EUA: {correlacao_eua}")

# Valores das correlações
dados_tabela = {
    'País': ['Paraguai', 'Rússia', 'EUA'],
    'Correlação': [0.8693, -0.3513, -0.2901]
}

df = pd.DataFrame(dados_tabela)

st.markdown(
    "<div style='text-align: center; font-size: 20px;'><b>Correlação Anual: Dólar vs Exportação de Vinho Brasileiro<b></div>",
    unsafe_allow_html=True
)

# Exibir a tabela no Streamlit
st.table(df)
st.markdown(
    "<div style='text-align: center; font-size: 13px;'>Fontes análise de câmbio: Embrapa | GPEstatistica | Consultoria ICA | Vitivinicultura Brasileira: Panorama 2021</div>",
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

GPEstatistica = """
De acordo com o GPEstatística, uma correlação é considerada forte quando o coeficiente (r) é superior a 0,6 e igual ou inferior a 0,9. Ao analisarmos os dados, observamos que o valor do dólar não exerce uma influência significativa sobre as exportações para a Rússia e os Estados Unidos, pois sua correlação é bastante reduzida.

Entretanto, ao examinarmos as relações com o Paraguai, identificamos uma correlação de 0,8693, indicando uma associação forte entre a taxa de câmbio e o valor exportado. Nesse contexto, a valorização do dólar está diretamente relacionada ao aumento das exportações em dólares para esse país. Torna-se evidente que o valor exportado é sensível às flutuações cambiais.

Essa informação revela-se valiosa para compreender quais fatores impactam nossos lucros, fornecendo insights cruciais para a gestão estratégica dos negócios.
"""
st.write(GPEstatistica)

st.markdown("<br>", unsafe_allow_html=True)

# Bibliotecas utilizadas
from matplotlib.dates import DateFormatter, MonthLocator, YearLocator
warnings.filterwarnings("ignore")

# Título
st.title('O Rio Grande do Sul Destaca-se como o Principal Cultivador de Videiras no Brasil')

st.markdown("<br>", unsafe_allow_html=True)

RS = """
O Rio Grande do Sul é o maior produtor nacional de uva, contribuindo significativamente com aproximadamente 90% da produção nacional de uvas destinadas ao processamento. A Serra Gaúcha emerge como a principal zona produtora, responsável por cerca de 85% da produção de uvas no estado. Além disso, as regiões da Campanha Gaúcha, Serra do Sudeste, Campos de Cima da Serra e Vale Central também desempenham papéis proeminentes na atividade vitivinícola. Devido à magnitude da produção no Rio Grande do Sul, os dados desse estado são considerados como a principal base de referência para representação e análise do setor vitivinícola em âmbito nacional.

A produção de uva é destinada não apenas ao consumo de mesa, mas também à elaboração de sucos e vinhos, tanto de forma artesanal quanto industrial. Abaixo, segue uma imagem representando as Indicações Geográficas (IG) no território nacional.
"""
st.write(RS)

st.subheader("Indicações Geográficas (IG) de Vinhos do Brasil e Associações de Produtores")

# Adicionando a imagem
st.image("indicacoes_geograficas.jpg", caption="Fonte: https://www.embrapa.br/uva-e-vinho/indicacoes-geograficas-de-vinhos-do-brasil", use_column_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# Influência da temperatura na videira
temperatura_videira = """
A atividade fotossintética da videira é fortemente influenciada pela temperatura do ar. O comportamento da cultura da videira é significativamente afetado pela temperatura, sendo este o fator ambiental mais significante. A temperatura do ar influencia a atividade fotossintética das plantas, sendo que as reações da fotossíntese são menos intensas em temperaturas abaixo de 20°C, atingindo o máximo entre 25 e 30°C, e diminuindo novamente quando a temperatura se aproxima de 45°C.

A faixa de temperatura média considerada ideal para a produção de uvas de mesa situa-se entre 20°C e 30°C. Nesse intervalo, as condições são propícias para o desenvolvimento da videira e para a produção de uvas de mesa, passas e vinhos doces.

A temperatura da região de cultivo também afeta a composição química da uva. Em regiões com temperaturas mais elevadas, dentro dos limites críticos, há maior concentração de açúcar e menor concentração de ácido málico nos frutos. Isso favorece a produção de uva de mesa, passas e vinhos doces. Em regiões mais frias, as condições são mais propícias para a produção de vinhos secos, devido ao maior teor de ácido nos frutos.

O zoneamento agroclimático é uma ferramenta utilizada para delimitar regiões propícias ao cultivo da videira. Esse zoneamento considera variáveis como temperatura, umidade, precipitação e evapotranspiração. Em algumas regiões, como o Submédio São Francisco, as condições climáticas são favoráveis ao crescimento da videira.
"""
st.write(temperatura_videira)

# Análise climática
st.subheader("Análise Climática nas Regiões Produtoras: Estudo Detalhado de Precipitação e Temperatura no Rio Grande do Sul")

analise_climatica = """
Exploramos os registros da base de dados do Instituto Nacional de Meteorologia -
INMET e adquirimos dados sobre chuva e temperatura de forma mensal, abrangendo o
período de 2007 a 2022. A produção de uvas no Rio Grande do Sul é predominante, representando 90% do total nacional. Optamos por avaliar as condições climáticas em cidades cruciais no cultivo de uvas, como Erechim, Alegrete, Rio Grande, Bento Gonçalves e Bagé.

Para conduzir a análise, adotamos os seguintes procedimentos: realizamos a limpeza
dos dados e organizamos a temperatura e a precipitação em gráficos para uma
inspeção visual em busca de padrões.

A seguir, apresentamos uma análise exploratória com estatística descritiva,
destacando as variáveis de temperatura (em graus Celsius) e precipitação (em
milímetros) nas cinco cidades consideradas. As tabelas contêm dados do número total
de observações, média, desvio padrão, valor mínimo, primeiro quartil (25%), mediana
(50%), terceiro quartil (75%) e valor máximo para cada variável, abrangendo todas as
regiões analisadas. Seguem as tabelas:
"""
st.write(analise_climatica)

# Lista de cidades
cidades = ['Bento Gonçalves', 'Alegrete', 'Bagé', 'Rio Grande', 'Erechim']

def gerar_tabela_descritiva(analise_mediana_mensal, analise_precipitacao_mensal):
    # Selecionando as cinco cidades
    df_temp_mediana = analise_mediana_mensal[analise_mediana_mensal['Cidade'].isin(cidades)]
    df_temp_precipitacao = analise_precipitacao_mensal[analise_precipitacao_mensal['Cidade'].isin(cidades)]

    # Convertendo as datas para o formato datetime
    df_temp_mediana['Data de Referência'] = pd.to_datetime(df_temp_mediana['Data de Referência'])
    df_temp_precipitacao['Data de Referência'] = pd.to_datetime(df_temp_precipitacao['Data de Referência'])

    # Calculando estatísticas descritivas para temperatura mediana
    desc_temp_mediana = df_temp_mediana.groupby('Cidade')['Temperatura Mediana (°C)'].describe().round(2)

    # Calculando estatísticas descritivas para precipitação
    desc_precipitacao = df_temp_precipitacao.groupby('Cidade')['Precipitação (mm)'].describe().round(2)

    return desc_temp_mediana, desc_precipitacao

# Chamando a função nas tabelas
tabela_temp_mediana, tabela_precipitacao = gerar_tabela_descritiva(analise_mediana_mensal, analise_precipitacao_mensal)

# Exibindo as tabelas centralizadas
st.subheader("Estatística Descritiva - Temperatura (C°):")
st.dataframe(tabela_temp_mediana.style.format("{:.2f}").set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}]).set_properties(**{'text-align': 'center'}))

st.subheader("Estatística Descritiva - Precipitação (mm):")
st.dataframe(tabela_precipitacao.style.format("{:.2f}").set_table_styles([{'selector': 'th', 'props': [('text-align', 'center')]}]).set_properties(**{'text-align': 'center'}))

st.markdown("<br>", unsafe_allow_html=True)

# Análise Exploratória: Estatísticas Descritivas de Temperatura e Precipitação
st.subheader("Análise Exploratória: Estatísticas Descritivas de Temperatura e Precipitação")

st.markdown("<br>", unsafe_allow_html=True)

tabela_temp_mediana = tabela_temp_mediana.reset_index()
tabela_precipitacao = tabela_precipitacao.reset_index()

# Criando a função para gerar as tabelas com o Matplotlib
def criar_tabela_matplotlib(titulo, dados):
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.axis('off')

    rotulos = ['Cidade', 'Número total de observações', 'Média', 'Desvio Padrão', 'Valor Mínimo', 'Primeiro Quartil (25%)', 'Mediana (50%)', 'Terceiro Quartil (75%)', 'Valor Máximo']

    # Criando a tabela diretamente a partir dos dados
    tabela_matplotlib = ax.table(cellText=dados.values,
                                 colLabels=rotulos,
                                 loc='center',
                                 cellLoc='center')
    tabela_matplotlib.auto_set_font_size(False)
    tabela_matplotlib.set_fontsize(12)  
    tabela_matplotlib.auto_set_column_width([0] + list(range(1, len(rotulos)))) 
    tabela_matplotlib.scale(1.7, 2.7) 

    titulo_table = ax.text(0.5, 1.6, titulo, va='center', ha='center', fontsize=15)

    # Exibindo a tabela
    st.pyplot(fig)

# Exibindo as tabelas no Streamlit
criar_tabela_matplotlib("Estatística Descritiva - Temperatura (C°)", tabela_temp_mediana)
criar_tabela_matplotlib("Estatística Descritiva - Precipitação (mm)", tabela_precipitacao)

st.markdown("<br>", unsafe_allow_html=True)

analise_cinco_cidades = """
Finalizamos com uma análise exploratória abrangente que conectou as cinco
cidades, explorando as relações entre temperatura mediana durante o período
de 2007 a 2023. A seguir, apresentamos o gráfico correspondente:
"""
st.write(analise_cinco_cidades)

st.markdown("<br>", unsafe_allow_html=True)

# Criando o gráfico
sns.set(style="whitegrid")
fig, ax = plt.subplots(figsize=(15, 7))

for cidade in cidades:
    cidade_data = analise_mediana_mensal[analise_mediana_mensal['Cidade'] == cidade]
    sns.lineplot(data=cidade_data, x='Data de Referência', y='Temperatura Mediana (°C)', label=cidade)

ax.set(xlabel='Data de Referência', ylabel='Temperatura (°C)')
locator = MonthLocator(bymonthday=1, interval=6)
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
ax.set_xticks(pd.date_range(start='2007-01-01', end='2023-01-01', freq='6MS'))
plt.xticks(rotation=65, ha='right')
ax.set_ylim(0, 30)
ax.legend(title='Cidade', bbox_to_anchor=(1.05, 0.5), loc='center left', ncol=1, borderaxespad=-3.5)

# Exibindo o gráfico
st.pyplot(fig)
st.markdown(
    "<div style='text-align: center; font-size: 12px;'>Gráfico 11: Variação da Temperatura Mediana Mensal das cinco cidades (2007-2023)</div>",
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

influencia_El_Nino = """
A variação das temperaturas, mesmo em anos mais quentes como 2022 e 2011, não teve um impacto negativo direto na produção de uvas, indicando uma resiliência do setor a condições climáticas extremas. Além disso, a influência do El Niño nas chuvas ao longo de 2007 a 2022 foi observada, destacando sua capacidade de afetar o ciclo de crescimento das vinhas. A correlação entre a ocorrência do El Niño e reduções na produção de vinhos, especialmente tintos, sugere a importância de os agricultores monitorarem atentamente as safras em anos como 2024, quando há previsão desse fenômeno climático.
"""
st.write(influencia_El_Nino)

st.markdown("<br>", unsafe_allow_html=True)

conclusao_impactos_climaticos = """Conclusão"""
st.subheader(conclusao_impactos_climaticos)

conclusao = """
Investir no setor vitivinícola brasileiro, especialmente no estado do Rio Grande do Sul, apresenta-se como uma oportunidade estratégica e promissora para os investidores. Destacamos as razões fundamentais que respaldam essa recomendação:

**1. Crescimento Sustentável:**
   - As exportações de vinho do Brasil têm registrado um crescimento sustentável, com destaque para mercados-chave como Paraguai, Rússia, Estados Unidos e China.
   - O Paraguai, em particular, emerge como um mercado em ascensão constante, oferecendo oportunidades de expansão e diversificação.

**2. Mercados Estratégicos:**
   - A diversificação dos destinos de exportação, com ênfase em países como Rússia e China, abre portas para mercados estratégicos e amplia o alcance internacional do setor.

**3. Estabilidade no Rio Grande do Sul:**
   - O Rio Grande do Sul, responsável por mais de 90% da produção nacional, destaca-se como o principal estado exportador de derivados de uva no Brasil.
   - Condições climáticas favoráveis, com temperaturas ideais entre 20°C e 30°C, contribuem para uma produção consistente e de alta qualidade.

**4. Análise de Riscos:**
   - A análise climática indica a resiliência do Rio Grande do Sul frente a fenômenos climáticos passados, como o El Niño, não comprometendo significativamente a produção.
   - Monitoramento constante e práticas agrícolas eficientes contribuem para mitigar riscos climáticos.

**5. Recomendações de Marketing:**
   - Recomenda-se estratégias de marketing e promoção para consolidar e expandir a presença em mercados como Estados Unidos e Rússia, aproveitando seu potencial de crescimento.

**Em síntese, investir no setor vitivinícola brasileiro, com ênfase no Rio Grande do Sul, oferece aos investidores a perspectiva de participar de um mercado em expansão, impulsionado por exportações consistentes e favoráveis condições de produção. A resiliência demonstrada diante de desafios climáticos passados e as estratégias de crescimento sustentável posicionam o setor como uma escolha confiável para investimentos sólidos e de longo prazo.**
"""
st.write(conclusao)

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("Referências")

referencias = """
***EMBRAPA. Dados da Vitivinicultura.***
Disponível em: https://www.cnpuv.embrapa.br/vitibrazil/index.php?opcao=opt_01 - Acesso em 02 de novembro de 2023.

***IPEA Data. Taxa de câmbio comercial para compra.***
Disponível em: http://www.ipeadata.gov.br/ExibeSerie.aspx?serid=38590&module=M - Acesso em 02 de novembro de 2023.

***GPEstatistica. Coeficiente de Correlação de Pearson.***
Disponível em: https://gpestatistica.netlify.app/blog/correlacao - Acesso em 06 de janeiro de 2024.

***Consultoria ICA. Estudo de Mercado de Vinhos, Espumantes e Sucos de Uva no Paraguai.***
Disponível em: https://www.gov.br/empresas-e-negocios/pt-br/invest-export-brasil/exportar/conheca-os-mercados/pesquisas-de-mercado/estudo-de-mercado.pdf/Paraguai2021.pdf - Acesso em 20 de janeiro de 2024.

***Vitivinicultura Brasileira: Panorama 2021.***
Disponível em: https://ainfo.cnptia.embrapa.br/digital/bitstream/doc/1149674/1/Com-Tec-226.pdf - Acesso em 20 de janeiro de 2024.

***População Maior de 20 anos do Paraguai.***
Disponível em: https://opendata.paho.org/en/core-indicators/core-indicators-dashboard - Acesso em 20 de janeiro de 2024.

***Consumo de Álcool no Paraguai.***
Disponível em: https://www.paho.org/en/enlace/alcohol-consumption - Acesso em 20 de janeiro de 2024.

***Exportação do Rio Grande do Sul.***
Disponível em: https://www.cnpuv.embrapa.br/vitibrazil/index.php?opcao=opt_01 - Acesso em 20 de janeiro de 2024.

***INMET - Instituto Nacional de Meteorologia.***
Disponível em:
https://portal.inmet.gov.br/dadoshistoricos - Acesso em 28/11/2023.

***BASF Brasil | Agricultura.***
Disponível em:
https://agriculture.basf.com/br/pt/conteudos/cultivos-e-sementes/uva/qual-e-a-temperatura-ideal-para-o-cultivo-de-videiras-tropicais.html - Acesso em 06/01/2024.

***Vinícula Aliança.***
Disponível em:
https://vinicolaalianca.com.br/blog/3/suco-de-uva-alianca/69/voce-sabe-quanto-tempo-a-videira-leva-para-dar-uvas-confira-aqui - Acesso em 06/01/2024.

***Veja.***
Disponível em:
https://veja.abril.com.br/ciencia/el-nino-deve-durar-pelo-menos-ate-abril-de-2024-diz-agencia-da-onu - Acesso em 07/01/2024.

***g1 | Meio Ambiente.***
Disponível em:
https://g1.globo.com/meio-ambiente/noticia/2023/11/08/el-nino-deve-durar-ao-menos-ate-abril-de-2024-aponta-organizacao-meteorologica-mundial.ghtml - Acesso em 07/01/2024.

***Embrapa.***
Disponível em:
https://www.embrapa.br/cim-uva-e-vinho/a-viticultura-no-brasil - Acesso em 08/01/2024.\n
http://www.cpatsa.embrapa.br:8080/sistema_producao/spuva/clima.html - Acesso em 08/01/2024.\n
https://www.embrapa.br/uva-e-vinho/indicacoes-geograficas-de-vinhos-do-brasil - Acesso em 08/01/2024.\n

***Visão analítica da viticultura sul-rio-grandense – Conab***. 
Compêndio de estudos Conab V.19, 2019 - Acesso em 09/01/2024.

***Atlas Socioeconômico Rio Grande do Sul.***
Disponível em:
https://atlassocioeconomico.rs.gov.br/uva-e-maca#:~:text=O%20cultivo%20de%20uva%20no,de%2052%25%20da%20produ%C3%A7%C3%A3o%20nacional. - Acesso em 09/01/2024.

***Revista Brasileira de Engenharia Agrícola e Ambiental.***
Disponível em:
https://www.scielo.br/j/rbeaa/a/mDNzxqwJj3qZ3VrzwsMLNwL/? - Acesso em 10/01/2024.
"""
st.write(referencias)
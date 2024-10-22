import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib import ticker
import numpy as np

# Função para carregar os dados com cache
@st.cache_data
def carregar_dados(caminhos):
    """
    Carrega múltiplos arquivos CSV em uma lista de DataFrames.

    Parâmetros:
        caminhos (list): Lista de strings com os caminhos dos arquivos CSV.

    Retorna:
        tuple: Tupla contendo os DataFrames carregados a partir dos arquivos CSV.
    """
    dados_vinho = pd.read_csv(caminhos[0], sep=";")
    df_consumo_alcool = pd.read_csv(caminhos[1], sep=";")
    df_br_estado_producao = pd.read_csv(caminhos[2], sep=";")
    dados_import_vinhos = pd.read_csv(caminhos[3], sep=";")
    dados_cambio = pd.read_csv(caminhos[4], encoding='ISO-8859-1', sep=';', skipfooter=12, engine="python")
    analise_mediana_mensal = pd.read_csv(caminhos[5], parse_dates=["Data de Referência"])
    analise_precipitacao_mensal = pd.read_csv(caminhos[6], parse_dates=["Data de Referência"])

    return (dados_vinho, df_consumo_alcool, df_br_estado_producao, dados_import_vinhos,
            dados_cambio, analise_mediana_mensal, analise_precipitacao_mensal)


# Função para preparar os dados de exportação de vinho
def preparar_dados_exportacao(dados_vinho, anos):
    """
    Prepara os dados de exportação de vinho organizando-os em um DataFrame e somando os valores por país.

    Parâmetros:
        dados_vinho (DataFrame): O DataFrame original com os dados de exportação de vinho.
        anos (list): Lista de anos a serem considerados.

    Retorna:
        tuple: Contém o DataFrame total por país e o DataFrame detalhado por país e ano.
    """
    paises_vinho, anos_vinho, quantidades_vinho, valores_vinho = [], [], [], []

    # Iterar sobre as linhas e anos para construir as listas
    for index, row in dados_vinho.iterrows():
        for year in anos:
            paises_vinho.append(row['País'])
            anos_vinho.append(year)
            quantidades_vinho.append(row[str(year)])
            valores_vinho.append(row[str(year) + '.1'])

    # Criando o DataFrame final com todos os dados reorganizados
    final_data_vinho = pd.DataFrame({
        'País': paises_vinho,
        'Ano': anos_vinho,
        'Quantidade': quantidades_vinho,
        'ValorUSD': valores_vinho
    })

    # Somando os valores totais de exportação por país
    total_vinho_pais = final_data_vinho.groupby('País').agg({'Quantidade': 'sum', 'ValorUSD': 'sum'}).reset_index()

    return total_vinho_pais, final_data_vinho


# Função para gerar o gráfico de valor exportado
def gerar_grafico_valor_exportado(total_vinho_pais_sorted):
    """
    Gera um gráfico de barras para mostrar o valor total exportado em USD por país.

    Parâmetros:
        total_vinho_pais_sorted (DataFrame): O DataFrame com os países e seus valores totais de exportação ordenados.
    """
    fig, ax = plt.subplots(figsize=(8, 10))
    sns.barplot(x='ValorUSD', y='País', data=total_vinho_pais_sorted.head(20), palette='viridis', ax=ax)
    ax.set(xlabel='Valor Total Exportado (USD)', ylabel='País')

    # Formatando os valores para melhor visualização
    formatter = ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x).replace(',', '.'))
    ax.xaxis.set_major_formatter(formatter)

    # Adicionando rótulos numéricos a cada barra
    for index, value in enumerate(total_vinho_pais_sorted.head(10)['ValorUSD']):
        ax.text(value, index, f'{value:,.0f}', ha='left', va='center', fontsize=10, color='black')

    ax.set_xlim(0, total_vinho_pais_sorted['ValorUSD'].max() * 1.1)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)


# Função para gerar o gráfico de quantidade exportada
def gerar_grafico_quantidade_exportada(total_vinho_pais_sorted_by_volume):
    """
    Gera um gráfico de barras para mostrar a quantidade total exportada em litros por país.

    Parâmetros:
        total_vinho_pais_sorted_by_volume (DataFrame): O DataFrame com os países e suas quantidades totais exportadas, ordenados.
    """
    fig, ax = plt.subplots(figsize=(8, 10))
    sns.barplot(x='Quantidade', y='País', data=total_vinho_pais_sorted_by_volume.head(20), palette='viridis', ax=ax)
    ax.set(xlabel='Total de Exportação (Litros)', ylabel='País')

    # Formatando os valores do eixo x
    formatter = ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x).replace(',', '.'))
    ax.xaxis.set_major_formatter(formatter)

    # Adicionando rótulos numéricos a cada barra
    for index, value in enumerate(total_vinho_pais_sorted_by_volume.head(20)['Quantidade']):
        ax.text(value, index, f'{value:,.0f}', ha='left', va='center', fontsize=10, color='black')

    ax.set_xlim(0, total_vinho_pais_sorted_by_volume['Quantidade'].max() * 1.1)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

# Função para gerar tabela descritiva
def gerar_tabela_descritiva(analise_mediana_mensal, analise_precipitacao_mensal):
    """
    Gera tabelas descritivas para os dados de temperatura mediana e precipitação.

    Parâmetros:
        analise_mediana_mensal (DataFrame): DataFrame contendo dados de temperatura.
        analise_precipitacao_mensal (DataFrame): DataFrame contendo dados de precipitação.

    Retorna:
        tuple: Contém as tabelas descritivas para temperatura e precipitação.
    """
    # Selecionar apenas as cidades desejadas
    cidades = ['Bento Gonçalves', 'Alegrete', 'Bagé', 'Rio Grande', 'Erechim']
    
    # Filtrar os dados de temperatura e precipitação com base nas cidades selecionadas
    df_temp_mediana = analise_mediana_mensal[analise_mediana_mensal['Cidade'].isin(cidades)]
    df_temp_precipitacao = analise_precipitacao_mensal[analise_precipitacao_mensal['Cidade'].isin(cidades)]

    # Calcular estatísticas descritivas para temperatura mediana
    desc_temp_mediana = df_temp_mediana.groupby('Cidade')['Temperatura Mediana (°C)'].describe().round(2)

    # Calcular estatísticas descritivas para precipitação
    desc_precipitacao = df_temp_precipitacao.groupby('Cidade')['Precipitação (mm)'].describe().round(2)

    return desc_temp_mediana, desc_precipitacao

# Função para gerar o gráfico de exportação por país e ano
def gerar_grafico_exportacao_pais(filtro_data_vinho, eixo_y, rotulo_y):
    """
    Gera um gráfico de linha mostrando a tendência de exportação por país ao longo dos anos.

    Parâmetros:
        filtro_data_vinho (DataFrame): O DataFrame filtrado contendo os dados de exportação por país.
        eixo_y (str): A coluna do DataFrame que será utilizada para o eixo y.
        rotulo_y (str): O rótulo do eixo y.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.lineplot(data=filtro_data_vinho, x='Ano', y=eixo_y, hue='País', marker="o", palette="magma", linewidth=1, ax=ax)
    ax.set(xlabel='Ano', ylabel=rotulo_y)

    # Formatando os valores do eixo y
    formatter = ticker.FuncFormatter(lambda x, pos: '{:,.0f}'.format(x).replace(',', '.'))
    ax.yaxis.set_major_formatter(formatter)

    # Ajustando o limite do eixo y com base nos dados
    ax.set_ylim(0, filtro_data_vinho[eixo_y].max() * 1.1)

    # Ajustando rótulos do eixo x
    anos = filtro_data_vinho['Ano'].unique()
    ax.set_xticks(anos)
    ax.set_xticklabels(anos, rotation=45, ha='right')

    plt.tight_layout()

    # Exibir o gráfico no Streamlit
    st.pyplot(fig)

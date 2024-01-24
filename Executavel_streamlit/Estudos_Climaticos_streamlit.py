# Bibliotecas utilizadas
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter, MonthLocator, YearLocator
import sys
import warnings
warnings.filterwarnings("ignore")

# Título
st.title('O Rio Grande do Sul Destaca-se como o Principal Cultivador de Videiras no Brasil')

st.markdown("<br>", unsafe_allow_html=True)

RS = """
O Rio Grande do Sul é o maior produtor nacional de uva, contribuindo significativamente com aproximadamente 90% da produção nacional de uvas destinadas ao processamento. A Serra Gaúcha emerge como a principal zona produtora, responsável por cerca de 85% da produção de uvas no estado. Além disso, as regiões da Campanha Gaúcha, Serra do Sudeste, Campos de Cima da Serra e Vale Central também desempenham papéis proeminentes na atividade vitivinícola. Devido à magnitude da produção no Rio Grande do Sul, os dados desse estado são considerados como a principal base de referência para representação e análise do setor vitivinícola em âmbito nacional.

A produção de uva é destinada não apenas ao consumo de mesa, mas também à elaboração de sucos e vinhos, tanto de forma artesanal quanto industrial. Abaixo, segue uma imagem representando as Indicações Geográficas (IG) no território nacional.
"""
st.write(RS)

st.markdown("<br>", unsafe_allow_html=True)

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

# Leitura dos dados
analise_mediana_mensal = pd.read_csv("analise_mediana_mensal.csv", parse_dates=["Data de Referência"])
analise_precipitacao_mensal = pd.read_csv("analise_precipitacao_mensal.csv", parse_dates=["Data de Referência"])

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
As elevadas temperaturas não tiveram um impacto adverso direto na
produção. Houve períodos em que as temperaturas estavam
consideravelmente acima da média, como evidenciado em 2022. No entanto,
apesar dessas condições, a produção foi robusta nesse ano, sugerindo que as
altas temperaturas não exercem uma influência determinante nas condições
das safras. Ao analisar as temperaturas de forma ordenada, da estação mais
quente para a mais fria, não foi possível identificar um padrão visual claro que
permitisse fazer afirmações conclusivas. Além de 2022, o ano de 2011 também
se destacou como um dos mais quentes, correlacionado a um aumento
significativo na produção. Em resumo, as oscilações de temperatura estiveram
presentes tanto nos picos quanto nos declínios na produção.

A influência do fenômeno El Niño nas chuvas pode ser significativa para a
produção e safra das uvas ao longo dos anos de 2007 a 2022. O El Niño,
caracterizado pelo aquecimento anômalo das águas do Oceano Pacífico, tem
potencial para alterar os padrões climáticos em diversas regiões do mundo,
inclusive afetando as condições meteorológicas em áreas vitivinícolas.

Durante os anos em que o El Niño esteve presente, é possível observar
variações nas chuvas que podem impactar diretamente a produção de uvas.
Eventos climáticos extremos, como chuvas intensas ou períodos de seca
prolongados associados ao El Niño, podem influenciar o ciclo de crescimento
das vinhas, afetando a qualidade e quantidade da safra.

Notamos que nos anos de ocorrência do fenômeno El Niño, há uma correlação
com reduções significativas, sejam sutis ou extremas, na produção de vinhos,
especialmente os tintos, tanto os de mesa quanto os finos, que são
comercializados em grande escala. A previsão de um El Niño para 2024 destaca a importância de os agricultores estarem atentos às suas safras neste
ano específico, considerando os potenciais impactos adversos nas condições
climáticas.
"""
st.write(influencia_El_Nino)

st.markdown("<br>", unsafe_allow_html=True)

conclusao_impactos_climaticos = """
Conclusão sobre os Impactos Climáticos
"""
st.subheader(conclusao_impactos_climaticos)

st.markdown("<br>", unsafe_allow_html=True)

conclusao = """
Podemos assegurar aos investidores que, até o momento, não observamos
efeitos climáticos negativos nem comprometimento da fertilidade do solo em
nossa produção anual. Nossas análises indicam consistência na produção de
uvas, mesmo em anos de El Niño, sem impactos significativos.

O Rio Grande do Sul, principal cultivador de videiras no Brasil, mantém-se
eficiente diante das condições climáticas. A Serra Gaúcha e outras regiões
desempenham papéis proeminentes na produção de uvas.

A temperatura média ideal para a produção de uvas tem sido mantida entre
20°C e 30°C. Análises climáticas nas cidades-chave não evidenciaram impactos
negativos significativos.

Portanto, afirmamos que, até o momento, não há indícios de que a
temperatura ou as condições climáticas estejam comprometendo a fertilidade
do solo ou causando efeitos adversos na produção. Continuamos a monitorar
atentamente as condições climáticas, e a previsão de El Niño para 2024 nos
alerta para permanecermos vigilantes. As boas práticas agrícolas são
essenciais para garantir a continuidade de uma produção saudável e
consistente.
"""
st.write(conclusao)

st.markdown("<br>", unsafe_allow_html=True)

ref = """
Referências
"""
st.subheader(ref)

st.markdown("<br>", unsafe_allow_html=True)

referencias = """
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


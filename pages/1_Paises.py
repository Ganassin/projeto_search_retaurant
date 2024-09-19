# Importa o STREAMLIT, que é uma biblioteca. Antes de importar tive que instalar com o pip install no terminal
import streamlit as st
# Importando biblioteca para mostrar imagem
from PIL import Image
# biblioteca para carregar e tratasr o dataframe
import pandas as pd
# Importar biblioteca para criação de gráficos: plotly
import plotly.express as px


# Cria um dataframe com os dados já limpos no arquivo limpa_dataset.ipynb
df = pd.read_csv('datasets/zomato_limpo.csv')

# ============================================================================================================================
# LAYOUT DO STREAMLIT
# ============================================================================================================================

# Configura as informações da página, é a barrinha que aparece na parte de cima do navegador 
st.set_page_config(
    page_title='Países', 
    page_icon='🌍', 
    layout='wide')

# =========================================================================================
# SIDEBAR =================================================================================
# =========================================================================================

# Logo, deve estar na mesma pasta que o arquivo .py
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120 )

# ------------------------------------------------------------------------
st.sidebar.markdown('# Search For Restaurants.') # Título da sidebar
st.sidebar.markdown(""" --- """) # Divider
st.sidebar.markdown('## Filtros') # Subtítulo da sidebar

# Cria um filtro de seleção de países
countrys = df['country_name'].sort_values().unique()
country = st.sidebar.multiselect(
    'País:',
    countrys,
    default = countrys
)

# Cria um filtro de BARRA DE SELEÇÃO de avaliação
aval_slider = st.sidebar.slider(
    'Avaliação:',
    value= [0.0, 5.0], # É o DEFAUlT, o padrão
    min_value = 0.0,
    max_value = 5.0,
    step = 0.1
)

# Cria um filtro de seleção de intervalo de preço
prices = df['price_range'].unique()
prices = st.sidebar.multiselect(
    'Classificações de preço:',
    prices,
    default = prices
)

# Vinculando os filtros ao DF 
linhas_filtradas = (df['country_name'].isin(country)) & (df['aggregate_rating'] >= aval_slider[0]) & (df['aggregate_rating'] <= aval_slider[1]) & (df['price_range'].isin(prices))
df = df.loc[linhas_filtradas, :]

st.sidebar.markdown(""" --- """) # Divider
# ------------------------------------------------------------------------

st.sidebar.markdown('### Criado por Gabriel Ganassin')
st.sidebar.link_button("Saiba Mais", "https://resumo-gabriel-ganassin.notion.site/Resumo-Gabriel-Ganassin-363e4a3b1a7340ce97470be588a8bdcd")
st.sidebar.link_button("LinkedIn", "www.linkedin.com/in/gabriel-ganassin")
#==========================================================================================


#==========================================================================================
# PÁG PRINCIPAL ===========================================================================
# =========================================================================================

st.markdown('# 🌍 Visão Países')
st.markdown('#####')

# ------------------------------------------------------------------------
with st.container(): 
    st.markdown('## Quantidade de Restaurantes Cadastrados por País')
    
    qnt_restaurantes_por_pais = (df.loc[:, ['restaurant_id', 'country_name']]
                                 .groupby('country_name').nunique()
                                 .sort_values('restaurant_id', ascending=False).reset_index())
    qnt_restaurantes_por_pais = qnt_restaurantes_por_pais.rename(columns={'country_name': 'pais', 'restaurant_id': 'qnt_rest'})
    
    graf = px.bar(qnt_restaurantes_por_pais, x='pais', y='qnt_rest') # Cria o gráfico

    # Personalizações
    graf.update_layout(
        xaxis_title='Países',
        yaxis_title='Qnt. Restaurantes',
        height=500,  # Ajusta a altura
        plot_bgcolor='rgba(211, 211, 211, 0.1)'  # Fundo transparente
    )
    # Personalizar cor e rótulos
    graf.update_traces(
        marker_color='lightsalmon',
        texttemplate='%{y}',
        textposition='outside'
    )
    
    st.plotly_chart( graf, use_container_width=True) # Mostra o gráfico
# ------------------------------------------------------------------------

with st.container(): 
    st.markdown('## Quantidade de Cidades Cadastrados por País')

    qnt_city_por_pais = (df.loc[:, ['city', 'country_name']]
                         .groupby('country_name').nunique()
                         .sort_values('city', ascending=False).reset_index())

    graf = px.bar(qnt_city_por_pais, x='country_name', y='city')

    # Personalizações
    graf.update_layout(
        xaxis_title='Países',
        yaxis_title='Qnt. Cidades',
        height=500,  # Ajusta a altura
        plot_bgcolor='rgba(211, 211, 211, 0.1)'  # Fundo cinza com transparência
    )
    # Personalizar cor e rótulos
    graf.update_traces(
        marker_color='lightsalmon',
        texttemplate='%{y}',
        textposition='outside'
    )
    
    st.plotly_chart( graf, use_container_width=True) # Mostra o gráfico
# ------------------------------------------------------------------------
st.markdown(""" --- """) # Divider
with st.container(): 
    st.markdown('## Avaliação')
    
    maior_avalizacao_pais = (df.loc[:, ['aggregate_rating', 'country_name']]
                             .groupby('country_name').mean().round(2)
                             .sort_values('aggregate_rating', ascending=False).reset_index())

    graf = px.bar(maior_avalizacao_pais, x='country_name', y='aggregate_rating')

    # Personalizações
    graf.update_layout(
        xaxis_title='Países',
        yaxis_title='Avaliação média',
        title='Avaliação Média dos Restaurantes por País',
        width=350,
        height=450,  # Ajusta a altura
        plot_bgcolor='rgba(211, 211, 211, 0.1)'  # Fundo cinza com transparência
    )
    # Personalizar cor e rótulos
    graf.update_traces(
        marker_color='lightsalmon',
        texttemplate='%{y}',
        textposition='outside'
    )
    
    st.plotly_chart( graf, use_container_width=True) # Mostra o gráfico
# ------------------------------------------------------------------------

with st.container(): 
    
    qnt_avaliacoes_por_pais = (df.loc[:, ['votes', 'country_name']]
                               .groupby('country_name').sum()
                               .sort_values('votes', ascending=False).reset_index())

    graf = px.bar(qnt_avaliacoes_por_pais, x='country_name', y='votes')

    # Personalizações
    graf.update_layout(
        xaxis_title='Países',
        yaxis_title='Qnt. de Avaliação',
        title='Quantidade de Avaliações Feitas por País',
        width=350,
        height=450,  # Ajusta a altura
        plot_bgcolor='rgba(211, 211, 211, 0.1)'  # Fundo cinza com transparência
    )
    # Personalizar cor e rótulos
    graf.update_traces(
        marker_color='lightsalmon',
        texttemplate='%{y}',
        textposition='outside'
    )
    
    st.plotly_chart( graf, use_container_width=True) # Mostra o gráfico
# ------------------------------------------------------------------------

st.markdown(""" --- """) # Divider
st.markdown('## Quantidade de Restaurantes por Classificação de Preço')

with st.container(): 
    col1, col2 = st.columns(2)
    with col1:
        qnt_pais_rest_goumet = (df.loc[df['price_range'] == 'gourmet', ['restaurant_id', 'country_name']]
                                .groupby('country_name').nunique()
                                .sort_values('restaurant_id', ascending=False).reset_index())
            
        graf = px.bar(qnt_pais_rest_goumet, x='country_name', y='restaurant_id')

        # Personalizações
        graf.update_layout(
            xaxis_title='Países',
            yaxis_title='Qnt. de Restaurantes',
            title='Gourmet',
            width=350,
            height=450,  # Ajusta a altura
            plot_bgcolor='rgba(211, 211, 211, 0.1)'  # Fundo cinza com transparência
        )
        # Personalizar cor e rótulos
        graf.update_traces(
            marker_color='lightsalmon',
            texttemplate='%{y}',
            textposition='outside'
        )
            
        st.plotly_chart( graf, use_container_width=True) # Mostra o gráfico

    with col2:
        qnt_pais_rest_expensive = (df.loc[df['price_range'] == 'expensive', ['restaurant_id', 'country_name']]
                                .groupby('country_name').nunique()
                                .sort_values('restaurant_id', ascending=False).reset_index())
            
        graf = px.bar(qnt_pais_rest_expensive, x='country_name', y='restaurant_id')

        # Personalizações
        graf.update_layout(
            xaxis_title='Países',
            yaxis_title='Qnt. de Restaurantes',
            title='Expensive',
            width=350,
            height=450,  # Ajusta a altura
            plot_bgcolor='rgba(211, 211, 211, 0.1)'  # Fundo cinza com transparência
        )
        # Personalizar cor e rótulos
        graf.update_traces(
            marker_color='lightsalmon',
            texttemplate='%{y}',
            textposition='outside'
        )
            
        st.plotly_chart( graf, use_container_width=True) # Mostra o gráfico

with st.container(): 
    col1, col2 = st.columns(2)
    with col1:
        qnt_pais_rest_normal = (df.loc[df['price_range'] == 'normal', ['restaurant_id', 'country_name']]
                                .groupby('country_name').nunique()
                                .sort_values('restaurant_id', ascending=False).reset_index())
            
        graf = px.bar(qnt_pais_rest_normal, x='country_name', y='restaurant_id')

        # Personalizações
        graf.update_layout(
            xaxis_title='Países',
            yaxis_title='Qnt. de Restaurantes',
            title='Normal',
            width=350,
            height=450,  # Ajusta a altura
            plot_bgcolor='rgba(211, 211, 211, 0.1)'  # Fundo cinza com transparência
        )
        # Personalizar cor e rótulos
        graf.update_traces(
            marker_color='lightsalmon',
            texttemplate='%{y}',
            textposition='outside'
        )
            
        st.plotly_chart( graf, use_container_width=True) # Mostra o gráfico

    with col2:
        qnt_pais_rest_cheap = (df.loc[df['price_range'] == 'cheap', ['restaurant_id', 'country_name']]
                                .groupby('country_name').nunique()
                                .sort_values('restaurant_id', ascending=False).reset_index())
            
        graf = px.bar(qnt_pais_rest_cheap, x='country_name', y='restaurant_id')

        # Personalizações
        graf.update_layout(
            xaxis_title='Países',
            yaxis_title='Qnt. de Restaurantes',
            title='Cheap',
            width=350,
            height=450,  # Ajusta a altura
            plot_bgcolor='rgba(211, 211, 211, 0.1)'  # Fundo cinza com transparência
        )
        # Personalizar cor e rótulos
        graf.update_traces(
            marker_color='lightsalmon',
            texttemplate='%{y}',
            textposition='outside'
        )
            
        st.plotly_chart( graf, use_container_width=True) # Mostra o gráfico


    
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
    page_title='Cidades', 
    page_icon='🏙️', 
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

st.markdown('# 🏙️ Visão Cidades')
st.markdown('#####')

# ------------------------------------------------------------------------
with st.container(): 
    st.markdown('## TOP 10 Cidades com Mais Restaurantes')
    
    rest_por_city = (df.loc[:, ['restaurant_id', 'city', 'country_name']].groupby(['city', 'country_name']).nunique()
                     .sort_values('restaurant_id', ascending=False).reset_index()).head(10)
    
    
    graf = px.bar(rest_por_city, x='city', y='restaurant_id', color='country_name') # Cria o gráfico

    # Personalizações
    graf.update_layout(
        xaxis_title='Cidades',
        yaxis_title='Qnt. Restaurantes',
        height=500,  # Ajusta a altura
        plot_bgcolor='rgba(211, 211, 211, 0.1)'  # Fundo transparente
    )
    # Personalizar cor e rótulos
    graf.update_traces(
        texttemplate='%{y}',
        textposition='outside'
    )
    
    st.plotly_chart( graf, use_container_width=True) # Mostra o gráfico
st.markdown(""" --- """) # Divider

# ------------------------------------------------------------------------
with st.container(): 
    st.markdown('## TOP Cidades com Restaurantes por Média de Avaliação')
    
    col1, col2 = st.columns(2)
    with col1:
        rest_melhor_por_city = (df.loc[df['aggregate_rating']>4, ['restaurant_id', 'city']].groupby('city')
                                .nunique().sort_values('restaurant_id', ascending=False).reset_index()).head(5)
            
        graf = px.bar(rest_melhor_por_city, x='city', y='restaurant_id')

        # Personalizações
        graf.update_layout(
            xaxis_title='Cidades',
            yaxis_title='Qnt. de Restaurantes',
            title='Top 5 Restaurantes Acima de 4',
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
        rest_pior_por_city = (df.loc[df['aggregate_rating']<2.5, ['restaurant_id', 'city']].groupby('city')
                              .nunique().sort_values('restaurant_id', ascending=False).reset_index()).head(5)
            
        graf = px.bar(rest_pior_por_city, x='city', y='restaurant_id')

        # Personalizações
        graf.update_layout(
            xaxis_title='Cidades',
            yaxis_title='Qnt. de Restaurantes',
            title='Top 5 Restaurantes Abaixo de 2.5',
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
st.markdown(""" --- """) # Divider

# ------------------------------------------------------------------------
with st.container(): 
    st.markdown('## TOP 10 Cidades com Maior Variedade de Culinárias')
    
    qnt_cuisines_por_city = (df.loc[:, ['cuisines', 'city', 'country_name']].groupby(['city', 'country_name'])
                             .nunique().sort_values('cuisines', ascending=False).reset_index()).head(10)
    
    
    graf = px.bar(qnt_cuisines_por_city, x='city', y='cuisines', color='country_name') # Cria o gráfico

    # Personalizações
    graf.update_layout(
        xaxis_title='Cidades',
        yaxis_title='Qnt. Culinárias',
        height=500,  # Ajusta a altura
        plot_bgcolor='rgba(211, 211, 211, 0.1)'  # Fundo transparente
    )
    # Personalizar cor e rótulos
    graf.update_traces(
        texttemplate='%{y}',
        textposition='outside'
    )
    
    st.plotly_chart( graf, use_container_width=True) # Mostra o gráfico

    
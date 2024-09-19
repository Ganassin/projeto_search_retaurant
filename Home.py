import streamlit as st
from PIL import Image
import pandas as pd
# Importando a biblioteca para desenhar o mapa
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Cria um dataframe com os dados já limpos no arquivo limpa_dataset.ipynb
df = pd.read_csv('datasets/zomato_limpo.csv')


# ============================================================================================================================
# LAYOUT DO STREAMLIT
# ============================================================================================================================

# Função que junta as páginas, o streamlit entrende que tem que buscas os arquivos (páginas) dentro de uma pasta chamada pages
st.set_page_config(
    page_title="Home",
    page_icon="📈",
    layout="wide"
)

# =========================================================================================
# SIDEBAR =================================================================================
# =========================================================================================

image_path = 'logo.png' # Logo, deve estar na mesma pasta que o arquivo .py
image = Image.open( image_path )
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

st.sidebar.markdown('### Dados Tratados:')
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")
    
csv = convert_df(df)

st.sidebar.download_button(
    label="Download",
    data=csv,
    file_name="dataset.csv"
)
# ------------------------------------------------------------------------

st.sidebar.markdown(""" --- """) # Divider
st.sidebar.markdown('### Criado por Gabriel Ganassin')
st.sidebar.link_button("Saiba Mais", "https://resumo-gabriel-ganassin.notion.site/Resumo-Gabriel-Ganassin-363e4a3b1a7340ce97470be588a8bdcd")
st.sidebar.link_button("LinkedIn", "www.linkedin.com/in/gabriel-ganassin")
#==========================================================================================


#==========================================================================================
# PÁG PRINCIPAL ===========================================================================
# =========================================================================================

st.write('# Search For Restaurants')

st.markdown(
    """
    ### O melhor lugar para encontrar seu mais novo restaurante favorito!
    
    #### Dados gerais da plataforma
    
    """
)


with st.container(): # Cria uma "subdivisão" ============================================================
    
    col1, col2, col3, col4, col5 = st.columns(5)   
    with col1:
        qnt_restaurantes = df['restaurant_id'].nunique() # Pega a quantidade de restaurantes
        st.metric('Rest. Cadastrados', qnt_restaurantes) # Mostra na tela
    
    with col2:
        qnt_paises = df['country_name'].nunique() # Pega a quantidade de países
        st.metric('Países Cadastrados', qnt_paises)
    
    with col3:
        qnt_city = df['city'].nunique() # Pega a mquantidade de cidades
        st.metric('Cidades Cadastradas', qnt_city) # Mostra na tela
    
    with col4:
        qnt_avalia = df['votes'].sum() # Pega a quantidade de avaliações feitas na plataforma
        qnt_avalia_format = "{:,.0f}".format(qnt_avalia).replace(',', '.') 
        st.metric('Qnt. de Avaliações Feitas', qnt_avalia_format) # Mostra na tela

    with col5:
        qnt_cuisines = df['cuisines'].nunique() # Pega a quantidade de culinárias cadastradas
        st.metric('Culinárias Cadastradas', qnt_cuisines) # Mostra na tela
#========================================================================================================

@st.cache_data
def create_map():
    # Criação do mapa centrado no Brasil
    m = folium.Map(location=[-14.2350, -51.9253], zoom_start=3)
    
    # Criação do cluster de marcadores
    marker_cluster = MarkerCluster().add_to(m)

    # Iterar sobre o DataFrame e adicionar os marcadores ao cluster
    for index, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['restaurant_name'],
            icon=folium.Icon(color=row['rating_color'], icon="info-sign")
        ).add_to(marker_cluster)

    return m

# Renderiza o mapa apenas uma vez
m = create_map()

with st.container():
    st_folium(m, width=1024, height=700)
    st.markdown(""" --- """) # Divider

#========================================================================================================

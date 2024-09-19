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
    page_title='Culinárias', 
    page_icon='🍽️', 
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
    'Selecione um ou mais países:',
    countrys,
    default = countrys
)

# Cria um filtro de seleção de intervalo de preço
prices = df['price_range'].unique()
prices = st.sidebar.multiselect(
    'Classificações de preço:',
    prices,
    default = prices
)

# Vinculando os filtros ao DF 
linhas_filtradas = (df['country_name'].isin(country)) & (df['price_range'].isin(prices))
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

st.markdown('# 🍽️ Visão Culinária')
st.markdown('#####')

# ------------------------------------------------------------------------
with st.container(): 
    st.markdown('## Melhores Restaurantes das Principais Culinárias')
    qnt_restaurantes_por_cuisines = (df.loc[:, ['restaurant_id', 'cuisines']].groupby('cuisines').nunique()
                                     .sort_values('restaurant_id', ascending=False).reset_index()).head(10)
    qnt_restaurantes_por_cuisines = qnt_restaurantes_por_cuisines.rename(columns={'cuisines': 'culinaria', 'restaurant_id': 'qnt_rest'})
    
    graf = px.bar(qnt_restaurantes_por_cuisines, x='culinaria', y='qnt_rest') # Cria o gráfico

    # Personalizações
    graf.update_layout(
        title='Principais Culinárias',
        xaxis_title='Culinárias',
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
    st.markdown('##### Melhores Restaurantes')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        melhores_rest = (df.loc[df['cuisines'] == (qnt_restaurantes_por_cuisines.iloc[0,0]), ['restaurant_id', 'aggregate_rating', 'restaurant_name']]
                         .groupby('restaurant_name').max().sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).reset_index())

        o_melhor_rest = melhores_rest.iloc[0, 0]
        avaliacao = melhores_rest.iloc[0, 2]

        st.markdown(f'{qnt_restaurantes_por_cuisines.iloc[0,0]}: {o_melhor_rest}')
        st.markdown(f'Avaliação: {avaliacao}')

    with col2:
        melhores_rest = (df.loc[df['cuisines'] == (qnt_restaurantes_por_cuisines.iloc[1,0]), ['restaurant_id', 'aggregate_rating', 'restaurant_name']]
                         .groupby('restaurant_name').max().sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).reset_index())

        o_melhor_rest = melhores_rest.iloc[0, 0]
        avaliacao = melhores_rest.iloc[0, 2]

        st.markdown(f'{qnt_restaurantes_por_cuisines.iloc[1,0]}: {o_melhor_rest}')
        st.markdown(f'Avaliação: {avaliacao}')

    with col3:
        melhores_rest = (df.loc[df['cuisines'] == (qnt_restaurantes_por_cuisines.iloc[2,0]), ['restaurant_id', 'aggregate_rating', 'restaurant_name']]
                         .groupby('restaurant_name').max().sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).reset_index())

        o_melhor_rest = melhores_rest.iloc[0, 0]
        avaliacao = melhores_rest.iloc[0, 2]

        st.markdown(f'{qnt_restaurantes_por_cuisines.iloc[2,0]}: {o_melhor_rest}')
        st.markdown(f'Avaliação: {avaliacao}')

    with col4:
        melhores_rest = (df.loc[df['cuisines'] == (qnt_restaurantes_por_cuisines.iloc[3,0]), ['restaurant_id', 'aggregate_rating', 'restaurant_name']]
                         .groupby('restaurant_name').max().sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).reset_index())

        o_melhor_rest = melhores_rest.iloc[0, 0]
        avaliacao = melhores_rest.iloc[0, 2]

        st.markdown(f'{qnt_restaurantes_por_cuisines.iloc[3,0]}: {o_melhor_rest}')
        st.markdown(f'Avaliação: {avaliacao}')

# ------------------------------------------------------------------------
st.markdown(""" --- """) # Divider
st.markdown('## Top Culinárias')

with st.container(): 
    col1, col2 = st.columns(2)
    with col1:
        df_aux = (df.loc[df['cuisines'] != 'Others', ['aggregate_rating', 'cuisines']]
          .groupby('cuisines').mean().reset_index()
          .sort_values(['aggregate_rating', 'cuisines'], ascending=[False, True])
          .reset_index(drop=True)).head(10)
            
        graf = px.bar(df_aux, x='cuisines', y='aggregate_rating')

        # Personalizações
        graf.update_layout(
            xaxis_title='Culinárias',
            yaxis_title='Média Avaliação',
            title='TOP 10 Melhores',
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
        df_aux = (df.loc[((df['cuisines'] != 'Others') & (df['aggregate_rating'] != 0)), ['aggregate_rating', 'cuisines']]
          .groupby('cuisines').mean().reset_index()
          .sort_values(['aggregate_rating', 'cuisines'], ascending=[True, True])
          .reset_index(drop=True)).head(10)
            
        graf = px.bar(df_aux, x='cuisines', y='aggregate_rating')

        # Personalizações
        graf.update_layout(
            xaxis_title='Culinárias',
            yaxis_title='Média Avaliação',
            title='TOP 10 Piores',
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
with st.container(): 
    st.markdown('## TOP Restaurantes')

    melhores_rest = (df.loc[:, ['restaurant_id', 'restaurant_name', 'cuisines', 'country_name', 'city', 'aggregate_rating']]
                     .sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True]).reset_index(drop=True))

    st.dataframe(melhores_rest, use_container_width=True)






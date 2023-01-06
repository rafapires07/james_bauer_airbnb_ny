import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import geopandas
import folium
from folium.plugins import MarkerCluster
from PIL import Image
import plotly.express as px
import streamlit as st
from streamlit_folium import folium_static
import plotly.graph_objects as go

# set wide page
st.set_page_config(layout='wide')


@st.cache(allow_output_mutation=True)
def get_df(path):
    df = pd.read_csv(path)
    return df


def get_geofile(geofile_path):
    geofile = geopandas.read_file(geofile_path)
    return geofile


def transform_df(df):
    # Criando nomes para imóveis sem nomes
    df['name'] = df.apply(lambda x: x['neighbourhood'] + str(x['id']) if pd.isna(x['name']) == True else x['name'],
                          axis=1)

    # Criando nomes para hosts sem nomes
    df['host_name'] = df.apply(
        lambda x: x['neighbourhood'] + str(x['host_id']) if pd.isna(x['host_name']) == True else x['host_name'], axis=1)

    # Criando nova base de Dados retirando os imóveis considerados inativos (Sem número de Reviews e disponibilidade 0)
    df_ativos = df[(df['number_of_reviews'] >= 1) & (df['availability_365'] != 0)].copy()

    # Criando Feature rentability (Calculando a rentabilidade de cada imóvel)
    df_ativos['rentability'] = df_ativos.apply(
        lambda x: (x['price'] * (x['minimum_nights'] + 1) * x['number_of_reviews']) / np.sqrt(x['availability_365']),
        axis=1)

    # Convertendo last_review para formato de data
    df_ativos['last_review'] = pd.to_datetime(df_ativos['last_review'])

    # Retirando dos dados ativos com rentabilidade que foi considerada muito discrepante através da EDA
    df_analise = df_ativos[df_ativos['rentability'] <= 29794.06].copy()

    return df_analise


def create_px_bargraph(df, x, y, color, title, text, unit1, unit2):
    df_graph = df[[x, y]].groupby(by=x).mean().sort_values(by=y).reset_index()
    fig = px.bar(df_graph, x=x, y=y, color=color,
                 title=title, text=text,
                 color_discrete_sequence=('PeachPuff', 'cadetblue', 'darkseagreen', 'LightSkyBlue', 'lightcoral'))
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_traces(texttemplate=unit1 + '%{text:.3s}' + unit2, textposition='outside')
    st.plotly_chart(fig)
    return None


def point_map(df):
    houses = df[
        ['id', 'latitude', 'longitude', 'price', 'rentability', 'number_of_reviews', 'availability_365', 'room_type']]
    fig = px.scatter_mapbox(data_frame=houses, lat='latitude', lon='longitude', color='room_type', text=None,
                            hover_name=None,
                            hover_data={'room_type': True, 'rentability': True, 'latitude': False, 'longitude': False,
                                        'number_of_reviews': True, },
                            custom_data=None, size='number_of_reviews', animation_frame=None, animation_group=None,
                            category_orders=None,
                            labels={'room_type': 'Tipo de imóvel', 'number_of_reviews': 'N° de Reviews',
                                    'rentability': 'Rentabilidade'}, color_discrete_sequence=None,
                            color_discrete_map=None, color_continuous_scale=None,
                            range_color=None, color_continuous_midpoint=None, opacity=None, size_max=15, zoom=10,
                            center=None,
                            mapbox_style='open-street-map', title='AB_NYC_2019', template=None, width=None, height=600)
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
    fig.show()
    return None


def create_px_catplot(df, x, y, col, kind, xlabel):
    sns.set(rc={'axes.facecolor': 'black',
                'figure.facecolor': 'black',
                'text.color': 'white',
                'xtick.color': 'white',
                'ytick.color': 'white',
                'axes.labelcolor': 'white'
                })
    ax1 = sns.catplot(
        data=df, x=x, y=y, col=col, ci=None,
        kind=kind)
    ax1.set_axis_labels("", xlabel)
    ax1.set_titles(col_template="{col_name}")
    for ax in ax1.axes.ravel():
        for c in ax.containers:
            ax.bar_label(c, fmt='%1.1f')
        ax.margins(y=0.2)
    st.pyplot(fig=ax1)
    return None


# Criação de Gráfico de Barras por Média
def create_sns_bargraph_mean(df, x, y, title):
    df_graph = df[[x, y]].groupby(by=x).mean().sort_values(by=y, ascending=False).head(10).reset_index()
    fig1 = plt.figure(figsize=[15, 3])
    ax1 = sns.barplot(data=df_graph, x=x, y=y)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    for i in ax1.containers:
        ax1.bar_label(i, )
    st.pyplot(fig=ax1.figure)
    return None


# Criação de Gráfico de Barras por Soma
def create_sns_bargraph_sum(df, x, y, title):
    df_graph = df[[x, y]].groupby(by=x).sum().sort_values(by=y, ascending=False).head(10).reset_index()
    fig1 = plt.figure(figsize=[15, 3])
    ax1 = sns.barplot(data=df_graph, x=x, y=y)
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    for i in ax1.containers:
        ax1.bar_label(i, )
    st.pyplot(fig=ax1.figure)
    return None


def pages(df_analise, geodata):
    page = st.sidebar.selectbox("Selecione a Página:",
                                ("Problema de Negócio", "Visualização dos Dados", "Hipóteses de Negócio", "Conclusão"))
    # Problema de Negócio
    if page == "Problema de Negócio":
        st.title('Projeto de Insight')
        st.markdown('''O Objetivo deste projeto é gerar insights com base na análise exploratória dos dados da Airbnb 
            NY de 2019.''')
        st.markdown('---')
        st.title('Sobre o Problema de Negócio')
        st.markdown('''O investidor James Bauer gostaria de diversificar seus negócios e começar a investir em 
            imóveis. Ele definiu que compraria imóveis na cidade de Nova York, nos Estados Unidos. Por ser um dos locais 
            mais caros para se viver no País, ele acredita que obterá um retorno satisfatório de seus investimentos caso 
            loque imóveis na cidade.''')

        st.markdown('''Como planeja-se inicialmente locar os imóveis adquiridos, ele definiu que irá utilizar a 
            plataforma Airbnb para esse fim. Para realizar o estudo foi fornecida a base de dados referente aos imóveis 
            da Airbnb em Nova York em 2019. O estudo tem como objetivo a escolha das regiões onde há maior locação, 
            maiores preços, maior rentabilidade, e que fiquem em regiões favoráveis da cidade de Nova York, 
            pois ele acredita que essas características irão ajudá-lo a recuperar o dinheiro investido na aquisição 
            desses imóveis mais rapidamente.''')
        st.markdown('---')
        st.title('Qual o valor em R$ gerado por este projeto?')
        st.markdown('Infelizmente devido a base de dados não possuir os valores dos imóveis,não é possivel estimar com precisão o retorno gerado.')
        st.markdown('Entretando o tempo de retorno do investimento poderia ser calculado com a fórmula abaixo:')
        st.markdown(
            r'''
            $$ R𝑒𝑡𝑢𝑟𝑛 I𝑛𝑣𝑒𝑠𝑡𝑚𝑒𝑛𝑡 = \frac{𝑖𝑛𝑣𝑒𝑠𝑡𝑚𝑒𝑛𝑡}{𝑝𝑟𝑖𝑐𝑒 * (𝑚𝑖𝑛𝑖𝑚𝑢𝑚\_𝑛𝑖𝑔ℎ𝑡𝑠 + 1)}  $$)
            ''')

    # Visualização dos Dados
    if page == "Visualização dos Dados":
        st.title('Visualização dos Dados')
        st.markdown('Clicando no cabeçalho de cada coluna, é possível ordenar os dados de forma ascendente ou '
                    'decrescente')
        st.write(df_analise)
        st.markdown('A feature **Rentability** foi obtida através dos dados com a seguinte fórmula: ')
        st.markdown(
            r'''
            $$ 𝑟𝑒𝑛𝑡𝑎𝑏𝑖𝑙𝑖ty = \frac{𝑝𝑟𝑖𝑐𝑒 * (𝑚𝑖𝑛𝑖𝑚𝑢𝑚\_𝑛𝑖𝑔ℎ𝑡𝑠 + 1) *  n𝑢𝑚𝑏𝑒𝑟\_𝑜𝑓\_𝑟𝑒𝑣𝑖𝑒𝑤𝑠}{ \sqrt{𝑎𝑣𝑎𝑖𝑙𝑎𝑏𝑖𝑙𝑖𝑡𝑦_365}} $$)
            ''')
        st.markdown('---')
        st.subheader('Mapas')
        st.markdown('Selecione o Mapa que deseja visualizar na barra ao lado')

        c1, c2 = st.columns(2)
        st.sidebar.markdown('Selecione os mapas desejados:')
        # Mapa 1
        is_check = st.sidebar.checkbox('Mapa - Imóveis por tipo')
        if is_check:
            with c1:
                st.header('Mapa - Imóveis por tipo')
            df_map = df_analise[
                ['id', 'latitude', 'longitude', 'price', 'rentability', 'number_of_reviews', 'availability_365',
                 'room_type']]
            fig = px.scatter_mapbox(data_frame=df_map, lat='latitude', lon='longitude', color='room_type', text=None,
                                    hover_name=None,
                                    hover_data={'room_type': True, 'rentability': True, 'latitude': False,
                                                'longitude': False, 'number_of_reviews': True, },
                                    custom_data=None, size='number_of_reviews', animation_frame=None,
                                    animation_group=None,
                                    category_orders=None,
                                    labels={'room_type': 'Tipo de imóvel', 'number_of_reviews': 'N° de Reviews',
                                            'rentability': 'Rentabilidade'}, color_discrete_sequence=None,
                                    color_discrete_map=None, color_continuous_scale=None,
                                    range_color=None, color_continuous_midpoint=None, opacity=None, size_max=15,
                                    zoom=10,
                                    center=None,
                                    mapbox_style='open-street-map', title='AB_NYC_2019', template=None, width=None,
                                    height=510)
            fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
            c1.plotly_chart(fig)

        is_check2 = st.sidebar.checkbox('Mapa de Calor - Rentabilidade Média')
        if is_check2:
            with c2:
                st.header('Mapa de Calor - Rentabilidade Média')
            df_map = df_analise[['neighbourhood_group', 'rentability']].groupby(
                by='neighbourhood_group').mean().sort_values(
                by='rentability').reset_index()
            f = folium.Figure(width=900, height=500)
            m = folium.Map(location=[df_analise['latitude'].mean(), df_analise['longitude'].mean()],
                           default_zoom_start=15).add_to(f)
            folium.Choropleth(
                geo_data=geodata,
                name='choropleth',
                data=df_map,
                columns=['neighbourhood_group', 'rentability'],
                key_on='feature.properties.name',
                fill_color='YlOrRd',
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name='AVG RENTABILITY').add_to(m)
            with c2:
                folium_static(m)
        # Filters
        f_neighbourhood = st.sidebar.multiselect('Selecione os Bairros Desejados',
                                                 sorted(set(df_analise['neighbourhood'].unique())))
        f_price = st.sidebar.slider('Selecione a faixa de Preço desejada', min_value=int(df_analise['price'].min()),
                                    max_value=int(df_analise['price'].max()), value=int(df_analise['price'].max()))
        f_roomtype = st.sidebar.multiselect('Selecione o tipo de  imóvel',
                                            sorted(set(df_analise['room_type'].unique())))
        if not f_neighbourhood:
            f_neighbourhood = df_analise['neighbourhood'].unique()

        if not f_roomtype:
            f_roomtype = df_analise['room_type'].unique()

        st.markdown('---')
        st.subheader('Análises Gráficas')

        c1, c2 = st.columns(2)

        with c1:
            create_px_bargraph(df_analise[df_analise['price'] <= f_price &
                                          df_analise['neighbourhood'].isin(f_neighbourhood) &
                                          df_analise['room_type'].isin(f_roomtype)], "neighbourhood_group",
                               "availability_365", 'neighbourhood_group',
                               'Média de Disponibilidade x Regiões', 'availability_365', '', " Days")
        with c2:
            create_px_bargraph(df_analise[df_analise['neighbourhood'].isin(f_neighbourhood) &
                                          df_analise['price'] <= f_price &
                                          df_analise['room_type'].isin(f_roomtype)], "neighbourhood_group", "price",
                               'neighbourhood_group',
                               'Média de Preço x Regiões', 'price', '$ ', "")

        create_sns_bargraph_mean(df_analise[df_analise['neighbourhood'].isin(f_neighbourhood) &
                                            df_analise['price'] <= f_price &
                                            df_analise['room_type'].isin(f_roomtype)],
                                 'neighbourhood',
                                 'rentability', "Neighbourhood vs Rentability Mean")
        create_sns_bargraph_sum(df_analise[df_analise['neighbourhood'].isin(f_neighbourhood) &
                                           df_analise['price'] <= f_price &
                                           df_analise['room_type'].isin(f_roomtype)], 'neighbourhood',
                                'number_of_reviews', "Neighbourhood vs Number os Reviews Sum")

        create_px_catplot(data, "neighbourhood_group", "price", "room_type", "bar", "Rentability")
        create_px_catplot(data, "neighbourhood_group", "price", "room_type", "bar", "Price ($)")
        create_px_catplot(data, "neighbourhood_group", "number_of_reviews", "room_type", "bar",
                          "Number of Reviews")
        create_px_catplot(data, "neighbourhood_group", "availability_365", "room_type", "bar", "Availability 365")

    if page == "Hipóteses de Negócio":
        st.title('Hipótese 1')
        st.markdown('Em média, os aluguéis mais caros da cidade de Nova York estão nas regiões ao entorno do Central '
                    'Park.')
        st.markdown('As regiões ao entorno do Central Park são:')
        st.text('- East Harlem')
        st.text('- Harlem')
        st.text('- Upper East Side')
        st.text('- Upper West Side')
        g1 = df_analise[['neighbourhood', 'price']].groupby(by='neighbourhood'). \
            mean().sort_values(by='price', ascending=False).head(10).reset_index()
        fig = plt.figure(figsize=[15, 2])
        sns.barplot(x='neighbourhood', y='price', data=g1)
        st.pyplot(fig)
        st.subheader('Hipótese Falsa: Como podemos ver a no gráfico acima, na média, os alugueis mais caros são em '
                     'Sea Gate.')

        st.markdown('---')
        st.title('Hipótese 2')
        st.markdown('Staten Island tem em média os aluguéis mais baratos')
        g2 = df_analise[['neighbourhood_group', 'price']].groupby(by='neighbourhood_group').mean().sort_values(
            by='price', ascending=False).reset_index()
        fig = plt.figure(figsize=[15, 2])
        sns.barplot(x='neighbourhood_group', y='price', data=g2)
        st.pyplot(fig)
        st.subheader('Hipótese Falsa: Como podemos ver a hipotese é falsa, na média os alugueis mais baratos são no '
                     'Bronx. Sendo a média do aluguel de Staten Islande 10% maior que no Bronx.')

        st.markdown('---')
        st.title('Hipótese 3')
        st.markdown('Quanto mais reviews, menos tempo o imóvel ficou dispónivel')
        st.write(df_analise[['number_of_reviews', 'availability_365']].corr())
        st.subheader('Hipótese Falsa: Ambos os valores apresentam uma baixa correlação, não tendo uma relação '
                     'especifica')

        st.markdown('---')
        st.title('Hipótese 4')
        st.markdown('Hosts com mais de um lugar cobram mais caro os alugúeis do que aqueles que tem apenas um lugar')
        st.write(df_analise[['calculated_host_listings_count', 'price']].corr())
        st.subheader('Hipótese Falsa: Ambos os valores apresentam uma baixa correlação. Na média, o número de '
                     'imóveis que o Host tem, não impacta no preço do aluguel')

        st.markdown('---')
        st.title('Hipótese 5')
        st.markdown('A categoria Entire home/apt é a mais cara que qualquer outra categoria, independente da região')
        g5 = df_analise[['room_type', 'price']].groupby(by='room_type').mean().sort_values(by='price',
                                                                                           ascending=False).reset_index()
        fig = plt.figure(figsize=[15, 2])
        sns.barplot(x='room_type', y='price', data=g5)
        st.pyplot(fig)
        st.subheader('Hipótese Verdadeira: Dos 3 tipos de imóveis, Entire home/apt é o mais caro. Sendo '
                     'aproximadamente 238% mais caro que o segundo colocado, Private Room.')

    if page == "Conclusão":
        st.title(
            "Quais são os melhores bairros e tipos de imóveis a serem comprados para termos a maior rentabilidade?")
        st.subheader("Com base na análise dos dados mostrados na página de visualização de dados e nas hipóteses "
                     "levantadas, vamos elencar as melhores caracteristicas:")
        st.markdown("- Região com maior rentabilidade média: **Manhattan**")
        st.markdown("- Região com a menor disponibilidade média: **Brooklyn**")
        st.markdown("- Região com os maiores valores de aluguéis em média: **Manhattan**")
        st.markdown("- Tipo de quarto com maior rentabilidade média: **Entire home/apt**")
        st.markdown("- Bairro com maior quantidade de reviews:**Bedford-stuyvesant - Brooklyn**")
        st.markdown("- Bairro com maior rentabilidade média: **DUMBO - Brooklyn**")

        st.markdown("Com base nessas caracteristicas iremos recomendar a compra de imóveis em dois bairros, "
                    "sendo esses **Manhattan** e **Brooklyn**, para aumentar a diversificação e optando "
                    "preferencialmente pelos tipos de quarto **Entire home/apt**. Abaixo os melhores bairros em cada "
                    "um dos dois Burgos para se adquirir imóveis")

        st.markdown('---')
        st.subheader("Manhattan")
        a1 = df_analise[['neighbourhood', 'rentability']][(df_analise['neighbourhood_group'] == 'Manhattan') & (
                df_analise['room_type'] == 'Entire home/apt')].reset_index(drop=True)
        create_sns_bargraph_mean(a1, 'neighbourhood', 'rentability', 'Manhattan - Neighbourhood x Rentability')
        st.subheader("Recomendamos a compra de Entire Home/Apt em Manhattan nos bairros Civic Center e Nolita. Com a "
                     "adição do Harlem, que figura no top 3 bairros com maior número de reviews e no Top 9 dos com "
                     "melhor rentabilidade média.")

        st.markdown('---')
        st.subheader("Brooklyn")
        a2 = df_analise[['neighbourhood', 'rentability']][(df_analise['neighbourhood_group'] == 'Brooklyn') & (
                df_analise['room_type'] == 'Entire home/apt')].reset_index(drop=True)
        create_sns_bargraph_mean(a2, 'neighbourhood', 'rentability', 'Brooklyn - Neighbourhood x Rentability')
        st.subheader("Recomendamos a compra de Entire Home/Apt em Brooklyn nos bairros DUMBO e Park Slope. Com a "
                     "adição de Williamsburg, que figura no top 2 bairros com maior número de reviews e no Top 8 dos "
                     "com melhor rentabilidade média.")


if __name__ == '__main__':
    path = 'AB_NYC_2019.csv'
    data = get_df(path)
    geo = get_geofile('new-york-city-boroughs.geojson')
    data_analise = transform_df(data)
    pages(data_analise, geo)

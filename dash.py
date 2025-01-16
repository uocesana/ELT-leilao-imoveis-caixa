import streamlit as st
import pandas as pd
import plotly.express as px
import mysql.connector
import json
import requests
from credenciais import host, user, password, database
st.set_page_config(layout="wide")


def carregar_dados_mysql():
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lista_imoveis")
    dados = cursor.fetchall()
    conn.close()
    df = pd.DataFrame(dados)
    return df


def exibir_dados(df):
    st.title('Imóveis de Leilão - Caixa Econômica Federal')
    df['data_processamento'] = pd.to_datetime(df['data_processamento'])
    st.text(f'Dados atualizados em: {
            df["data_processamento"].max().strftime("%d/%m/%Y")}')

    col1, col2, col3, col4, col5 = st.columns(5)
    df['preco'] = pd.to_numeric(df['preco'], errors='coerce')
    with col1:
        st.metric('Total de Imóveis', f'{df.shape[0]:,.0f}', border=True)
    with col2:
        st.metric('Total R$ em Negócio', f'R$ {
                  df["preco"].sum():,.0f}', border=True)
    with col3:
        st.metric('Menor Preço', f'R$ {df["preco"].min():,.0f}', border=True)
    with col4:
        st.metric('Maior Preço', f'R$ {df["preco"].max():,.0f}', border=True)
    with col5:
        st.metric('Preço Médio', f'R$ {df["preco"].mean():,.0f}', border=True)

    st.subheader('Dados Carregados')
    campos_renomeados = df.rename(columns={
        'metro_quadrado_m3': 'metro_quadrado_m2',
        'metro_quadrado_area_total_m3': 'area_total_m2',
        'preco': 'Preço'
    })
    st.data_editor(campos_renomeados, width=5000, height=250)

    col1, col2 = st.columns(2)
    with col1:
        # 📊 Gráfico de colunas verticais: Quantidade de Imóveis por UF
        st.subheader('Quantidade de Imóveis por UF')
        if 'uf' in df.columns:
            uf_count = df['uf'].value_counts().reset_index()
            uf_count.columns = ['UF', 'Quantidade']
            fig_bar = px.bar(uf_count, x='UF', y='Quantidade',
                             title="Quantidade de Imóveis por UF",
                             color='Quantidade', text_auto=True)
            st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader('Preço Médio de Imóveis por UF')
        if 'uf' in df.columns:
            media_valores_uf = df.groupby('uf')['preco'].mean().reset_index()
            media_valores_uf.columns = ['UF', 'Média de Valor']
            # Ordenando os valores de preço médio de forma decrescente
            media_valores_uf = media_valores_uf.sort_values(
                by='Média de Valor', ascending=False)
            fig_bar = px.bar(media_valores_uf, x='UF', y='Média de Valor',
                             title="Média de Valores dos Imóveis por UF",
                             color='Média de Valor', text_auto=True)
            st.plotly_chart(fig_bar, use_container_width=True)

    # 🗺️ Gráfico de Mapa: Média de Valores dos Imóveis por Estado usando GeoJSON
    st.subheader('Média de Valores dos Imóveis por Estado')

    # Importando GeoJSON com os estados brasileiros
    url_geojson = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
    geojson = requests.get(url_geojson).json()

    # Calcular a média de preços por estado
    df['uf'] = df['uf'].str.upper()
    media_valores_uf = df.groupby('uf')['preco'].mean().reset_index()
    media_valores_uf.columns = ['UF', 'Média de Valor']

    # Dicionário com latitudes e longitudes de cada estado do Brasil
    coordenadas_estados = {
        "AC": {"lat": -9.0238, "lon": -70.811},
        "AL": {"lat": -9.5713, "lon": -36.782},
        "AP": {"lat": 0.902, "lon": -51.055},
        "AM": {"lat": -3.4168, "lon": -65.856},
        "BA": {"lat": -12.5797, "lon": -41.700},
        "CE": {"lat": -5.498, "lon": -39.320},
        "DF": {"lat": -15.799, "lon": -47.864},
        "ES": {"lat": -19.183, "lon": -40.308},
        "GO": {"lat": -15.827, "lon": -49.836},
        "MA": {"lat": -5.420, "lon": -45.440},
        "MT": {"lat": -12.681, "lon": -56.921},
        "MS": {"lat": -20.772, "lon": -54.786},
        "MG": {"lat": -18.512, "lon": -44.555},
        "PA": {"lat": -3.797, "lon": -52.482},
        "PB": {"lat": -7.121, "lon": -36.724},
        "PR": {"lat": -25.252, "lon": -52.021},
        "PE": {"lat": -8.813, "lon": -36.954},
        "PI": {"lat": -7.718, "lon": -42.728},
        "RJ": {"lat": -22.906, "lon": -43.172},
        "RN": {"lat": -5.402, "lon": -36.954},
        "RS": {"lat": -30.034, "lon": -51.217},
        "RO": {"lat": -11.505, "lon": -63.580},
        "RR": {"lat": 1.989, "lon": -61.326},
        "SC": {"lat": -27.242, "lon": -50.218},
        "SP": {"lat": -23.550, "lon": -46.633},
        "SE": {"lat": -10.574, "lon": -37.385},
        "TO": {"lat": -10.175, "lon": -48.298}
    }

    # Adicionar colunas de latitude e longitude ao DataFrame
    media_valores_uf['lat'] = media_valores_uf['UF'].map(
        lambda x: coordenadas_estados[x]['lat'])
    media_valores_uf['lon'] = media_valores_uf['UF'].map(
        lambda x: coordenadas_estados[x]['lon'])

    # Criar o mapa usando lat e lon reais
    fig_mapbox = px.scatter_mapbox(
        media_valores_uf,
        lat='lat',
        lon='lon',
        size='Média de Valor',
        hover_name='UF',
        hover_data=['Média de Valor'],
        color='Média de Valor',
        color_continuous_scale="Viridis",
        zoom=5.5,  # Ajuste do zoom mais próximo
        height=800  # Aumentando a altura do mapa para uma abertura maior
    )

    # Melhorando o estilo do mapa para visualização detalhada
    fig_mapbox.update_layout(
        mapbox_style="carto-darkmatter",  # Estilo mais limpo e aberto
        margin={"r": 0, "t": 0, "l": 0, "b": 0}  # Remover margens
    )

    st.plotly_chart(fig_mapbox, use_container_width=True)


if __name__ == "__main__":
    df = carregar_dados_mysql()
    exibir_dados(df)

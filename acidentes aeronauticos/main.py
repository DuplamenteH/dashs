import  pandas as pd
import  streamlit as st
import numpy as np
import pydeck as pdk

data_url = "https://raw.githubusercontent.com/carlosfab/curso_data_science_na_pratica/master/modulo_02/ocorrencias_aviacao.csv"

@st.cache
def load_Data():
    """
        Carrega os dados e deixa guardado na memoria para não recarregalos sempre.
    :return: -> um Dataframe já com os dados prontos.
    """
    columns = {
        'ocorrencia_latitude': 'latitude',
        'ocorrencia_longitude': 'longitude',
        'ocorrencia_dia': 'data',
        'ocorrencia_classificacao': 'classificacao',
        'ocorrencia_tipo': 'tipo',
        'ocorrencia_tipo_categoria': 'tipo_categoria',
        'ocorrencia_tipo_icao': 'tipo_icao',
        'ocorrencia_aerodromo': 'aerodromo',
        'ocorrencia_cidade': 'cidade',
        'investigacao_status': 'status',
        'divulgacao_relatorio_numero': 'relatorio_numero',
        'total_aeronaves_envolvidas': 'aeronaves_envolvidas'
    }

    data = pd.read_csv(data_url,index_col='codigo_ocorrencia')
    data = data.rename(columns=columns)
    data.data = data.data+" "+data.ocorrencia_horario
    data.data = pd.to_datetime(data.data)
    data = data[list(columns.values())]

    labels = data.classificacao.unique().tolist()

    return data, labels

# carregando os dados
df,labels = load_Data()

#side bar
st.sidebar.header("Parâmetros") # ->parâmetros e números de ocorrencias
info_side = st.sidebar.empty() # -> placeholder, para filtradas que só serão carregadas depois

# Slider de seleção do ano
st.sidebar.subheader("Ano")
ano_por_filtro = st.sidebar.slider("Escolha o ano desejado",2008,2018,2017)

#checkbox da tabela
st.sidebar.subheader("Tabela")
tabela = st.sidebar.empty() # valor padrão para começar vazio

label_para_Filtro = st.sidebar.multiselect(
    label="Escolha a classificação da ocorrência",
    options=labels,
    default=["INCIDENTE","ACIDENTE"]
)

# Informação no rodapé da Sidebar
st.sidebar.markdown("""
A base de dados de ocorrências aeronáuticas é gerenciada pelo ***Centro de Investigação e Prevenção de Acidentes 
Aeronáuticos (CENIPA)***.
""")

# Somente aqui os dados filtrados por ano são atualizados em novo dataframe
filtered_df = df[(df.data.dt.year == ano_por_filtro) & (df.classificacao.isin(label_para_Filtro))]

# Aqui o placehoder vazio finalmente é atualizado com dados do filtered_df
info_side.info("{} ocorrências selecionadas.".format(filtered_df.shape[0]))


# MAIN
st.title("CENIPA - Acidentes Aeronáuticos")
st.markdown(f"""
            ℹ️ Estão sendo exibidas as ocorrências classificadas como **{", ".join(label_para_Filtro)}**
            para o ano de **{ano_por_filtro}**.
            """)

# raw data (tabela) dependente do checkbox
if tabela.checkbox("Mostrar tabela de dados"):
    st.write(filtered_df)


# mapa
st.subheader("Mapa de ocorrências")
st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=-22.96592,
        longitude=-43.17896,
        zoom=3,
        pitch=50
    ),
    layers=[
        pdk.Layer(
            'HexagonLayer',
            data=filtered_df,
            disk_resolution=12,
            radius=30000,
            get_position='[longitude,latitude]',
            get_fill_color='[255, 255, 255, 255]',
            get_line_color="[255, 255, 255]",
            auto_highlight=True,
            elevation_scale=1500,
            # elevation_range=[0, 3000],
            # get_elevation="norm_price",
            pickable=True,
            extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=filtered_df,
            get_position='[longitude, latitude]',
            get_color='[255, 255, 255, 30]',
            get_radius=60000,
        ),
    ],
))
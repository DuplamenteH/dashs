# importações

import  pandas as pd
import  streamlit as st
import numpy as np

pathData = "https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"
data_column = "date/time"

@st.cache
def load_data(nrows):
    data = pd.read_csv(pathData, nrows=nrows)
    lowercase = lambda x:str(x).lower()
    data.rename(lowercase,axis="columns", inplace=True)
    data["date/time"]=pd.to_datetime(data["date/time"])
    return data

data_load_state = st.text("Carregando dados ...")
data = load_data(10000)
data_load_state.text("Dados carregados")

if st.checkbox("Mostrar Raw Data"):
    st.subheader("Raw Data")
    st.write(data)

st.subheader("Número de corridas por hora")
hist_values = np.histogram(data[data_column].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[data_column].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)

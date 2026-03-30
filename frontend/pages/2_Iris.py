import streamlit as st
import pandas as pd

st.set_page_config(page_title="Iris Dataset", layout='wide', page_icon="🌸")

st.title("Iris Dataset Analysis")

@st.cache_data(ttl=10)
def load_data():
    df = pd.read_csv('data/Iris.csv')
    print("Загрузка снова...")
    return df


df = load_data()
species_options = df['Species'].unique()

select_species = st.selectbox(
    label='Choose class:',
    options=species_options,
    label_visibility='collapsed',
    index=None
)
filtered_df = df[df['Species'] == select_species]

st.dataframe(filtered_df)

x_axis = "Id"
y_axis = st.selectbox(
    "Y", 
    df.columns[::-1]
)

st.scatter_chart(
    filtered_df,
    x=x_axis,
    y=y_axis
)



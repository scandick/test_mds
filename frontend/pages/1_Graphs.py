import streamlit as st
import numpy as np
import pandas as pd


with st.sidebar:
    delta = st.slider("Delta", 0, 10, 2)

col_1, col_2 = st.columns(2)

x = np.linspace(0, 10, 100)
y = np.sin(x) + delta

df = pd.DataFrame({
    "x": x,
    "sin(x)": y
})

with col_2:
    st.header("Sinus")
    st.line_chart(df.set_index("x"))
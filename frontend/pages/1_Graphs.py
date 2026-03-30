import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Iris Dataset", layout='wide', page_icon="🌸")

if "delta" not in st.session_state:
    st.session_state.delta = None

with st.sidebar:
    st.session_state.delta = st.slider("Delta", 0, 10, st.session_state.delta)

col_1, col_2 = st.columns(2)

x = np.linspace(0, 10, 100)
y = np.sin(x) + st.session_state.delta

df = pd.DataFrame({
    "x": x,
    "sin(x)": y
})

with col_2:
    st.header("Sinus")
    st.line_chart(df.set_index("x"))

expander = st.expander("DEBUG",
                       expanded=True)
expander.text(st.session_state,)

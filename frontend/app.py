import streamlit as st

st.title("Demo Streamlit")

name = st.text_input("What is your name?", placeholder="Type your name here...")

number = st.slider("Select a number", 0, 100, 5)

#Кнопка для расчёта
if st.button("Calculate"):
    result = number**2
    st.write(f"Hello, {name}! The square of {number} is {result}.")
    st.balloons()
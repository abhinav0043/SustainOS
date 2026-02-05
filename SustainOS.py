import streamlit as st
import pandas as pd

st.title("ASOS – AI-Driven Adaptive Sustainability System")

st.write(
    "This prototype predicts future energy demand, explains risks, "
    "and recommends adaptive sustainability actions."
)

st.header("Upload Campus Energy Data")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    st.subheader("Historical Energy Usage")
    st.line_chart(data["Energy_Usage_kWh"])

    st.success("Data loaded successfully!")
else:
    st.info("Please upload a CSV file to begin.")

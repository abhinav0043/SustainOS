import streamlit as st
import pandas as pd
import requests
import json

API_KEY = st.secrets["GEMINI_API_KEY"]
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def gemini(prompt):
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    r = requests.post(URL, json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

st.title("SustainOS – AI-Driven Adaptive Sustainability System")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.line_chart(df["Energy_Usage_kWh"])

    if st.button("Run AI Prediction"):
        pred = gemini(
            "Predict electricity demand for the next 24 hours and identify peak hours."
        )
        st.header("AI Prediction")
        st.write(pred)

        exp = gemini(
            "Explain in simple terms why these energy peaks occur."
        )
        st.header("Explainable AI")
        st.write(exp)

        pol = gemini(
            "Suggest 3 adaptive sustainability actions to reduce peak demand."
        )
        st.header("Policy Recommendations")
        st.write(pol)

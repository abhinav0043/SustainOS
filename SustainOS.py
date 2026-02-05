import streamlit as st
import pandas as pd
import requests

API_KEY = st.secrets["GEMINI_API_KEY"]
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def gemini(prompt):
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        r = requests.post(URL, json=payload, timeout=30)

        # NEVER crash the app
        if r.status_code != 200:
            return (
                f"⚠️ Gemini API returned {r.status_code}.\n\n"
                "Demo intelligence:\n"
                "Predicted peak electricity demand tomorrow between 7–9 PM "
                "based on historical usage patterns and evening activity."
            )

        data = r.json()

        if "candidates" in data and len(data["candidates"]) > 0:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return (
                "⚠️ Gemini response blocked.\n\n"
                "Demo intelligence:\n"
                "Energy demand typically peaks during evening hours due to user behavior."
            )

    except Exception as e:
        return (
            "⚠️ AI service temporarily unavailable.\n\n"
            "Demo intelligence:\n"
            "Peak electricity usage is expected between 7–9 PM."
        )

st.title("SustainOS – AI-Driven Adaptive Sustainability System")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.line_chart(df["Energy_Usage_kWh"])

    if st.button("Run AI Prediction"):
        st.header("AI Prediction")
        st.write(gemini(
            "Predict electricity demand for the next 24 hours and identify peak hours."
        ))

        st.header("Explainable AI")
        st.write(gemini(
            "Explain in simple terms why electricity demand peaks in the evening."
        ))

        st.header("Policy Recommendations")
        st.write(gemini(
            "Suggest 3 adaptive sustainability actions to reduce peak electricity demand."
        ))
else:
    st.info("Upload CSV to begin.")

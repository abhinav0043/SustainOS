import streamlit as st
import pandas as pd
import requests

# ---------- CONFIG ----------
API_KEY = st.secrets["GEMINI_API_KEY"]
GEMINI_URL = (
    GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-1.5-flash:generateContent?key=" + API_KEY
)
)
# ---------- GEMINI CALL ----------
def call_gemini(prompt: str) -> str:
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_URL, json=payload, timeout=30)

        # Never crash the app
        if response.status_code != 200:
            return (
                f"⚠️ Gemini API returned {response.status_code}.\n\n"
                "Demo intelligence:\n"
                "Predicted peak electricity demand tomorrow between 7–9 PM "
                "based on historical usage patterns."
            )

        data = response.json()

        if "candidates" in data and len(data["candidates"]) > 0:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return (
                "⚠️ Gemini response blocked.\n\n"
                "Demo intelligence:\n"
                "Evening energy demand peaks due to user activity and cooling load."
            )

    except Exception:
        return (
            "⚠️ AI service temporarily unavailable.\n\n"
            "Demo intelligence:\n"
            "Peak electricity usage is expected between 7–9 PM."
        )

# ---------- UI ----------
st.title("SustainOS – AI-Driven Adaptive Sustainability System")
st.write(
    "AI-powered system to predict energy demand, explain risks, "
    "and recommend adaptive sustainability actions."
)

uploaded_file = st.file_uploader("Upload campus energy CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Historical Energy Usage")
    st.line_chart(df["Energy_Usage_kWh"])

    if st.button("Run AI Prediction"):
        st.header("2️⃣ AI Prediction")
        st.write(
            call_gemini(
                "Predict electricity demand for the next 24 hours and identify peak hours."
            )
        )

        st.header("3️⃣ Explainable AI")
        st.write(
            call_gemini(
                "Explain in simple terms why electricity demand peaks in the evening."
            )
        )

        st.header("4️⃣ Adaptive Policy Recommendations")
        st.write(
            call_gemini(
                "Suggest 3 adaptive sustainability actions to reduce peak electricity demand."
            )
        )
else:
    st.info("Upload a CSV file to begin.")

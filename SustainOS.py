import streamlit as st
import pandas as pd
import requests
import json

# ---------------- CONFIG ----------------
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1/models/"
    "gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY
)

st.title("SustainOS – AI-Driven Adaptive Sustainability System")
st.write(
    "SustainOS predicts future energy demand, explains risks, "
    "and recommends adaptive sustainability actions."
)

# ---------------- DATA UPLOAD ----------------
st.header("1️⃣ Upload Campus Energy Data")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

def call_gemini(prompt):
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(
        GEMINI_URL,
        headers=headers,
        data=json.dumps(payload),
        timeout=30
    )

    data = response.json()

    # ---- SAFE PARSING ----
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return (
            "⚠️ AI response unavailable at the moment.\n\n"
            "Demo output:\n"
            "Predicted peak electricity demand tomorrow between 7–9 PM, "
            "driven by historical usage patterns and evening activity."
        )

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    st.subheader("Historical Energy Usage")
    st.line_chart(data["Energy_Usage_kWh"])
    st.success("Data loaded successfully!")

    if st.button("Run AI Prediction"):
        with st.spinner("AI is analyzing future demand..."):

            # -------- PREDICTION --------
            prediction_prompt = f"""
            You are an energy forecasting AI for a university campus.

            Historical hourly electricity usage data:
            {data.tail(48).to_string()}

            Predict electricity usage for the next 24 hours
            and identify peak risk hours.
            """

            prediction_text = call_gemini(prediction_prompt)
            st.header("2️⃣ AI Prediction")
            st.write(prediction_text)

            # -------- EXPLANATION --------
            explanation_prompt = """
            Explain in simple language why the predicted energy spike occurs.
            """

            explanation_text = call_gemini(explanation_prompt)
            st.header("3️⃣ Explainable AI")
            st.write(explanation_text)

            # -------- POLICY --------
            policy_prompt = """
            Suggest 3 adaptive sustainability actions
            to reduce peak electricity demand.
            """

            policy_text = call_gemini(policy_prompt)
            st.header("4️⃣ Adaptive Policy Recommendations")
            st.write(policy_text)

else:
    st.info("Please upload a CSV file to begin.")

import streamlit as st
import pandas as pd
import json
import vertexai
from vertexai.preview.generative_models import GenerativeModel

# -------- AUTH SETUP --------
creds = json.loads(st.secrets["GOOGLE_APPLICATION_CREDENTIALS"])

vertexai.init(
    project=creds["project_id"],
    location="us-central1",
    credentials=creds
)

model = GenerativeModel("gemini-1.0-pro")

# -------- UI --------
st.title("SustainOS – AI-Driven Adaptive Sustainability System")
st.write(
    "Predicts future energy demand, explains risks, "
    "and recommends adaptive sustainability actions."
)

st.header("1️⃣ Upload Campus Energy Data")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.line_chart(data["Energy_Usage_kWh"])
    st.success("Data loaded")

    if st.button("Run AI Prediction"):
        with st.spinner("AI reasoning in progress..."):

            prediction_prompt = f"""
            You are an energy forecasting AI for a university campus.

            Based on recent patterns, predict electricity demand
            for the next 24 hours and identify peak risk periods.
            """

            prediction = model.generate_content(prediction_prompt)

            st.header("2️⃣ AI Prediction")
            st.write(prediction.text)

            explanation = model.generate_content(
                "Explain in simple terms why these energy peaks occur."
            )

            st.header("3️⃣ Explainable AI")
            st.write(explanation.text)

            policy = model.generate_content(
                "Suggest 3 adaptive sustainability actions to reduce peak demand."
            )

            st.header("4️⃣ Adaptive Policy Recommendations")
            st.write(policy.text)
else:
    st.info("Upload CSV to begin.")

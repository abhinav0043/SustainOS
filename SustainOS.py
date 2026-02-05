import streamlit as st
import pandas as pd
import google.generativeai as genai

# ---------------- CONFIG ----------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("models/gemini-1.0-pro")

st.title("SustainOS – AI-Driven Adaptive Sustainability System")
st.write(
    "SustainOS predicts future energy demand, explains risks, "
    "and recommends adaptive sustainability actions."
)

# ---------------- DATA UPLOAD ----------------
st.header("1️⃣ Upload Campus Energy Data")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    st.subheader("Historical Energy Usage")
    st.line_chart(data["Energy_Usage_kWh"])
    st.success("Data loaded successfully!")

    # ---------------- BUTTON ----------------
    if st.button("Run AI Prediction"):
        with st.spinner("AI is analyzing future demand..."):

            # --------- PREDICTION PROMPT ---------
            prediction_prompt = f"""
            You are an energy forecasting AI for a university campus.

            Historical hourly electricity usage data:
            {data.tail(48).to_string()}

            Tasks:
            1. Predict electricity usage for the next 24 hours.
            2. Identify peak risk hours.
            """

            prediction = model.generate_content(prediction_prompt)

            st.header("2️⃣ AI Prediction")
            st.write(prediction.text)

            # --------- EXPLANATION PROMPT ---------
            explanation_prompt = """
            Explain in simple, non-technical language
            why the predicted energy spikes may occur.
            """

            explanation = model.generate_content(explanation_prompt)

            st.header("3️⃣ Explainable AI")
            st.write(explanation.text)

            # --------- POLICY PROMPT ---------
            policy_prompt = """
            Based on the predicted energy demand,
            suggest 3 adaptive sustainability actions
            a campus administrator can take today
            to reduce peak load tomorrow.
            """

            policies = model.generate_content(policy_prompt)

            st.header("4️⃣ Adaptive Policy Recommendations")
            st.write(policies.text)

else:
    st.info("Please upload a CSV file to begin.")

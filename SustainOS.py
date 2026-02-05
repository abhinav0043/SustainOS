import streamlit as st
import pandas as pd
import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel

# ---------- AUTH ----------
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp"]
)

vertexai.init(
    project=st.secrets["gcp"]["project_id"],
    location="us-central1",
    credentials=credentials
)

model = GenerativeModel("gemini-1.5-flash-001")

# ---------- UI ----------
st.title("SustainOS – AI-Driven Adaptive Sustainability System")
st.write(
    "Predicts future energy demand, explains risks, "
    "and recommends adaptive sustainability actions."
)

st.header("1️⃣ Upload Campus Energy Data")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.subheader("Historical Energy Usage")
    st.line_chart(data["Energy_Usage_kWh"])
    st.success("Data loaded")

    if st.button("Run AI Prediction"):
        with st.spinner("AI reasoning in progress..."):
            prediction_prompt = (
                "You are an energy forecasting AI for a university campus. "
                "Predict electricity demand for the next 24 hours and identify peak risk periods."
            )
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

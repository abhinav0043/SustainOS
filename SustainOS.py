import streamlit as st
import pandas as pd
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

st.title("SustainOS – AI-Driven Adaptive Sustainability System")
st.write(
    "This system predicts future energy demand, explains risks, "
    "and recommends adaptive sustainability actions."
)

st.header("1️⃣ Upload Campus Energy Data")
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)

    st.subheader("Historical Energy Usage")
    st.line_chart(data["Energy_Usage_kWh"])

    st.success("Data loaded successfully!")

    st.header("2️⃣ AI Prediction: Next 24 Hours")

    prompt = f"""
    You are an energy forecasting AI for a university campus.

    Here is historical hourly electricity usage data:
    {data.tail(48).to_string()}

    Tasks:
    1. Predict electricity usage for the next 24 hours.
    2. Identify peak risk hours.
    3. Respond in simple text.
    """

    if st.button("Run AI Prediction"):
        with st.spinner("AI is analyzing future demand..."):
            response = model.generate_content(prompt)
            st.write(response.text)

else:
    st.info("Please upload a CSV file to begin.")

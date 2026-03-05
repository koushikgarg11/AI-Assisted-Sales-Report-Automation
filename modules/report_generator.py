import streamlit as st
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Load model
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_report(df):

    data_sample = df.head(20).to_string()

    prompt = f"""
    Generate a professional analytics report from this dataset.

    Dataset preview:
    {data_sample}

    Include the following sections:

    1. Executive Summary
    2. Key Metrics
    3. Trends and Patterns
    4. Business Recommendations
    """

    response = model.generate_content(prompt)

    return response.text

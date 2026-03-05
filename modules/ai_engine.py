import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_ai_summary(df):

    preview = df.head(20).to_string()

    prompt = f"""
    Analyze this dataset and generate insights.

    Dataset preview:
    {preview}

    Provide:
    - Key trends
    - Patterns
    - Business insights
    """

    response = model.generate_content(prompt)

    return response.text

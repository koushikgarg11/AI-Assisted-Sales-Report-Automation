import google.generativeai as genai
import streamlit as st

@st.cache_resource
def get_model(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")

def generate_ai_summary(df, api_key: str):
    model = get_model(api_key)
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

import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_ai_summary(df):

    data_sample = df.head(20).to_string()

    prompt = f"""
    Analyze this dataset sample and provide business insights.

    Dataset:
    {data_sample}

    Give:
    - Key trends
    - Interesting patterns
    - Business insights
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content

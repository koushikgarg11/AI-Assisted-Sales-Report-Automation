import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_report(df):

    data_sample = df.head(20).to_string()

    prompt = f"""
    Generate a professional analytics report from this dataset.

    Dataset preview:
    {data_sample}

    Include:
    Executive Summary
    Key Metrics
    Business Recommendations
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content

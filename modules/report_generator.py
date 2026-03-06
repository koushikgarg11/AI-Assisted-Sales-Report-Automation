import google.generativeai as genai
import streamlit as st
import time


@st.cache_resource
def get_model():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    return genai.GenerativeModel("gemini-2.5-flash")


def generate_report(df):
    model = get_model()
    data_sample = df.head(10).to_string()
    prompt = f"""Generate a concise professional analytics report. Max 300 words.

Dataset:
{data_sample}

Sections:
1. Executive Summary
2. Key Metrics
3. Trends and Patterns
4. Business Recommendations"""

    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            err = str(e)
            if "ResourceExhausted" in err or "429" in err:
                if attempt < 2:
                    time.sleep((attempt + 1) * 10)
                    continue
                return "⚠️ Service busy. Please try again in a minute."
            if "404" in err or "not found" in err.lower():
                return "⚠️ Model unavailable. Please contact the app owner."
            return f"⚠️ Error: {err}"

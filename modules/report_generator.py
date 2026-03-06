import google.generativeai as genai
import streamlit as st
import time


@st.cache_resource
def get_model(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def generate_report(df, api_key: str):
    model = get_model(api_key)

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
                return "⚠️ Quota exceeded. Wait a minute or get a new key at aistudio.google.com/apikey"
            if "API_KEY_INVALID" in err or "401" in err:
                return "⚠️ Invalid API key. Re-enter your Gemini key in the sidebar."
            if "404" in err or "not found" in err.lower():
                return "⚠️ Model not available. Check aistudio.google.com for current models."
            return f"⚠️ Error: {err}"

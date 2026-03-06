import google.generativeai as genai
import streamlit as st
import time


@st.cache_resource
def get_model():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    return genai.GenerativeModel("gemini-2.5-flash")


def generate_ai_summary(df):
    model = get_model()
    preview = df.head(10).to_string()
    prompt = f"""Analyze this sales dataset. Be concise, max 200 words.

Data:
{preview}

Give:
- 3 key trends
- 2 patterns
- 3 business recommendations"""

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

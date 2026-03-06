import google.generativeai as genai
import streamlit as st
import time


@st.cache_resource
def get_model(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def generate_ai_summary(df, api_key: str):
    model = get_model(api_key)

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
                return "⚠️ Quota exceeded. Wait a minute or get a new key at aistudio.google.com/apikey"
            if "API_KEY_INVALID" in err or "401" in err:
                return "⚠️ Invalid API key. Re-enter your Gemini key in the sidebar."
            if "404" in err or "not found" in err.lower():
                return "⚠️ Model not available. The model name may have changed — check aistudio.google.com"
            return f"⚠️ Error: {err}"

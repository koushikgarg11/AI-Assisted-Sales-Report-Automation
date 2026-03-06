import google.generativeai as genai
import streamlit as st


@st.cache_resource
def get_model(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash-lite")  # lighter = less quota


def generate_ai_summary(df, api_key: str):
    try:
        model = get_model(api_key)

        # Limit to 10 rows + basic stats to reduce token usage
        preview = df.head(10).to_string()
        stats = df.describe(include="all").to_string()

        prompt = f"""Analyze this dataset briefly. Be concise.

Dataset preview (10 rows):
{preview}

Basic stats:
{stats}

Provide:
- 3 key trends
- 2 notable patterns
- 3 business insights
Keep response under 300 words."""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        err = str(e)
        if "ResourceExhausted" in err or "429" in err:
            return "⚠️ Gemini API quota exceeded. Wait a few minutes or get a new key at aistudio.google.com/apikey"
        if "API_KEY_INVALID" in err or "401" in err:
            return "⚠️ Invalid API key. Please check and re-enter your Gemini API key."
        if "404" in err or "not found" in err.lower():
            return "⚠️ Model not found. Try updating the model name in ai_engine.py."
        return f"⚠️ Unexpected error: {err}"

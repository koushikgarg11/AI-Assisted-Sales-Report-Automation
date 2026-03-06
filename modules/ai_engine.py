import google.generativeai as genai
import streamlit as st
import time


@st.cache_resource
def get_model(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash-8b")  # highest free tier quota


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

    # Retry up to 3 times with backoff
    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            err = str(e)

            if "ResourceExhausted" in err or "429" in err:
                if attempt < 2:
                    wait = (attempt + 1) * 10  # 10s, then 20s
                    time.sleep(wait)
                    continue
                return "⚠️ Quota exceeded. Try again in a minute or upgrade your Gemini plan at aistudio.google.com"

            if "API_KEY_INVALID" in err or "401" in err:
                return "⚠️ Invalid API key. Re-enter your Gemini key in the sidebar."

            if "404" in err or "not found" in err.lower():
                return "⚠️ Model not available. Check aistudio.google.com for available models."

            return f"⚠️ Error: {err}"

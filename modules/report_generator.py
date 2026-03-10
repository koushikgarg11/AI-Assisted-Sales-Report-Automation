import google.generativeai as genai
import streamlit as st
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


@st.cache_resource
def get_model():
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    return genai.GenerativeModel("gemini-1.5-flash")


def generate_report(df):
    model = get_model()

    data_sample = df.head(10).to_string()

    prompt = f"""
Generate a concise professional sales analytics report (max 250 words).

Dataset Sample:
{data_sample}

Include:

1. Executive Summary
2. Key Metrics
3. Trends and Patterns
4. Business Recommendations
"""

    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            return response.text

        except Exception as e:
            err = str(e)

            if "429" in err or "ResourceExhausted" in err:
                time.sleep((attempt + 1) * 10)
                continue

            return f"⚠️ Error generating report: {err}"

    return "⚠️ AI service temporarily unavailable."


def generate_pdf(report_text, filename="sales_report.pdf"):

    c = canvas.Canvas(filename, pagesize=letter)

    y = 750
    c.setFont("Helvetica", 12)

    for line in report_text.split("\n"):

        c.drawString(50, y, line)
        y -= 20

        if y < 50:
            c.showPage()
            y = 750

    c.save()

    return filename

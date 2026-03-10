import streamlit as st

from modules.data_loader import load_data
from modules.kpi_engine import generate_kpis
from modules.visualization_engine import (
    sales_by_region,
    sales_by_category,
    sales_trend
)
from modules.insight_engine import generate_insights
from modules.report_generator import generate_report, generate_pdf


st.set_page_config(
    page_title="AI Sales Intelligence Platform",
    layout="wide"
)

st.title("📊 AI Sales Intelligence Platform")

st.write(
    "Upload your sales dataset to generate KPIs, charts, insights, and an AI-powered report."
)

uploaded_file = st.file_uploader(
    "Upload Sales Dataset",
    type=["csv", "xlsx"]
)

# =========================
# DATA LOADING
# =========================

if uploaded_file:

    df = load_data(uploaded_file)

    if df is None:
        st.stop()

    st.subheader("📂 Dataset Preview")
    st.dataframe(df.head())

    # Helpful for debugging datasets
    st.write("Dataset Columns:", list(df.columns))

    # =========================
    # KPI DASHBOARD
    # =========================

    kpis = generate_kpis(df)

    st.subheader("📊 KPI Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"${kpis.get('Total Revenue',0):,.0f}")
    col2.metric("Total Orders", kpis.get("Total Orders",0))
    col3.metric(
        "Average Order Value",
        f"${kpis.get('Average Order Value',0):,.2f}"
    )

    col4, col5 = st.columns(2)

    col4.metric("Top Category", kpis.get("Top Category","N/A"))
    col5.metric("Top Region", kpis.get("Top Region","N/A"))

    # =========================
    # VISUALIZATIONS
    # =========================

    st.subheader("📊 Custom Visualization Builder")

columns = df.columns.tolist()

col1, col2, col3 = st.columns(3)

x_axis = col1.selectbox("Select X-axis", columns)
y_axis = col2.selectbox("Select Y-axis", columns)

chart_type = col3.selectbox(
    "Select Chart Type",
    ["Bar Chart", "Line Chart", "Scatter Plot"]
)

import plotly.express as px

try:

    if chart_type == "Bar Chart":

        chart = px.bar(
            df,
            x=x_axis,
            y=y_axis,
            title=f"{y_axis} by {x_axis}"
        )

    elif chart_type == "Line Chart":

        chart = px.line(
            df,
            x=x_axis,
            y=y_axis,
            title=f"{y_axis} trend"
        )

    else:

        chart = px.scatter(
            df,
            x=x_axis,
            y=y_axis,
            title=f"{x_axis} vs {y_axis}"
        )

    st.plotly_chart(chart, use_container_width=True)

except Exception as e:

    st.warning("Unable to create visualization with selected columns.")

    # =========================
    # BUSINESS INSIGHTS
    # =========================

    st.subheader("🧠 AI Business Insights")

    insights = generate_insights(df)

    if insights:
        for i in insights:
            st.write("•", i)
    else:
        st.info("No insights could be generated from this dataset.")

    # =========================
    # AI REPORT GENERATION
    # =========================

    st.subheader("🤖 AI Sales Analysis Report")

    if st.button("Generate AI Report"):

        with st.spinner("Generating AI report..."):
            report = generate_report(df)

        st.markdown(report)

        # =========================
        # PDF DOWNLOAD
        # =========================

        pdf_file = generate_pdf(report)

        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📄 Download PDF Report",
                data=f,
                file_name="sales_report.pdf",
                mime="application/pdf"
            )

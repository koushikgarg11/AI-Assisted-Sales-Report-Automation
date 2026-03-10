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

    st.subheader("📈 Visualizations")

    region_chart = sales_by_region(df)
    if region_chart:
        st.plotly_chart(region_chart, use_container_width=True)
    else:
        st.warning("Region column not found for visualization.")

    category_chart = sales_by_category(df)
    if category_chart:
        st.plotly_chart(category_chart, use_container_width=True)
    else:
        st.warning("Category column not found for visualization.")

    trend_chart = sales_trend(df)
    if trend_chart:
        st.plotly_chart(trend_chart, use_container_width=True)

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

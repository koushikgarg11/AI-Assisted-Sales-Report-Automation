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

st.write("Upload your sales dataset to generate KPIs, charts, insights, and an AI-powered report.")

uploaded_file = st.file_uploader(
    "Upload Sales Dataset",
    type=["csv", "xlsx"]
)

if uploaded_file:

    # Load Data
    df = load_data(uploaded_file)

    st.subheader("📂 Dataset Preview")
    st.dataframe(df.head())

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

    try:
        st.plotly_chart(sales_by_region(df), use_container_width=True)
    except:
        st.warning("Region column not found for visualization.")

    try:
        st.plotly_chart(sales_by_category(df), use_container_width=True)
    except:
        st.warning("Category column not found for visualization.")

    if "Order Date" in df.columns:
        try:
            st.plotly_chart(sales_trend(df), use_container_width=True)
        except:
            st.warning("Could not generate sales trend chart.")

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

        file = generate_pdf(report)

        with open(file, "rb") as f:

            st.download_button(
                label="📄 Download PDF Report",
                data=f,
                file_name="sales_report.pdf",
                mime="application/pdf"
            )

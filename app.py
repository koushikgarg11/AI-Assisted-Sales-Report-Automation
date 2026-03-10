import streamlit as st

from modules.data_loader import load_data
from modules.kpi_engine import generate_kpis
from modules.visualization_engine import (
    sales_by_region,
    sales_by_category,
    sales_trend
)
from modules.insight_engine import generate_insights
from modules.report_generator import generate_pdf

st.set_page_config(page_title="AI Sales Intelligence Platform")

st.title("📊 AI Sales Intelligence Platform")

uploaded_file = st.file_uploader(
    "Upload Sales Dataset",
    type=["csv", "xlsx"]
)

if uploaded_file:

    df = load_data(uploaded_file)

    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    # KPI Dashboard

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

    # Charts

    st.subheader("📈 Visualizations")

    st.plotly_chart(sales_by_region(df))
    st.plotly_chart(sales_by_category(df))

    if "Order Date" in df.columns:
        st.plotly_chart(sales_trend(df))

    # Insights

    st.subheader("🧠 AI Business Insights")

    insights = generate_insights(df)

    for i in insights:
        st.write("•", i)

    # Report generation

    if st.button("Generate PDF Report"):

        file = generate_pdf(kpis, insights)

        with open(file, "rb") as f:

            st.download_button(
                label="Download Sales Report",
                data=f,
                file_name="sales_report.pdf",
                mime="application/pdf"
            )

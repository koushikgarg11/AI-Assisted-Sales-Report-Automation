import streamlit as st
import pandas as pd
import plotly.express as px

from modules.data_loader import load_data
from modules.kpi_engine import generate_kpis
from modules.insight_engine import generate_insights
from modules.report_generator import generate_pdf


st.set_page_config(
    page_title="AI Sales Intelligence Platform",
    layout="wide"
)

st.title("📊 AI Sales Intelligence Platform")

st.write(
    "Upload any dataset to generate KPIs, charts, insights, chat with data, and download a report."
)

uploaded_file = st.file_uploader(
    "Upload Dataset",
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

    st.write("Dataset Columns:", list(df.columns))

    # =========================
    # KPI DASHBOARD
    # =========================

    kpis = generate_kpis(df)

    st.subheader("📊 KPI Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Revenue", f"{kpis.get('Total Revenue',0):,.2f}")
    col2.metric("Total Rows", kpis.get("Total Orders",0))
    col3.metric(
        "Average Value",
        f"{kpis.get('Average Order Value',0):,.2f}"
    )

    col4, col5 = st.columns(2)

    col4.metric("Top Category", kpis.get("Top Category","N/A"))
    col5.metric("Top Region", kpis.get("Top Region","N/A"))

    # =========================
    # CUSTOM VISUALIZATION BUILDER
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

    except:

        st.warning("Unable to create visualization with selected columns.")

    # =========================
    # BUSINESS INSIGHTS
    # =========================

    st.subheader("🧠 Data Insights")

    insights = generate_insights(df)

    if insights:
        for i in insights:
            st.write("•", i)
    else:
        st.info("No insights generated.")

    # =========================
    # CHAT WITH DATA
    # =========================

    st.subheader("💬 Chat With Your Data")

    question = st.text_input("Ask a question about your dataset")

    if question:

        try:

            numeric_cols = df.select_dtypes(include="number").columns
            cat_cols = df.select_dtypes(include="object").columns

            if "total" in question.lower():

                col = numeric_cols[0]
                answer = df[col].sum()

                st.write(f"Total {col}: {answer:,.2f}")

            elif "average" in question.lower():

                col = numeric_cols[0]
                answer = df[col].mean()

                st.write(f"Average {col}: {answer:,.2f}")

            elif "highest" in question.lower():

                num = numeric_cols[0]
                cat = cat_cols[0]

                result = df.groupby(cat)[num].sum().idxmax()

                st.write(f"{result} has the highest {num}")

            else:

                st.write("Try asking about total, average, or highest values.")

        except:

            st.write("Unable to analyze this question.")

    # =========================
    # REPORT GENERATION (NO API)
    # =========================

    st.subheader("📄 Generate Analysis Report")

    if st.button("Generate Report"):

        numeric_cols = df.select_dtypes(include="number").columns

        report = "## Dataset Analysis Report\n\n"

        report += f"Total Rows: {len(df)}\n\n"
        report += f"Total Columns: {len(df.columns)}\n\n"

        if len(numeric_cols) > 0:

            col = numeric_cols[0]

            report += f"Total {col}: {df[col].sum():,.2f}\n\n"
            report += f"Average {col}: {df[col].mean():,.2f}\n\n"

        report += "### Key Insights\n"

        for i in insights:
            report += f"- {i}\n"

        st.markdown(report)

        pdf_file = generate_pdf(report)

        with open(pdf_file, "rb") as f:

            st.download_button(
                label="📄 Download PDF Report",
                data=f,
                file_name="analysis_report.pdf",
                mime="application/pdf"
            )

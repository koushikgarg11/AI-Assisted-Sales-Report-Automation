import streamlit as st

from modules.data_loader import load_dataset
from modules.etl_pipeline import clean_data
from modules.auto_analysis import detect_columns
from modules.charts_engine import generate_chart
from modules.semantic_search import search_dataframe
from modules.ai_engine import generate_ai_summary
from modules.report_generator import generate_report

st.title("SalesLens AI - Smart Data Analyzer")

uploaded_file = st.file_uploader("Upload Dataset")

if uploaded_file:

    df = load_dataset(uploaded_file)

    df = clean_data(df)

    st.subheader("Dataset Preview")

    st.dataframe(df.head())

    numeric_cols, cat_cols = detect_columns(df)

    st.write("Numeric Columns:", numeric_cols)
    st.write("Categorical Columns:", cat_cols)

    if numeric_cols and cat_cols:

        x = st.selectbox("Category", cat_cols)
        y = st.selectbox("Metric", numeric_cols)

        chart_type = st.selectbox(
            "Chart Type",
            ["bar","line","scatter","box","histogram","pie"]
        )

        fig = generate_chart(df, x, y, chart_type)

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("AI Dataset Insights")

    if st.button("Generate AI Insights"):

        insights = generate_ai_summary(df)

        st.write(insights)

    st.subheader("Semantic Search")

    query = st.text_input("Search your dataset")

    if query:

        results = search_dataframe(df, query)

        st.dataframe(results)

    st.subheader("Generate AI Report")

    if st.button("Create Report"):

        report = generate_report(df)

        st.download_button(
            "Download Report",
            report,
            file_name="saleslens_report.txt"
        )

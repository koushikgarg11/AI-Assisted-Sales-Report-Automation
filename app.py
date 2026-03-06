import streamlit as st
from modules.data_loader import load_dataset
from modules.etl_pipeline import clean_data
from modules.auto_analysis import detect_columns
from modules.charts_engine import generate_chart
from modules.semantic_search import search_dataframe
from modules.ai_engine import generate_ai_summary
from modules.report_generator import generate_report

st.set_page_config(page_title="SalesLens AI", layout="wide")
st.title("SalesLens AI — Smart Data Analyzer")

# ── SIDEBAR ───────────────────────────────────
with st.sidebar:
    st.markdown("### 📋 Pipeline")
    st.markdown("01 · Upload CSV\n\n02 · ETL clean\n\n03 · Visualize\n\n04 · AI Insights\n\n05 · Semantic Search\n\n06 · Report")
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("Upload any sales CSV and get AI-powered insights, semantic search, and a generated report — no API key needed.")

# ── DATA UPLOAD ───────────────────────────────
uploaded_file = st.file_uploader("Upload Dataset (.csv)", type=["csv"])

if uploaded_file:
    df = load_dataset(uploaded_file)
    df = clean_data(df)

    st.subheader("Dataset Preview")
    st.dataframe(df.head(), use_container_width=True)

    numeric_cols, cat_cols = detect_columns(df)
    col1, col2 = st.columns(2)
    col1.write(f"**Numeric columns:** {', '.join(numeric_cols) if numeric_cols else '—'}")
    col2.write(f"**Categorical columns:** {', '.join(cat_cols) if cat_cols else '—'}")

    # ── CHARTS ───────────────────────────────
    if numeric_cols and cat_cols:
        st.subheader("Visualize Data")
        c1, c2, c3 = st.columns(3)
        x = c1.selectbox("Category (X)", cat_cols)
        y = c2.selectbox("Metric (Y)", numeric_cols)
        chart_type = c3.selectbox("Chart Type", ["bar", "line", "scatter", "box", "histogram", "pie"])
        fig = generate_chart(df, x, y, chart_type)
        st.plotly_chart(fig, use_container_width=True)

    # ── AI INSIGHTS ───────────────────────────
    st.subheader("AI Dataset Insights")
    if st.button("✦ Generate AI Insights"):
        with st.spinner("Analyzing with Gemini..."):
            insights = generate_ai_summary(df)
        st.write(insights)

    # ── SEMANTIC SEARCH ───────────────────────
    st.subheader("Semantic Search")
    st.caption("Ask anything in plain English — e.g. 'highest revenue customers' or 'refunded orders in Europe'")

    col_q, col_k = st.columns([3, 1])
    query = col_q.text_input("Search your dataset", placeholder="e.g. top performing products last quarter")
    top_k = col_k.slider("Results", min_value=1, max_value=20, value=5)

    if query:
        with st.spinner("Searching..."):
            output = search_dataframe(df, query, top_k=top_k, threshold=0.25)

        if output["no_results"]:
            st.info("No results matched your query. Try rephrasing.")
        else:
            results = output["results"]
            st.success(f"Found {len(results)} result(s)")
            results["_similarity_score"] = results["_similarity_score"].apply(lambda x: f"{x:.0%}")
            results = results.rename(columns={"_similarity_score": "Match %"})
            st.dataframe(results, use_container_width=True)

    # ── REPORT ────────────────────────────────
    st.subheader("Generate AI Report")
    if st.button("📋 Create Report"):
        with st.spinner("Generating report..."):
            report = generate_report(df)
        st.download_button(
            "⬇ Download Report",
            report,
            file_name="saleslens_report.txt",
            mime="text/plain"
        )

else:
    st.info("⬆ Upload a CSV file to get started.")

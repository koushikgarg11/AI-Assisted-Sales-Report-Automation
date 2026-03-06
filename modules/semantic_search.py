import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ─────────────────────────────────────────────
# MODEL LOADING
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading semantic search model...")
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


# ─────────────────────────────────────────────
# ROW TEXT BUILDER
# Better than raw join — adds column names for context
# e.g. "customer: Acme Corp  region: North America  total: 1200.0"
# ─────────────────────────────────────────────
def build_row_texts(df):
    rows = []
    for _, row in df.iterrows():
        parts = [f"{col}: {val}" for col, val in row.items()]
        rows.append("  ".join(parts))
    return rows


# ─────────────────────────────────────────────
# CACHE EMBEDDINGS PER DATAFRAME
# Avoids re-encoding on every search
# ─────────────────────────────────────────────
@st.cache_data(show_spinner="Indexing dataset...")
def compute_embeddings(df_hash: str, row_texts: tuple):
    model = load_model()
    return model.encode(list(row_texts), show_progress_bar=False)


# ─────────────────────────────────────────────
# MAIN SEARCH FUNCTION
# ─────────────────────────────────────────────
def search_dataframe(df, query: str, top_k: int = 5, threshold: float = 0.25):
    """
    Semantic search over a dataframe using sentence embeddings.

    Args:
        df       : pandas DataFrame to search
        query    : plain-English search string
        top_k    : number of results to return (default 5)
        threshold: minimum similarity score to include a result (0–1)

    Returns:
        dict with keys:
            'results'    : filtered DataFrame of top matches
            'scores'     : similarity scores for each result
            'no_results' : True if nothing passed threshold
    """
    if df is None or df.empty:
        return {"results": df, "scores": [], "no_results": True}

    if not query or not query.strip():
        return {"results": df.head(top_k), "scores": [], "no_results": False}

    model = load_model()

    # Build enriched row texts with column names as context
    row_texts = build_row_texts(df)

    # Use a hash of the dataframe shape + columns as cache key
    df_hash = f"{df.shape}_{list(df.columns)}_{df.iloc[0].to_json()}"
    embeddings = compute_embeddings(df_hash, tuple(row_texts))

    # Encode query
    query_embedding = model.encode([query.strip()], show_progress_bar=False)

    # Compute cosine similarity
    scores = cosine_similarity(query_embedding, embeddings)[0]

    # Get top_k indices sorted by score descending
    top_indices = scores.argsort()[::-1][:top_k]
    top_scores = scores[top_indices]

    # Filter by threshold
    mask = top_scores >= threshold
    filtered_indices = top_indices[mask]
    filtered_scores = top_scores[mask]

    if len(filtered_indices) == 0:
        return {"results": df.iloc[[]], "scores": [], "no_results": True}

    result_df = df.iloc[filtered_indices].copy()
    result_df["_similarity_score"] = np.round(filtered_scores, 3)

    # Sort by score descending
    result_df = result_df.sort_values("_similarity_score", ascending=False)

    return {
        "results": result_df,
        "scores": filtered_scores.tolist(),
        "no_results": False
    }

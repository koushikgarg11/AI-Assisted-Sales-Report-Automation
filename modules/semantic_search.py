import streamlit as st
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

def search_dataframe(df, query):

    text_data = df.astype(str).agg(" ".join, axis=1)

    embeddings = model.encode(text_data.tolist())
    query_embedding = model.encode([query])

    similarity = cosine_similarity(query_embedding, embeddings)[0]

    top_indices = similarity.argsort()[-5:][::-1]

    return df.iloc[top_indices]

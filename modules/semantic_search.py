from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def search_dataframe(df, query):

    text_rows = df.astype(str).apply(" ".join, axis=1)

    embeddings = model.encode(text_rows.tolist())

    query_embedding = model.encode([query])

    similarity = cosine_similarity(query_embedding, embeddings)[0]

    top_idx = similarity.argsort()[-5:][::-1]

    return df.iloc[top_idx]

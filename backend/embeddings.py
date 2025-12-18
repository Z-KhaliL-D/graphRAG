import faiss
import numpy as np
import pickle
from llm_agent import ask_gemini

EMBEDDING_SIZE = 768  

graph_nodes = [
    {"id": 1, "text": "Multi-Agent AI with LangGraph, 2025"},
    {"id": 2, "text": "Alice collaborated with Bob"},
]


index = faiss.IndexFlatL2(EMBEDDING_SIZE)


def embed_text(text: str):
    """
    TEMPORARY – returns random embedding.
    Replace with real LLM embeddings later.
    """
    return np.random.rand(EMBEDDING_SIZE).astype("float32")


def build_vector_store():
    embeddings = []

    for node in graph_nodes:
        emb = embed_text(node["text"])
        embeddings.append(emb)

    embeddings_np = np.array(embeddings)
    index.add(embeddings_np)

    faiss.write_index(index, "vector.index")
    with open("nodes.pkl", "wb") as f:
        pickle.dump(graph_nodes, f)

    print("Vector store built successfully.")


def load_vector_store():
    idx = faiss.read_index("vector.index")
    with open("nodes.pkl", "rb") as f:
        nodes = pickle.load(f)
    return idx, nodes


def search_similar(query: str, top_k=3):
    idx, nodes = load_vector_store()

    query_emb = embed_text(query)
    D, I = idx.search(np.array([query_emb]), top_k)

    results = []
    for i in I[0]:
        results.append(nodes[i])

    return results

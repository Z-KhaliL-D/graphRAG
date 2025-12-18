from neo4j_connect import retrieve_nodes_by_cypher, get_all_nodes
import numpy as np
import faiss
from llm_agent import get_embedding

graph_nodes = []
embeddings = []
faiss_index = None

def build_faiss_index(nodes):
    global graph_nodes, embeddings, faiss_index
    graph_nodes = nodes
    embeddings = []
    for node in nodes:
        node_text = " | ".join([f"{k}: {v}" for k, v in node.items()])
        emb = get_embedding(node_text)
        embeddings.append(np.array(emb, dtype="float32"))
    embeddings_np = np.array(embeddings)
    faiss_index = faiss.IndexFlatL2(embeddings_np.shape[1])
    faiss_index.add(embeddings_np)

def retrieve_vector(query, top_k=3):
    global faiss_index
    if faiss_index is None or len(graph_nodes) == 0:
        return []
    query_emb = np.array(get_embedding(query), dtype="float32")
    D, I = faiss_index.search(np.array([query_emb]), top_k)
    return [graph_nodes[i] for i in I[0]]

def hybrid_retrieve(query, top_k=3):
    cypher_nodes = retrieve_nodes_by_cypher(query, top_k)
    vector_nodes = retrieve_vector(query, top_k)
    all_nodes = {n.get("name") or n.get("title"): n for n in cypher_nodes}
    for n in vector_nodes:
        key = n.get("name") or n.get("title")
        if key:
            all_nodes[key] = n
    return list(all_nodes.values())

nodes = get_all_nodes()
build_faiss_index(nodes)

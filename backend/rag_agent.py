from embeddings import search_similar
from llm_agent import ask_gemini

def rag_answer(query: str):
    retrieved_nodes = search_similar(query)

    context = " | ".join([n["text"] for n in retrieved_nodes])

    prompt = f"""
Use the following context to answer the query.

CONTEXT:
{context}

QUERY:
{query}

ANSWER:
"""

    return ask_gemini(prompt)

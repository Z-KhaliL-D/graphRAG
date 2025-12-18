from llm_agent import ask_gemini
from tools import get_papers_by_topic, get_collaborators
from graph_rag import hybrid_retrieve

def agent(query):
    """
    Multi-step agent workflow:
    - Uses tools for structured queries (papers, collaborators)
    - Uses hybrid GraphRAG (Cypher + vector search) for unstructured queries
    - Sends context to LLM for reasoning and final answer
    """
    query_lower = query.lower()
    
    if "papers on" in query_lower:
        topic = query_lower.split("papers on")[-1].strip()
        papers = get_papers_by_topic(topic)
        context = f"Papers on {topic}: {papers}"
        answer = ask_gemini(f"Summarize these papers and highlight key details: {context}")
        return answer

    elif "collaborators of" in query_lower:
        researcher = query_lower.split("collaborators of")[-1].strip()
        collaborators = get_collaborators(researcher)
        context = f"{researcher}'s collaborators: {collaborators}"
        answer = ask_gemini(f"Describe these collaborators and their research areas: {context}")
        return answer

    else:
        retrieved_nodes = hybrid_retrieve(query, top_k=3)
        if retrieved_nodes:
            context_text = " | ".join([str(n) for n in retrieved_nodes])
            answer = ask_gemini(f"Using this context: {context_text}, answer the query: {query}")
        else:
            answer = ask_gemini(f"Answer this research query: {query}")
        return answer

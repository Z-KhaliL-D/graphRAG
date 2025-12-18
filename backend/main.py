from fastapi import FastAPI, Query
from agent import agent
from rag_agent import rag_answer
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/ask")
def ask(query: str = Query(..., description="Your query to the agent")):
    answer = agent(query)
    return {"query": query, "answer": answer}

@app.get("/graph-info")
def graph_info():
    return {
        "nodes": ["Researcher", "Paper", "Institution", "Tool", "Topic"],
        "relationships": ["AUTHORED", "AFFILIATED_WITH", "USES_TOOL", "HAS_TOPIC", "COLLABORATES_WITH"]
    }
@app.post("/rag")
def rag(query: dict):
    """
    Process a query using hybrid GraphRAG retrieval + LLM.
    Expects JSON: {"query": "Your question here"}
    """
    user_query = query.get("query", "")
    if not user_query:
        return {"error": "Query missing"}
    
    answer = agent(user_query)
    return {"query": user_query, "response": answer}
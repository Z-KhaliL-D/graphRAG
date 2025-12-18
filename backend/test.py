import requests
from neo4j import GraphDatabase

BACKEND_URL = "http://127.0.0.1:8000/rag"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "mypass123" 

def test_backend():
    print("\n=== TEST 1 — Backend /rag endpoint ===")

    try:
        res = requests.post(BACKEND_URL, json={"query": "hello"}, timeout=10)
        print("Status code:", res.status_code)
        print("Response:", res.text[:500])
    except Exception as e:
        print("FAILED: Backend not reachable")
        print("Error:", e)

# ================================
# TEST 2 — Neo4j connection
# ================================
def test_neo4j():
    print("\n=== TEST 2 — Neo4j connectivity ===")

    try:
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        with driver.session() as session:
            result = session.run("MATCH (n) RETURN count(n) as c")
            count = result.single()["c"]
            print("Connected to Neo4j successfully.")
            print("Node count:", count)
    except Exception as e:
        print("FAILED: Neo4j not reachable")
        print("Error:", e)

# ================================
# TEST 3 — End-to-end Graph RAG query
# ================================
def test_graph_rag():
    print("\n=== TEST 3 — Full GraphRAG query ===")

    query = "Who are the researchers connected to Alice?"

    try:
        res = requests.post(BACKEND_URL, json={"query": query}, timeout=15)
        print("Status:", res.status_code)
        print("Output:", res.text[:1000])
    except Exception as e:
        print("FAILED: Full pipeline test failed")
        print("Error:", e)

# ================================
# RUN EVERYTHING
# ================================
if __name__ == "__main__":
    print("=====================================")
    print("    GRAPH-RAG SYSTEM TEST SUITE")
    print("=====================================")

    test_backend()
    test_neo4j()
    test_graph_rag()

    print("\n=== TESTING COMPLETE ===")

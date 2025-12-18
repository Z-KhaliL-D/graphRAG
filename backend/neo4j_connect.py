from neo4j import GraphDatabase

uri = "neo4j://127.0.0.1:7687"
user = "neo4j"
password = "mypass123"  
driver = GraphDatabase.driver(uri, auth=(user, password))

def run_cypher(query, parameters=None):
    with driver.session(database="neo4j") as session:
        result = session.run(query, parameters or {})
        return [record.data() for record in result]

def retrieve_nodes_by_cypher(keyword, top_k=3):
    """
    Return top_k nodes that match keyword using Neo4j full-text or property search.
    """
    query = """
    MATCH (n)
    WHERE toLower(n.name) CONTAINS toLower($keyword) 
       OR toLower(n.title) CONTAINS toLower($keyword)
    RETURN n
    LIMIT $top_k
    """
    results = run_cypher(query, {"keyword": keyword, "top_k": top_k})
    return [dict(record["n"]) for record in results]

def get_all_nodes():
    query = "MATCH (n) RETURN n LIMIT 100"
    results = run_cypher(query)
    nodes = [dict(record["n"]) for record in results]
    return nodes

if __name__ == "__main__":
    print("Sample nodes:", run_cypher("MATCH (n) RETURN n LIMIT 5"))

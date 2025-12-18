from neo4j_connect import run_cypher

def get_papers_by_topic(topic_name):
    query = """
    MATCH (p:Paper)-[:HAS_TOPIC]->(t:Topic)
    WHERE toLower(t.name) = toLower($topic)
    RETURN p.title AS title, p.year AS year
    """
    return run_cypher(query, {"topic": topic_name})

def get_collaborators(researcher_name):
    query = """
    MATCH (r:Researcher)-[:COLLABORATES_WITH]->(c:Researcher)
    WHERE toLower(r.name) = toLower($name)
    RETURN c.name AS collaborator
    """
    return run_cypher(query, {"name": researcher_name})

from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "your_password"

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)



query = """
MERGE (a:Account {account_id:$sender})
MERGE (b:Account {account_id:$receiver})

CREATE (a)-[:TRANSFERRED_TO {
    transaction_id:$transaction_id,
    amount:$amount,
    timestamp:$timestamp
}]->(b)
"""
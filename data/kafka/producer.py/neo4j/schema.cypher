MATCH (a:Account {account_id:'ACC001'})
CREATE (b:Account {account_id:'ACC002'})
CREATE (a)-[:TRANSFERRED_TO {
    transaction_id:'TX00001',
    amount:5000
}]->(b);
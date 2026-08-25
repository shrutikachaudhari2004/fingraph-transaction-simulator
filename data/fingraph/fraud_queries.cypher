// DAY 5 - Circular Money Flow

MATCH (a:Account)-[:TRANSFERRED_TO]->(b:Account)
      -[:TRANSFERRED_TO]->(c:Account)
      -[:TRANSFERRED_TO]->(a)
RETURN 
    a.account_id AS Account_A,
    b.account_id AS Account_B,
    c.account_id AS Account_C;


// DAY 5 - High Amount Transactions

MATCH (a:Account)-[t:TRANSFERRED_TO]->(b:Account)
WHERE t.amount > 10000
RETURN 
    a.account_id AS Sender,
    b.account_id AS Receiver,
    t.amount AS Amount,
    t.transaction_id AS Transaction_ID
ORDER BY t.amount DESC;


// DAY 5 - Highly Connected Accounts

MATCH (a:Account)-[t:TRANSFERRED_TO]->()
RETURN 
    a.account_id AS Account,
    count(t) AS transaction_count
ORDER BY transaction_count DESC;
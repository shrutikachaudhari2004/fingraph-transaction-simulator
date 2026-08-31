MATCH (a:Account)-[t:TRANSFERRED_TO]->(b:Account)
WHERE t.amount > 10000
RETURN a.account_id,
       b.account_id,
       t.amount
ORDER BY t.amount DESC;



// STEP 12 - Circular Money Flow Detection

MATCH (a:Account)-[:TRANSFERRED_TO]->(b:Account)
      -[:TRANSFERRED_TO]->(c:Account)
      -[:TRANSFERRED_TO]->(a)
RETURN a.account_id AS Account_A,
       b.account_id AS Account_B,
       c.account_id AS Account_C;
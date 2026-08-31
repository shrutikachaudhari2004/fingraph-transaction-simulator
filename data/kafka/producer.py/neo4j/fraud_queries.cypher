MATCH (a:Account)-[t:TRANSFERRED_TO]->(b:Account)
WHERE t.amount > 10000
RETURN a.account_id,
       b.account_id,
       t.amount
ORDER BY t.amount DESC;
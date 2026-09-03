import random
import csv
from datetime import datetime

accounts = [f"ACC{i:03d}" for i in range(1, 101)]

with open("data/transactions.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "transaction_id",
        "sender",
        "receiver",
        "amount",
        "timestamp"
    ])

    for i in range(1, 1001):

        sender = random.choice(accounts)
        receiver = random.choice(accounts)

        while receiver == sender:
            receiver = random.choice(accounts)

        amount = random.randint(500, 20000)

        writer.writerow([
            f"TX{i:05d}",
            sender,
            receiver,
            amount,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

print("1000 transactions generated successfully!")


import pandas as pd
import random
from datetime import datetime, timedelta

records = []

for i in range(10000):
    sender = f"ACC{random.randint(100, 999)}"
    receiver = f"ACC{random.randint(100, 999)}"
    
    while receiver == sender:
        receiver = f"ACC{random.randint(100, 999)}"

    amount = random.randint(100, 20000)

    if amount > 15000:
        risk = "HIGH"
    elif amount > 8000:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    is_fraud = 1 if risk == "HIGH" and random.random() < 0.5 else 0

    records.append({
        "transaction_id": f"TX{i+1:05d}",
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "timestamp": datetime.now() - timedelta(minutes=i),
        "risk": risk,
        "isFraud": is_fraud
    })

df = pd.DataFrame(records)

df.to_csv("transaction.csv", index=False)

print("✅ 10,000 transactions generated successfully!")
print(df.head())
print("Total records:", len(df))
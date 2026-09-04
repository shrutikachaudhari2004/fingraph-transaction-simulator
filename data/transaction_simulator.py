import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

records = []

for i in range(10000):

    sender = f"ACC{random.randint(100, 999)}"
    receiver = f"ACC{random.randint(100, 999)}"

    while sender == receiver:
        receiver = f"ACC{random.randint(100, 999)}"

    amount = random.randint(100, 20000)

    if amount > 15000:
        risk = "HIGH"
    elif amount > 8000:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    isFraud = 1 if risk == "HIGH" and random.random() < 0.5 else 0

    records.append({
        "transaction_id": f"TX{i+1:05d}",
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "timestamp": datetime.now() - timedelta(minutes=i),
        "risk": risk,
        "isFraud": isFraud
    })

df = pd.DataFrame(records)

# Save directly inside data folder
file_path = Path("data") / "transaction.csv"

df.to_csv(file_path, index=False)

print("✅ 10,000 transactions created!")
print("✅ File saved at:", file_path)
print("✅ Total records:", len(df))
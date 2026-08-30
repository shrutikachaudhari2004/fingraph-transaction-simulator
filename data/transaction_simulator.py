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
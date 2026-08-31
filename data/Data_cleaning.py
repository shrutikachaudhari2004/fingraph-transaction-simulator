import pandas as pd

data = {
    "transaction_id": ["TX001", "TX002", "TX003", "TX004"],
    "sender": ["ACC001", "", "ACC003", "ACC004"],
    "receiver": ["ACC002", "ACC003", "", "ACC005"],
    "amount": [5000, 2000, -100, 7000]
}

df = pd.DataFrame(data)

print("Original Data:")
print(df)

# Remove missing sender
df = df[df["sender"].notna() & (df["sender"] != "")]

# Remove missing receiver
df = df[df["receiver"].notna() & (df["receiver"] != "")]

# Keep only positive amount
df = df[df["amount"] > 0]

# Remove duplicate transactions
df = df.drop_duplicates(subset=["transaction_id"])

print("\nClean Data:")
print(df)
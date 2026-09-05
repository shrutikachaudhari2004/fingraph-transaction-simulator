import pandas as pd

df = pd.read_csv("data/transaction.csv")

high_value = df[df["amount"] > 10000]

print(high_value[
    ["transaction_id", "sender", "receiver", "amount"]
].sort_values("amount", ascending=False))


import pandas as pd
import networkx as nx

# Load 1000 transactions
df = pd.read_csv("data/transaction.csv")

print("Total Transaction:", len(df))


# ==========================================
# STEP 11 - HIGH AMOUNT FRAUD
# ==========================================

high_value = df[df["amount"] > 10000]

print("\n===== HIGH VALUE TRANSACTION =====")

print(
    high_value[
        [
            "transaction_id",
            "sender",
            "receiver",
            "amount"
        ]
    ]
    .sort_values(
        "amount",
        ascending=False
    )
    .to_string(index=False)
)

print(
    "\nTotal High Value Transaction:",
    len(high_value)
)


# ==========================================
# STEP 12 - CIRCULAR MONEY FLOW
# ==========================================

G = nx.DiGraph()

# Create transaction graph
for _, row in df.iterrows():

    sender = str(row["sender"])
    receiver = str(row["receiver"])

    G.add_edge(
        sender,
        receiver
    )


# Find circular flows
cycles = list(nx.simple_cycles(G))


print("\n===== CIRCULAR MONEY FLOWS =====")

if len(cycles) == 0:

    print("No circular money flow found.")

else:

    print(
        "Total Circular Patterns:",
        len(cycles)
    )

    for i, cycle in enumerate(cycles, start=1):

        # Close the cycle
        closed_cycle = cycle + [cycle[0]]

        print(
            f"{i}. " +
            " → ".join(closed_cycle)
        )



        # ==========================================
# STEP 13 - RISK SCORE
# ==========================================

def calculate_risk(amount):

    if amount > 15000:
        return 90

    elif amount > 10000:
        return 70

    elif amount > 5000:
        return 40

    else:
        return 10


def get_risk_level(score):

    if score <= 30:
        return "LOW"

    elif score <= 60:
        return "MEDIUM"

    else:
        return "HIGH"


# Calculate risk score for all transactions
df["risk_score"] = df["amount"].apply(calculate_risk)

# Calculate risk level
df["risk"] = df["risk_score"].apply(get_risk_level)


print("\n===== RISK ANALYSIS =====")

print(
    df[
        [
            "transaction_id",
            "sender",
            "receiver",
            "amount",
            "risk_score",
            "risk"
        ]
    ].head(20).to_string(index=False)
)


# Risk summary
print("\n===== RISK SUMMARY =====")

print(
    df["risk"].value_counts()
)


# Save result
df.to_csv(
    "data/fraud_transaction.csv",
    index=False
)

print("\nRisk analysis completed successfully!")
print("Saved file: data/fraud_transaction.csv")





import pandas as pd

# Load transaction data
df = pd.read_csv("data/transactions.csv")

# Make sure amount is numeric
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

print("Total Transactions:", len(df))

# High-value transactions
high_value = df[df["amount"] > 10000]

print("\n===== HIGH VALUE TRANSACTIONS =====")

print(
    high_value[
        [
            "transaction_id",
            "sender",
            "receiver",
            "amount"
        ]
    ]
    .sort_values("amount", ascending=False)
    .to_string(index=False)
)

print("\nTotal High Value Transactions:", len(high_value))





import pandas as pd
import networkx as nx

# Load transaction data
df = pd.read_csv("data/transactions.csv")

# Convert account IDs to strings
df["sender"] = df["sender"].astype(str)
df["receiver"] = df["receiver"].astype(str)

# Create directed graph
G = nx.DiGraph()

# Add transactions to graph
for _, row in df.iterrows():
    G.add_edge(
        row["sender"],
        row["receiver"]
    )

print("\n===== CIRCULAR MONEY FLOW DETECTION =====")

# Store detected cycles
cycles = set()

# Check for 3-account circular transactions
for a in G.nodes():

    for b in G.successors(a):

        if b == a:
            continue

        for c in G.successors(b):

            if c == a or c == b:
                continue

            # Check C → A
            if G.has_edge(c, a):

                # Remove duplicate rotations
                cycle = tuple(sorted([a, b, c]))
                cycles.add(cycle)


# Display results
if len(cycles) == 0:

    print("No 3-account circular transaction found.")

else:

    print("Circular transactions found:")

    for cycle in sorted(cycles):

        a, b, c = cycle

        print(f"{a} → {b} → {c} → {a}")

    print("\nTotal Circular Transactions:", len(cycles))
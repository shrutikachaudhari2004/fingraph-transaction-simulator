from pyflink.datastream import StreamExecutionEnvironment

env = StreamExecutionEnvironment.get_execution_environment()

data = env.from_collection([
    "Transaction 1",
    "Transaction 2",
    "Transaction 3",
    "Transaction 4"
])

data.print()




env.execute("Fingraph Flink Test")



transaction = {
    "transaction_id": "TX00002",
    "sender": "",
    "receiver": "ACC002",
    "amount": 5000
}




transaction = {
    "transaction_id": "TX00003",
    "sender": "ACC001",
    "receiver": "ACC002",
    "amount": -500
}





seen_transactions = set()


def clean_transaction(data):

    # Sender validation
    if not data.get("sender"):
        return None

    # Receiver validation
    if not data.get("receiver"):
        return None

    # Amount validation
    try:
        amount = float(data.get("amount", 0))
    except (ValueError, TypeError):
        return None

    if amount <= 0:
        return None

    # Duplicate validation
    transaction_id = data.get("transaction_id")

    if transaction_id in seen_transactions:
        return None

    seen_transactions.add(transaction_id)

    data["amount"] = amount

    return data


# Test
transactions = [
    {
        "transaction_id": "TX00001",
        "sender": "ACC001",
        "receiver": "ACC002",
        "amount": 5000
    },
    {
        "transaction_id": "TX00001",
        "sender": "ACC001",
        "receiver": "ACC002",
        "amount": 5000
    }
]

for transaction in transactions:

    result = clean_transaction(transaction)

    if result:
        print("CLEAN:", result)
    else:
        print("REJECTED:", transaction)
        
def clean_transaction(data):

    # 1. Sender check
    if not data.get("sender"):
        return None

    # 2. Receiver check
    if not data.get("receiver"):
        return None

    # 3. Amount check
    try:
        amount = float(data.get("amount", 0))
    except (ValueError, TypeError):
        return None

    if amount <= 0:
        return None

    # 4. Update amount as number
    data["amount"] = amount

    return data


# Test transaction
transaction = {
    "transaction_id": "TX00001",
    "sender": "ACC001",
    "receiver": "ACC002",
    "amount": 5000
}

cleaned = clean_transaction(transaction)

if cleaned:
    print("Clean transaction:")
    print(cleaned)
else:
    print("Invalid transaction")
    
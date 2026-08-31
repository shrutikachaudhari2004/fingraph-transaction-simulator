def calculate_risk(amount):

    if amount > 15000:
        return 90

    elif amount > 10000:
        return 70

    elif amount > 5000:
        return 40

    else:
        return 10



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


if _name_ == "_main_":

    amount = float(input("Enter transaction amount: "))

    score = calculate_risk(amount)
    level = get_risk_level(score)

    print("Amount:", amount)
    print("Risk Score:", score)
    print("Risk Level:", level)
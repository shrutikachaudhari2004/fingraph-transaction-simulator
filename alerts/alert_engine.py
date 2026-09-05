def check_alert(account, risk_score):

    threshold = 70

    if risk_score > threshold:
        print("🚨 FRAUD ALERT")
        print("Account:", account)
        print("Risk Score:", risk_score)
        print("Action: Investigate immediately")

    else:
        print("✅ No Fraud Alert")
        print("Account:", account)
        print("Risk Score:", risk_score)


check_alert("ACC101", 87)
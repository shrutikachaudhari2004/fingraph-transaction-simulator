import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="FinGraph Fraud Detection",
    layout="wide"
)

# Dashboard title
st.title("🔍 FinGraph Fraud Detection Dashboard")

# Load CSV file
csv_path = "../../../transaction.csv"

try:
    df = pd.read_csv(csv_path)

    st.success("✅ Transaction data loaded successfully!")

    # Total transactions
    total_transactions = len(df)

    # Risk calculation
    if "risk" not in df.columns:

        if "amount" in df.columns:
            df["risk"] = df["amount"].apply(
                lambda x: "HIGH" if x > 10000
                else "MEDIUM" if x > 5000
                else "LOW"
            )
        else:
            df["risk"] = "LOW"

    # KPI calculations
    high_risk = (df["risk"] == "HIGH").sum()
    medium_risk = (df["risk"] == "MEDIUM").sum()

    # Suspicious accounts
    if "sender" in df.columns and "risk" in df.columns:
        suspicious_accounts = df[df["risk"] == "HIGH"]["sender"].nunique()
    else:
        suspicious_accounts = 0

    # Display KPIs
    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Transactions",
        total_transactions
    )

    col2.metric(
        "🔴 High Risk",
        high_risk
    )

    col3.metric(
        "🟠 Medium Risk",
        medium_risk
    )

    col4.metric(
        "⚠️ Suspicious Accounts",
        suspicious_accounts
    )

    # Risk distribution
    st.subheader("📊 Risk Distribution")

    risk_count = df["risk"].value_counts()

    st.bar_chart(risk_count)

    # Transaction data
    st.subheader("📋 Transaction Data")

    st.dataframe(
        df,
        use_container_width=True
    )

except Exception as e:
    st.error(f"❌ Error: {e}")
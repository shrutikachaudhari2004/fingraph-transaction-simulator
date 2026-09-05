import streamlit as st
import pandas as pd
import os




# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="FinGraph Fraud Dashboard",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 FinGraph Fraud Detection Dashboard")

# -----------------------------
# Load Transaction CSV
# -----------------------------

csv_path = "../../../transaction.csv"

if not os.path.exists(csv_path):
    st.error("❌ transaction.csv file not found!")
    st.stop()

df = pd.read_csv(csv_path)

# -----------------------------
# Clean Column Names
# -----------------------------

df.columns = df.columns.str.strip()

# -----------------------------
# Total Transactions
# -----------------------------

total_transactions = len(df)

# -----------------------------
# Risk Calculation
# -----------------------------

if "risk" in df.columns:

    high_risk = (df["risk"].astype(str).str.upper() == "HIGH").sum()

    medium_risk = (df["risk"].astype(str).str.upper() == "MEDIUM").sum()

    low_risk = (df["risk"].astype(str).str.upper() == "LOW").sum()

else:

    # If risk column is not available,
    # calculate risk using amount

    if "amount" in df.columns:

        df["amount"] = pd.to_numeric(
            df["amount"],
            errors="coerce"
        ).fillna(0)

        df["risk"] = "LOW"

        df.loc[df["amount"] > 5000, "risk"] = "MEDIUM"

        df.loc[df["amount"] > 10000, "risk"] = "HIGH"

        high_risk = (df["risk"] == "HIGH").sum()

        medium_risk = (df["risk"] == "MEDIUM").sum()

        low_risk = (df["risk"] == "LOW").sum()

    else:

        high_risk = 0
        medium_risk = 0
        low_risk = 0


# -----------------------------
# Suspicious Accounts
# -----------------------------

suspicious_accounts = 28


# -----------------------------
# KPI Dashboard
# -----------------------------

st.subheader("📊 Dashboard KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Transactions",
        total_transactions
    )

with col2:
    st.metric(
        "High Risk",
        high_risk
    )

with col3:
    st.metric(
        "Medium Risk",
        medium_risk
    )

with col4:
    st.metric(
        "Suspicious Accounts",
        suspicious_accounts
    )


# -----------------------------
# Risk Distribution
# -----------------------------

st.subheader("🚨 Risk Distribution")

risk_counts = df["risk"].value_counts()

st.bar_chart(risk_counts)


# -----------------------------
# Transaction Data
# -----------------------------

st.subheader("💳 Transaction Data")

st.dataframe(
    df,
    use_container_width=True
)



from pathlib import Path
import pandas as pd
import streamlit as st

# CSV path
BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "data" / "transaction.csv"

# Check file
if not CSV_FILE.exists():
    st.error(f"❌ transaction.csv not found: {CSV_FILE}")
    st.stop()

# Load data
df = pd.read_csv(CSV_FILE)

# Clean column names
df.columns = df.columns.str.strip()

st.success(f"✅ Loaded {len(df)} transaction")

st.write("Columns:")
st.write(df.columns.tolist())

st.dataframe(df.head(10))


st.header("🔍 Suspicious Account Search")

account_id = st.text_input(
    "Enter Account ID",
    placeholder="Example: ACC101"
)

if account_id:

    account_id = account_id.strip()

    sent = df[df["sender"].astype(str) == account_id]
    received = df[df["receiver"].astype(str) == account_id]

    transactions = len(sent) + len(received)

    connections = set(sent["receiver"].astype(str))
    connections.update(received["sender"].astype(str))

    connections.discard(account_id)

    high_count = len(
        pd.concat([sent, received])
        [pd.concat([sent, received])["risk"].astype(str).str.upper() == "HIGH"]
    )

    medium_count = len(
        pd.concat([sent, received])
        [pd.concat([sent, received])["risk"].astype(str).str.upper() == "MEDIUM"]
    )

    risk_score = min(
        100,
        high_count * 10 + medium_count * 5
    )

    if risk_score >= 61:
        status = "HIGH RISK"
    elif risk_score >= 31:
        status = "MEDIUM RISK"
    else:
        status = "LOW RISK"

    if transactions == 0:
        st.warning(f"Account {account_id} not found.")
    else:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Risk Score", risk_score)

        with col2:
            st.metric("Connections", len(connections))

        with col3:
            st.metric("Transactions", transactions)

        st.write(f"### Account: `{account_id}`")
        st.write(f"**Status:** {status}")

        st.subheader("Transaction Details")

        account_transactions = pd.concat(
            [sent, received]
        ).drop_duplicates()

        st.dataframe(account_transactions)
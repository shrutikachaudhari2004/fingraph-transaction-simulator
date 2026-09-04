import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="FinGraph Fraud Dashboard",
    page_icon="🔎",
    layout="wide"
)

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🔎 FinGraph Fraud Detection Dashboard")
st.write("Real-time Financial Fraud Detection Analysis")

# --------------------------------------------------
# FIND transaction.csv AUTOMATICALLY
# --------------------------------------------------

current_folder = Path(_file_).resolve().parent

possible_files = [
    current_folder / "transaction.csv",
    current_folder.parent / "transaction.csv",
    current_folder.parent.parent / "transaction.csv",
    current_folder.parent.parent.parent / "transaction.csv",
    Path.cwd() / "transaction.csv",
]

csv_file = None

for file in possible_files:
    if file.exists():
        csv_file = file
        break

# --------------------------------------------------
# FILE UPLOAD OPTION
# --------------------------------------------------

if csv_file is None:

    st.warning("⚠️ transaction.csv automatically found नाही.")

    uploaded_file = st.file_uploader(
        "Upload transaction.csv",
        type=["csv"]
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.info("कृपया transaction.csv upload करा.")
        st.stop()

else:

    st.success(f"✅ CSV Found: {csv_file}")

    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        st.error(f"CSV read करताना error: {e}")
        st.stop()

# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

df.columns = df.columns.str.strip()

# Remove completely empty rows
df = df.dropna(how="all")

# --------------------------------------------------
# CREATE RISK COLUMN
# --------------------------------------------------

if "amount" in df.columns:

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    def calculate_risk(amount):

        if pd.isna(amount):
            return "LOW"

        if amount > 10000:
            return "HIGH"

        elif amount > 5000:
            return "MEDIUM"

        else:
            return "LOW"

    df["risk"] = df["amount"].apply(calculate_risk)

else:

    df["risk"] = "LOW"

# --------------------------------------------------
# FRAUD COLUMN
# --------------------------------------------------

if "isFraud" in df.columns:

    # Convert different possible values to numeric
    df["isFraud"] = pd.to_numeric(
        df["isFraud"],
        errors="coerce"
    ).fillna(0)

else:

    # If isFraud column does not exist
    df["isFraud"] = 0

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_transactions = len(df)

high_risk = len(
    df[df["risk"] == "HIGH"]
)

medium_risk = len(
    df[df["risk"] == "MEDIUM"]
)

low_risk = len(
    df[df["risk"] == "LOW"]
)

fraud_transactions = int(
    df["isFraud"].sum()
)

# --------------------------------------------------
# SUSPICIOUS ACCOUNTS
# --------------------------------------------------

account_columns = []

if "sender" in df.columns:
    account_columns.append("sender")

if "receiver" in df.columns:
    account_columns.append("receiver")

if len(account_columns) > 0:

    accounts = pd.concat(
        [df[col].astype(str) for col in account_columns],
        ignore_index=True
    )

    suspicious_accounts = 0

    for account in accounts.unique():

        account_data = df[
            (df["sender"].astype(str) == account)
            if "sender" in df.columns
            else pd.Series(False, index=df.index)
        ]

        if "receiver" in df.columns:

            receiver_data = df[
                df["receiver"].astype(str) == account
            ]

            account_data = pd.concat(
                [account_data, receiver_data]
            )

        if len(account_data) >= 3:

            suspicious_accounts += 1

else:

    suspicious_accounts = 0

# --------------------------------------------------
# DASHBOARD KPIs
# --------------------------------------------------

st.subheader("📊 Dashboard KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Transactions",
        total_transactions
    )

with col2:
    st.metric(
        "🔴 High Risk",
        high_risk
    )

with col3:
    st.metric(
        "🟠 Medium Risk",
        medium_risk
    )

with col4:
    st.metric(
        "🚨 Fraud Transactions",
        fraud_transactions
    )

st.divider()

# --------------------------------------------------
# SECOND KPI ROW
# --------------------------------------------------

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "🟢 Low Risk",
        low_risk
    )

with col6:
    st.metric(
        "⚠️ Suspicious Accounts",
        suspicious_accounts
    )

with col7:
    if total_transactions > 0:
        fraud_percentage = (
            fraud_transactions / total_transactions
        ) * 100
    else:
        fraud_percentage = 0

    st.metric(
        "Fraud %",
        f"{fraud_percentage:.2f}%"
    )

with col8:
    if "amount" in df.columns:
        total_amount = df["amount"].sum()
    else:
        total_amount = 0

    st.metric(
        "💰 Total Amount",
        f"₹{total_amount:,.2f}"
    )

# --------------------------------------------------
# RISK DISTRIBUTION
# --------------------------------------------------

st.divider()

st.subheader("📈 Risk Level Distribution")

risk_data = df["risk"].value_counts()

st.bar_chart(risk_data)

# --------------------------------------------------
# FRAUD DISTRIBUTION
# --------------------------------------------------

st.subheader("🚨 Fraud Distribution")

fraud_data = df["isFraud"].value_counts()

st.bar_chart(fraud_data)

# --------------------------------------------------
# TRANSACTION DATA
# --------------------------------------------------

st.divider()

st.subheader("📋 Transaction Data")

st.dataframe(
    df,
    use_container_width=True,
    height=400
)

# --------------------------------------------------
# HIGH RISK TRANSACTIONS
# --------------------------------------------------

st.subheader("🔴 High Risk Transactions")

high_risk_data = df[
    df["risk"] == "HIGH"
]

if len(high_risk_data) > 0:

    st.dataframe(
        high_risk_data,
        use_container_width=True
    )

else:

    st.info("No High Risk Transactions Found.")

# --------------------------------------------------
# FRAUD TRANSACTIONS
# --------------------------------------------------

st.subheader("🚨 Fraudulent Transactions")

fraud_data_table = df[
    df["isFraud"] == 1
]

if len(fraud_data_table) > 0:

    st.dataframe(
        fraud_data_table,
        use_container_width=True
    )

else:

    st.info("No Fraudulent Transactions Found.")

# --------------------------------------------------
# ACCOUNT SEARCH
# --------------------------------------------------

st.divider()

st.subheader("🔍 Suspicious Account Search")

account_id = st.text_input(
    "Enter Account ID",
    placeholder="Example: ACC101"
)

if st.button("Search Account"):

    if account_id.strip() == "":
        st.warning("Please enter Account ID.")

    else:

        account_id = account_id.strip()

        result = pd.DataFrame()

        if "sender" in df.columns:

            sender_result = df[
                df["sender"].astype(str) == account_id
            ]

            result = pd.concat(
                [result, sender_result]
            )

        if "receiver" in df.columns:

            receiver_result = df[
                df["receiver"].astype(str) == account_id
            ]

            result = pd.concat(
                [result, receiver_result]
            )

        result = result.drop_duplicates()

        if len(result) > 0:

            st.success(
                f"✅ Account Found: {account_id}"
            )

            st.write(
                f"*Account:* {account_id}"
            )

            st.write(
                f"*Transactions:* {len(result)}"
            )

            high_count = len(
                result[result["risk"] == "HIGH"]
            )

            st.write(
                f"*High Risk Transactions:* {high_count}"
            )

            if high_count >= 3:
                st.error("🚨 Status: HIGH RISK")

            elif high_count >= 1:
                st.warning("⚠️ Status: MEDIUM RISK")

            else:
                st.success("🟢 Status: LOW RISK")

            st.dataframe(
                result,
                use_container_width=True
            )

        else:

            st.error(
                f"❌ Account {account_id} not found."
            )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "FinGraph Fraud Detection System | Python + Streamlit + Pandas"
)


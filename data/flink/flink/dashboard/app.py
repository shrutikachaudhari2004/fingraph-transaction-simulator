[11:04 pm, 04/09/2026] Shrutika Chaudhari: from pathlib import Path
import pandas as pd
import streamlit as st

# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="FinGraph Fraud Detection",
    page_icon="🔍",
    layout="wide"
)

# =========================================================
# 2. DASHBOARD TITLE
# =========================================================

st.title("🔍 FinGraph Fraud Detection Dashboard")

st.markdown("---")


# =========================================================
# 3. FIND transaction.csv
# =========================================================

# Current app.py location
BASE_DIR = Path(_file_).resolve()

# Project folder:
# fingraph…
[11:10 pm, 04/09/2026] Shrutika Chaudhari: cd "C:\Users\user5\Desktop\fingraph-transaction-simulator"
[11:19 pm, 04/09/2026] Shrutika Chaudhari: # =========================================================
# 20. SUSPICIOUS ACCOUNT SEARCH
# =========================================================

st.markdown("---")

st.subheader("🔎 Suspicious Account Investigation")

st.write(
    "Enter an Account ID to investigate its transaction activity."
)

# Account ID input
account_id = st.text_input(
    "Enter Account ID:",
    placeholder="Example: ACC101"
)


if account_id:

    # Remove extra spaces
    account_id = account_id.strip().upper()

    # Find transactions where account is sender OR receiver
    account_transactions = df[
        (df["sender"].astype(str).str.upper() == account_id)
        |
        (df["receiver"].astype(str).str.upper() == account_id)
    ]

    # Check account exists
    if…
[11:25 pm, 04/09/2026] Shrutika Chaudhari: # =========================================================
# 20. SUSPICIOUS ACCOUNT SEARCH
# =========================================================

st.markdown("---")

st.subheader("🔎 Suspicious Account Investigation")

st.write(
    "Enter an Account ID to investigate its transaction activity."
)

# Account ID input
account_id = st.text_input(
    "Enter Account ID:",
    placeholder="Example: ACC101"
)


if account_id:

    # Remove extra spaces
    account_id = account_id.strip().upper()

    # Find transactions where account is sender OR receiver
    account_transactions = df[
        (df["sender"].astype(str).str.upper() == account_id)
        |
        (df["receiver"].astype(str).str.upper() == account_id)
    ]

    # Check account exists
    if account_transactions.empty:

        st.warning(
            f"⚠️ Account {account_id} not found in transaction data."
        )

    else:

        # -----------------------------------------
        # Transaction Count
        # -----------------------------------------

        transaction_count = len(
            account_transactions
        )

        # -----------------------------------------
        # Connections
        # -----------------------------------------

        senders = set(
            account_transactions["sender"]
            .astype(str)
        )

        receivers = set(
            account_transactions["receiver"]
            .astype(str)
        )

        connections = (
            senders.union(receivers)
        )

        # Remove searched account itself
        connections.discard(account_id)

        connection_count = len(connections)

        # -----------------------------------------
        # High Risk Transactions
        # -----------------------------------------

        high_count = len(
            account_transactions[
                account_transactions["risk"] == "High"
            ]
        )

        # -----------------------------------------
        # Medium Risk Transactions
        # -----------------------------------------

        medium_count = len(
            account_transactions[
                account_transactions["risk"] == "Medium"
            ]
        )

        # -----------------------------------------
        # Risk Score
        # -----------------------------------------

        risk_score = (
            high_count * 10
            + medium_count * 3
            + connection_count
        )

        # Maximum score = 100
        risk_score = min(
            int(risk_score),
            100
        )

        # -----------------------------------------
        # Status
        # -----------------------------------------

        if risk_score >= 70:

            status = "HIGH RISK"

        elif risk_score >= 40:

            status = "MEDIUM RISK"

        else:

            status = "LOW RISK"

        # -----------------------------------------
        # Display Account
        # -----------------------------------------

        st.success(
            f"Account: {account_id}"
        )

        # -----------------------------------------
        # KPI Cards
        # -----------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Risk Score",
                risk_score
            )

        with col2:

            st.metric(
                "Connections",
                connection_count
            )

        with col3:

            st.metric(
                "Transactions",
                transaction_count
            )

        with col4:

            st.metric(
                "High Risk Transactions",
                high_count
            )

        # -----------------------------------------
        # Status
        # -----------------------------------------

        if status == "HIGH RISK":

            st.error(
                f"🚨 Status: {status}"
            )

        elif status == "MEDIUM RISK":

            st.warning(
                f"⚠️ Status: {status}"
            )

        else:

            st.success(
                f"✅ Status: {status}"
            )

        # -----------------------------------------
        # Account Transactions
        # -----------------------------------------

        st.subheader(
            f"💳 Transactions for {account_id}"
        )

        st.dataframe(
            account_transactions,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# 20. SUSPICIOUS ACCOUNT SEARCH
# =========================================================

st.markdown("---")

st.subheader("🔎 Suspicious Account Investigation")

st.write(
    "Enter an Account ID to investigate its transaction activity."
)

# Account ID input
account_id = st.text_input(
    "Enter Account ID:",
    placeholder="Example: ACC101"
)


if account_id:

    # Remove extra spaces
    account_id = account_id.strip().upper()

    # Find transactions where account is sender OR receiver
    account_transactions = df[
        (df["sender"].astype(str).str.upper() == account_id)
        |
        (df["receiver"].astype(str).str.upper() == account_id)
    ]

    # Check account exists
    if account_transactions.empty:

        st.warning(
            f"⚠️ Account {account_id} not found in transaction data."
        )

    else:

        # -----------------------------------------
        # Transaction Count
        # -----------------------------------------

        transaction_count = len(
            account_transactions
        )

        # -----------------------------------------
        # Connections
        # -----------------------------------------

        senders = set(
            account_transactions["sender"]
            .astype(str)
        )

        receivers = set(
            account_transactions["receiver"]
            .astype(str)
        )

        connections = (
            senders.union(receivers)
        )

        # Remove searched account itself
        connections.discard(account_id)

        connection_count = len(connections)

        # -----------------------------------------
        # High Risk Transactions
        # -----------------------------------------

        high_count = len(
            account_transactions[
                account_transactions["risk"] == "High"
            ]
        )

        # -----------------------------------------
        # Medium Risk Transactions
        # -----------------------------------------

        medium_count = len(
            account_transactions[
                account_transactions["risk"] == "Medium"
            ]
        )

        # -----------------------------------------
        # Risk Score
        # -----------------------------------------

        risk_score = (
            high_count * 10
            + medium_count * 3
            + connection_count
        )

        # Maximum score = 100
        risk_score = min(
            int(risk_score),
            100
        )

        # -----------------------------------------
        # Status
        # -----------------------------------------

        if risk_score >= 70:

            status = "HIGH RISK"

        elif risk_score >= 40:

            status = "MEDIUM RISK"

        else:

            status = "LOW RISK"

        # -----------------------------------------
        # Display Account
        # -----------------------------------------

        st.success(
            f"Account: {account_id}"
        )

        # -----------------------------------------
        # KPI Cards
        # -----------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Risk Score",
                risk_score
            )

        with col2:

            st.metric(
                "Connections",
                connection_count
            )

        with col3:

            st.metric(
                "Transactions",
                transaction_count
            )

        with col4:

            st.metric(
                "High Risk Transactions",
                high_count
            )

        # -----------------------------------------
        # Status
        # -----------------------------------------

        if status == "HIGH RISK":

            st.error(
                f"🚨 Status: {status}"
            )

        elif status == "MEDIUM RISK":

            st.warning(
                f"⚠️ Status: {status}"
            )

        else:

            st.success(
                f"✅ Status: {status}"
            )

        # -----------------------------------------
        # Account Transactions
        # -----------------------------------------

        st.subheader(
            f"💳 Transactions for {account_id}"
        )

        st.dataframe(
            account_transactions,
            use_container_width=True,
            hide_index=True
        )
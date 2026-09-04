[11:48 pm, 04/09/2026] Shrutika Chaudhari: from pathlib import Path
import streamlit as st
import pandas as pd

# Find project folder
BASE_DIR = Path(_file_).resolve().parents[3]

# CSV file
csv_path = BASE_DIR / "data" / "transaction.csv"

st.title("🔍 FinGraph Fraud Detection Dashboard")

if not csv_path.exists():
    st.error(f"❌ transaction.csv not found at: {csv_path}")
    st.stop()

df = pd.read_csv(csv_path)

st.success("✅ transaction.csv loaded successfully!")

st.write("Total Records:", len(df))

st.dataframe(df, use_container_width=True)
[11:52 pm, 04/09/2026] Shrutika Chaudhari: from pathlib import Path
import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="FinGraph Fraud Detection Dashboard",
    page_icon="🔍",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("🔍 FinGraph Fraud Detection Dashboard")
st.markdown("### Real-Time Financial Fraud Detection System")

# =========================================================
# FIND PROJECT DIRECTORY
# =========================================================

APP_DIR = Path(_file_).resolve()

# Search for transaction.csv
possible_paths = [
    APP_DIR.parent / "transaction.csv",
    APP_DIR.parent.parent / "transaction.csv",
    APP_DIR.parent.parent.parent / "transaction.csv",
    APP_DIR.parent.parent.parent.parent / "transaction.csv",
    APP_DIR.parent.parent.parent.parent.parent / "transaction.csv",
]

csv_path = None

for path in possible_paths:
    if path.exists():
        csv_path = path
        break

# =========================================================
# LOAD CSV
# =========================================================

if csv_path is None:
    st.error("❌ transaction.csv file not found!")

    st.info(
        "Please make sure that transaction.csv exists "
        "inside your project folder."
    )

    st.stop()

try:
    df = pd.read_csv(csv_path)

except Exception as e:
    st.error(f"❌ Error reading transaction.csv: {e}")
    st.stop()

# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = df.columns.str.strip()

# =========================================================
# SUCCESS MESSAGE
# =========================================================

st.success(
    f"✅ transaction.csv loaded successfully! "
    f"Records: {len(df)}"
)

# =========================================================
# BASIC DATA CLEANING
# =========================================================

if "amount" in df.columns:

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    ).fillna(0)

# =========================================================
# RISK CALCULATION
# =========================================================

if "risk" in df.columns:

    df["risk"] = (
        df["risk"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

else:

    if "amount" in df.columns:

        df["risk"] = "LOW"

        df.loc[
            df["amount"] > 5000,
            "risk"
        ] = "MEDIUM"

        df.loc[
            df["amount"] > 10000,
            "risk"
        ] = "HIGH"

    else:

        df["risk"] = "LOW"

# =========================================================
# KPI CALCULATIONS
# =========================================================

total_transactions = len(df)

high_risk = (
    df["risk"] == "HIGH"
).sum()

medium_risk = (
    df["risk"] == "MEDIUM"
).sum()

low_risk = (
    df["risk"] == "LOW"
).sum()

# =========================================================
# SUSPICIOUS ACCOUNTS
# =========================================================

if "sender" in df.columns:

    suspicious_accounts = (
        df.loc[
            df["risk"] == "HIGH",
            "sender"
        ]
        .nunique()
    )

elif "account_id" in df.columns:

    suspicious_accounts = (
        df.loc[
            df["risk"] == "HIGH",
            "account_id"
        ]
        .nunique()
    )

else:

    suspicious_accounts = 0

# =========================================================
# DASHBOARD KPIs
# =========================================================

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
        "⚠️ Suspicious Accounts",
        suspicious_accounts
    )

# =========================================================
# ADDITIONAL KPI
# =========================================================

st.subheader("📈 Additional Statistics")

col5, col6, col7 = st.columns(3)

with col5:

    st.metric(
        "🟢 Low Risk",
        low_risk
    )

with col6:

    if "amount" in df.columns:

        total_amount = df["amount"].sum()

        st.metric(
            "💰 Total Amount",
            f"{total_amount:,.2f}"
        )

    else:

        st.metric(
            "💰 Total Amount",
            "N/A"
        )

with col7:

    if "amount" in df.columns:

        average_amount = df["amount"].mean()

        st.metric(
            "💵 Average Transaction",
            f"{average_amount:,.2f}"
        )

    else:

        st.metric(
            "💵 Average Transaction",
            "N/A"
        )

# =========================================================
# RISK DISTRIBUTION
# =========================================================

st.subheader("🚨 Risk Distribution")

risk_counts = df["risk"].value_counts()

st.bar_chart(risk_counts)

# =========================================================
# FRAUD TRANSACTIONS
# =========================================================

st.subheader("🚨 High Risk Transactions")

high_risk_df = df[
    df["risk"] == "HIGH"
]

if len(high_risk_df) > 0:

    st.dataframe(
        high_risk_df,
        use_container_width=True
    )

else:

    st.info("No HIGH risk transactions found.")

# =========================================================
# ACCOUNT SEARCH
# =========================================================

st.subheader("🔎 Suspicious Account Search")

# Determine available account column

account_column = None

if "account_id" in df.columns:

    account_column = "account_id"

elif "sender" in df.columns:

    account_column = "sender"

# =========================================================
# ACCOUNT SEARCH SECTION
# =========================================================

if account_column is not None:

    account_list = (
        df[account_column]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    account_id = st.text_input(
        "Enter Account ID:",
        placeholder="Example: ACC101"
    )

    if account_id:

        account_id = account_id.strip()

        account_data = df[
            df[account_column]
            .astype(str)
            .str.upper()
            == account_id.upper()
        ]

        if len(account_data) > 0:

            st.success(
                f"✅ Account found: {account_id}"
            )

            # -------------------------------------------------
            # ACCOUNT TRANSACTIONS
            # -------------------------------------------------

            account_transactions = len(
                account_data
            )

            # -------------------------------------------------
            # CONNECTIONS
            # -------------------------------------------------

            if "receiver" in df.columns:

                connections = (
                    account_data["receiver"]
                    .nunique()
                )

            else:

                connections = 0

            # -------------------------------------------------
            # RISK SCORE
            # -------------------------------------------------

            high_count = (
                account_data["risk"] == "HIGH"
            ).sum()

            medium_count = (
                account_data["risk"] == "MEDIUM"
            ).sum()

            risk_score = (
                high_count * 10
                + medium_count * 5
            )

            if risk_score > 100:
                risk_score = 100

            # -------------------------------------------------
            # ACCOUNT STATUS
            # -------------------------------------------------

            if risk_score >= 70:

                status = "HIGH RISK"

            elif risk_score >= 40:

                status = "MEDIUM RISK"

            else:

                status = "LOW RISK"

            # -------------------------------------------------
            # ACCOUNT KPIs
            # -------------------------------------------------

            a1, a2, a3, a4 = st.columns(4)

            with a1:

                st.metric(
                    "Account",
                    account_id
                )

            with a2:

                st.metric(
                    "Risk Score",
                    risk_score
                )

            with a3:

                st.metric(
                    "Connections",
                    connections
                )

            with a4:

                st.metric(
                    "Transactions",
                    account_transactions
                )

            # -------------------------------------------------
            # STATUS
            # -------------------------------------------------

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

            # -------------------------------------------------
            # ACCOUNT TRANSACTION DATA
            # -------------------------------------------------

            st.subheader(
                f"💳 Transactions for {account_id}"
            )

            st.dataframe(
                account_data,
                use_container_width=True
            )

        else:

            st.warning(
                f"⚠️ Account {account_id} not found."
            )

else:

    st.info(
        "Account search is unavailable because "
        "no account_id or sender column exists."
    )

# =========================================================
# COMPLETE TRANSACTION DATA
# =========================================================

st.subheader("💳 All Transaction Data")

st.write(
    f"Total Records Available: *{len(df)}*"
)

st.dataframe(
    df,
    use_container_width=True,
    height=500
)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "FinGraph | Financial Fraud Detection System"
)
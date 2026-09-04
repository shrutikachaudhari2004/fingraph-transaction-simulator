[10:56 pm, 04/09/2026] Shrutika Chaudhari: import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path

records = []

for i in range(10000):

    sender = f"ACC{random.randint(100, 999)}"
    receiver = f"ACC{random.randint(100, 999)}"

    while sender == receiver:
        receiver = f"ACC{random.randint(100, 999)}"

    amount = random.randint(100, 20000)

    if amount > 15000:
        risk = "HIGH"
    elif amount > 8000:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    isFraud = 1 if risk == "HIGH" and random.random() < 0.5 else 0

    records.append({
        "transaction_id": f"TX{i+1:05d}",
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "timestamp": datetime.now() - timedelta(minutes=i),
        "ris…
[10:58 pm, 04/09/2026] Shrutika Chaudhari: python -c "import pandas as pd; df=pd.read_csv('data/transaction.csv'); print(len(df))"
[10:58 pm, 04/09/2026] Shrutika Chaudhari: import pandas as pd

df = pd.read_csv(
    r"C:\Users\user5\Desktop\fingraph-transaction-simulator\data\transaction.csv"
)
[11:00 pm, 04/09/2026] Shrutika Chaudhari: python -m streamlit run data\flink\flink\dashboard\app.py
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
# fingraph-transaction-simulator
PROJECT_DIR = BASE_DIR.parents[3]

# transaction.csv should be in project root
CSV_PATH = PROJECT_DIR / "transaction.csv"


# =========================================================
# 4. CHECK CSV FILE
# =========================================================

if not CSV_PATH.exists():

    st.error("❌ transaction.csv file not found!")

    st.write("Expected location:")
    st.code(str(CSV_PATH))

    st.info(
        "Please keep transaction.csv inside the "
        "fingraph-transaction-simulator folder."
    )

    st.stop()


# =========================================================
# 5. READ CSV
# =========================================================

try:

    df = pd.read_csv(CSV_PATH)

except Exception as e:

    st.error(f"❌ Error while reading CSV: {e}")

    st.stop()


# =========================================================
# 6. CHECK DATA
# =========================================================

if df.empty:

    st.warning("⚠️ transaction.csv is empty.")

    st.stop()


# =========================================================
# 7. CLEAN COLUMN NAMES
# =========================================================

df.columns = df.columns.str.strip()


# =========================================================
# 8. CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "transaction_id",
    "sender",
    "receiver",
    "amount",
    "timestamp"
]

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]


if missing_columns:

    st.error("❌ Required columns are missing!")

    st.write("Missing columns:")
    st.write(missing_columns)

    st.write("Available columns:")
    st.write(list(df.columns))

    st.stop()


# =========================================================
# 9. CONVERT AMOUNT TO NUMBER
# =========================================================

df["amount"] = pd.to_numeric(
    df["amount"],
    errors="coerce"
)

# Remove invalid amount records
df = df.dropna(
    subset=["amount"]
)


# =========================================================
# 10. RISK CALCULATION
# =========================================================

def calculate_risk(amount):

    if amount > 15000:

        return "High"

    elif amount > 10000:

        return "Medium"

    else:

        return "Low"


df["risk"] = df["amount"].apply(
    calculate_risk
)


# =========================================================
# 11. KPI CALCULATIONS
# =========================================================

total_transactions = len(df)

high_risk = len(
    df[df["risk"] == "High"]
)

medium_risk = len(
    df[df["risk"] == "Medium"]
)

low_risk = len(
    df[df["risk"] == "Low"]
)

# Accounts involved in High Risk transactions
suspicious_accounts = df[
    df["risk"] == "High"
]["sender"].nunique()


# =========================================================
# 12. DISPLAY KPIs
# =========================================================

st.subheader("📊 Dashboard KPIs")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        label="💳 Total Transactions",
        value=f"{total_transactions:,}"
    )


with col2:

    st.metric(
        label="🔴 High Risk",
        value=f"{high_risk:,}"
    )


with col3:

    st.metric(
        label="🟠 Medium Risk",
        value=f"{medium_risk:,}"
    )


with col4:

    st.metric(
        label="⚠️ Suspicious Accounts",
        value=f"{suspicious_accounts:,}"
    )


st.markdown("---")


# =========================================================
# 13. RISK SUMMARY
# =========================================================

st.subheader("🚨 Risk Distribution")


risk_data = pd.DataFrame(
    {
        "Risk Level": [
            "High",
            "Medium",
            "Low"
        ],

        "Transactions": [
            high_risk,
            medium_risk,
            low_risk
        ]
    }
)


col1, col2 = st.columns(2)


with col1:

    st.dataframe(
        risk_data,
        use_container_width=True,
        hide_index=True
    )


with col2:

    chart_data = risk_data.set_index(
        "Risk Level"
    )

    st.bar_chart(chart_data)


# =========================================================
# 14. TOTAL AMOUNT
# =========================================================

st.markdown("---")

st.subheader("💰 Transaction Amount")


total_amount = df["amount"].sum()

average_amount = df["amount"].mean()


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Total Transaction Amount",
        f"₹{total_amount:,.2f}"
    )


with col2:

    st.metric(
        "Average Transaction Amount",
        f"₹{average_amount:,.2f}"
    )


# =========================================================
# 15. HIGH RISK TRANSACTIONS
# =========================================================

st.markdown("---")

st.subheader("🔴 High Risk Transactions")


high_risk_data = df[
    df["risk"] == "High"
].sort_values(
    by="amount",
    ascending=False
)


st.dataframe(
    high_risk_data,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# 16. MEDIUM RISK TRANSACTIONS
# =========================================================

st.markdown("---")

st.subheader("🟠 Medium Risk Transactions")


medium_risk_data = df[
    df["risk"] == "Medium"
].sort_values(
    by="amount",
    ascending=False
)


st.dataframe(
    medium_risk_data,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# 17. TOP SUSPICIOUS ACCOUNTS
# =========================================================

st.markdown("---")

st.subheader("⚠️ Suspicious Accounts")


suspicious_data = (
    df[df["risk"] == "High"]
    .groupby("sender")
    .agg(
        High_Risk_Transactions=(
            "transaction_id",
            "count"
        ),

        Total_Amount=(
            "amount",
            "sum"
        )
    )
    .sort_values(
        by="High_Risk_Transactions",
        ascending=False
    )
)


if not suspicious_data.empty:

    st.dataframe(
        suspicious_data,
        use_container_width=True
    )

else:

    st.info(
        "No suspicious accounts found."
    )


# =========================================================
# 18. COMPLETE TRANSACTION DATA
# =========================================================

st.markdown("---")

st.subheader("💳 Complete Transaction Data")


st.write(
    f"Total records available: *{len(df):,}*"
)


st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# 19. DOWNLOAD DATA
# =========================================================

st.markdown("---")

st.subheader("⬇️ Download")


csv_download = df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="📥 Download Transaction Data",
    data=csv_download,
    file_name="fingraph_transactions.csv",
    mime="text/csv"
)


# =========================================================
# 20. FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "FinGraph Fraud Detection System | "
    "Python + Pandas + Streamlit"
)
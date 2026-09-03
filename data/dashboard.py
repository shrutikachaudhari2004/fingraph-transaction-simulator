import streamlit as st

st.set_page_config(
    page_title="FinGraph Fraud Detection",
    page_icon="💰",
    layout="wide"
)

st.title("💰 FinGraph - Fraud Detection Dashboard")

st.write("Real-Time Financial Fraud Detection System")

st.success("Streamlit is working successfully!")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Transactions", 10000)

with col2:
    st.metric("Risk Level", "HIGH")

with col3:
    st.metric("Fraud Status", "Monitoring")

st.subheader("Risk Score")

risk_score = st.slider(
    "Select Risk Score",
    0,
    100,
    70
)

if risk_score <= 30:
    st.success("Risk Level: LOW")
elif risk_score <= 60:
    st.warning("Risk Level: MEDIUM")
else:
    st.error("Risk Level: HIGH")




    import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="FinGraph Fraud Detection",
    page_icon="💰",
    layout="wide"
)

st.title("💰 FinGraph - Fraud Detection Dashboard")

# Load transaction data
df = pd.read_csv("transaction.csv")

# Total transactions
total_transactions = len(df)

# Display metrics
col1, col2, col3 = st.columns(3)

col1.metric("Total Transactions", total_transactions)

if "amount" in df.columns:
    col2.metric("Total Amount", f"₹{df['amount'].sum():,.2f}")

if "isFraud" in df.columns:
    fraud_count = df["isFraud"].sum()
    col3.metric("Fraud Transactions", int(fraud_count))

# Show data
st.subheader("📊 Transaction Data")
st.dataframe(df, use_container_width=True)

# Fraud chart
if "isFraud" in df.columns:
    st.subheader("🚨 Fraud Distribution")
    st.bar_chart(df["isFraud"].value_counts())
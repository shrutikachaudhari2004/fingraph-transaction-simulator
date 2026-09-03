import streamlit as st
import pandas as pd

st.set_page_config(page_title="FinGraph", layout="wide")

st.title("🔍 FinGraph Fraud Detection Dashboard")

df = pd.read_csv("transaction.csv")

st.subheader("📊 Transaction Data")
st.dataframe(df, use_container_width=True)

st.metric("Total Transactions", len(df))

if "amount" in df.columns:
    st.metric("Total Amount", f"{df['amount'].sum():,.2f}")

if "isFraud" in df.columns:
    fraud_count = int(df["isFraud"].sum())
    st.metric("Fraud Transactions", fraud_count)

    st.subheader("🚨 Fraud Distribution")
    st.bar_chart(df["isFraud"].value_counts())
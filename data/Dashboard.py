import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("transaction.csv")

print("Total Transactions:", len(df))

print("\nRisk Distribution:")
print(df["risk"].value_counts())

df["risk"].value_counts().plot(kind="bar")

plt.title("Fraud Risk Distribution")
plt.xlabel("Risk Level")
plt.ylabel("Number of Transactions")
plt.show()
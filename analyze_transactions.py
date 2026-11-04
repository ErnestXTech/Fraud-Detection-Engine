
import pandas as pd
from main import generate_transactions

# Generate sample transactions
transactions = generate_transactions()

# Convert transactions into a DataFrame
df = pd.DataFrame(transactions)

#  Display the first five transactions
print("\nFIRST FIVE TRANSACTIONS")
print(df.head())

# Find transactions of 500,000 or more
large_transactions = df[df["amount"] >= 500000]

print("\nLARGE TRANSACTIONS")
print(large_transactions)

#  Calculate the total amount transacted by each account
account_totals = df.groupby("account")["amount"].sum()

print("\nTOTAL AMOUNT BY ACCOUNT")
print(account_totals)

#  Count transactions made by each account
account_counts = df["account"].value_counts()

print("\nTRANSACTION COUNT BY ACCOUNT")
print(account_counts)

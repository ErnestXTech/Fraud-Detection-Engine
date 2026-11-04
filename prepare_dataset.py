
import pandas as pd
from sklearn.model_selection import train_test_split
from main import generate_transactions

# 1. Generate sample transactions
transactions = generate_transactions()

# 2. Convert transactions into a DataFrame
df = pd.DataFrame(transactions)

# 3. Convert transaction times from strings into datetime values
df["time"] = pd.to_datetime(df["time"])

# 4. Label the simulated suspicious transactions
suspicious_ids = [
    "TXN026",
    "TXN027",
    "TXN028",
    "TXN029",
    "TXN030",
    "TXN031",
    "TXN032"
]

df["label"] = df["id"].isin(suspicious_ids).astype(int)

# 5. Create a feature for rapid transaction activity
df["rapid_transaction_count"] = 0

for index, transaction in df.iterrows():
    recent_transactions = df[
        (df["account"] == transaction["account"])
        & (df["time"] <= transaction["time"])
        & (
            df["time"]
            >= transaction["time"] - pd.Timedelta(seconds=120)
        )
    ]

    df.loc[index, "rapid_transaction_count"] = len(
        recent_transactions
    )

# 6. Select the information the model will learn from
X = df[["amount", "rapid_transaction_count"]]

# 7. Select the correct answers the model should learn to predict
y = df["label"]

# 8. Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# 9. Display the results
print("\nFEATURES AND LABELS")
print(
    df[
        ["id", "amount", "rapid_transaction_count", "label"]
    ].to_string(index=False)
)

print("\nDATASET SPLIT")
print("Training features:", X_train.shape)
print("Testing features:", X_test.shape)
print("Training labels:", y_train.shape)
print("Testing labels:", y_test.shape)

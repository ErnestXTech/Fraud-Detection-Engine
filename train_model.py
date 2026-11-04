
import pandas as pd
import joblib
from main import generate_transactions
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# 1. Generate transactions
transactions = generate_transactions()
df = pd.DataFrame(transactions)

# 2. Convert transaction times into datetime values
df["time"] = pd.to_datetime(df["time"])

# 3. Label our simulated suspicious transactions
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

# 4. Calculate transaction frequency within 120 seconds
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

# 5. Choose the features and labels
X = df[["amount", "rapid_transaction_count"]]
y = df["label"]

# 6. Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# 7. Create the Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

# 8. Train the model
model.fit(X_train, y_train)
# Save the trained model to a file
joblib.dump(model, "sentinel_model.joblib")

print("Sentinel model saved successfully.")

# 9. Predict labels for the test data
predictions = model.predict(X_test)

# 10. Display the evaluation results
print("\nCLASSIFICATION REPORT")
print(
    classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["Legitimate", "Suspicious"],
        zero_division=0
    )
)

print("CONFUSION MATRIX")
print(confusion_matrix(y_test, predictions, labels=[0, 1]))


from datetime import datetime,timedelta 
import random

def generate_transactions():
    transactions = []

    start_time = datetime(2026, 10, 10, 8, 0, 0)

    accounts = ["ACC101", "ACC202", "ACC303", "ACC404", "ACC505"]

    # Generate 25 ordinary transactions
    for i in range(25):
        transaction = {
            "id": f"TXN{i + 1:03}",
            "account": random.choice(accounts),
            "amount": random.randint(1000, 80000),
            "time": (
                start_time + timedelta(minutes=i * 5)
            ).strftime("%Y-%m-%d %H:%M:%S")
        }

        transactions.append(transaction)

    # Add one unusually large transaction
    transactions.append({
        "id": "TXN026",
        "account": "ACC777",
        "amount": 950000,
        "time": (
            start_time + timedelta(hours=3)
        ).strftime("%Y-%m-%d %H:%M:%S")
    })

    # Generate six rapid transactions from one account
    suspicious_start = start_time + timedelta(hours=4)

    for i in range(6):
        transaction = {
            "id": f"TXN{27 + i:03}",
            "account": "ACC999",
            "amount": random.randint(20000, 50000),
            "time": (
                suspicious_start + timedelta(seconds=i * 20)
            ).strftime("%Y-%m-%d %H:%M:%S")
        }

        transactions.append(transaction)

    return transactions


transactions = generate_transactions()

def validate_transaction(transaction):
    required_fields = ["id", "account", "amount", "time"]

    for field in required_fields:
        if field not in transaction:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(transaction["amount"], (int, float)):
        raise ValueError("Amount must be a number")
    if transaction["amount"] < 0:
        raise ValueError("Amount cannot be negative")
    if not transaction["account"]:
        raise ValueError("Account ID cannot be empty")

    try:
        datetime.strptime(transaction["time"], "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        raise ValueError("Time must be in the format YYYY-MM-DD HH:MM:SS")
    return True

def detect_fraud(transaction, all_transactions):
    validate_transaction(transaction)

    risk_score = 0
    reasons = []

    # Rule 1: Check for unusually large transactions
    if transaction["amount"] >= 500000:
        risk_score += 50
        reasons.append("Unusually large transaction amount")

    # Rule 2: Check transaction frequency in the last 2 minutes
    
    # Rule 2: Detect rapid transactions from the same account
    transaction_time = datetime.strptime(
        transaction["time"], "%Y-%m-%d %H:%M:%S"
    )

    recent_count = 0

    for other in all_transactions:
        if other["account"] != transaction["account"]:
            continue

        if other["id"] == transaction["id"]:
            continue

        other_time = datetime.strptime(
            other["time"], "%Y-%m-%d %H:%M:%S"
        )

        difference = (
            transaction_time - other_time
        ).total_seconds()

        if 0 <= difference <= 120:
            recent_count += 1

    if recent_count >= 5:
        risk_score += 40
        reasons.append("Unusually high transaction frequency")

 
    # Keep the score between 0 and 100
    risk_score = min(risk_score, 100)

    if risk_score >= 70:
        status = "HIGH RISK"
    elif risk_score >= 40:
        status = "MEDIUM RISK"
    else:
        status = "LOW RISK"

    return {
        "transaction_id": transaction["id"],
        "amount": transaction["amount"],
        "risk_score": risk_score,
        "status": status,
        "reasons": reasons
    }


# Analyze all sample transactions

def main():
    # Generate transactions for Sentinel to analyze
    transactions = generate_transactions()

    print("Sentinel is starting...")

    # Analyze every transaction
    for transaction in transactions:
        result = detect_fraud(transaction, transactions)

        print("\n------------------------------")
        print("Transaction:", result["transaction_id"])
        print("Amount: ₦", format(result["amount"], ","))
        print("Risk score:", result["risk_score"], "/100")
        print("Status:", result["status"])

        if result["reasons"]:
            print("Reasons:", ", ".join(result["reasons"]))
        else:
            print("Reasons: No suspicious patterns detected")


if __name__ == "__main__":
    main()

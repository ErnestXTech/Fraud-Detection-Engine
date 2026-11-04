
from datetime import datetime, timedelta
import unittest
from main import detect_fraud


class TestSentinel(unittest.TestCase):

    def test_large_transaction(self):
        transaction = {
            "id": "TXN001",
            "account": "ACC101",
            "amount": 950000,
            "time": "2026-10-10 10:00:00"
        }

        result = detect_fraud(transaction, [transaction])

        self.assertEqual(result["risk_score"], 50)
        self.assertEqual(result["status"], "MEDIUM RISK")

    def test_normal_transaction(self):
        transaction = {
            "id": "TXN002",
            "account": "ACC202",
            "amount": 5000,
            "time": "2026-10-10 10:00:00"
        }

        result = detect_fraud(transaction, [transaction])

        self.assertEqual(result["risk_score"], 0)
        self.assertEqual(result["status"], "LOW RISK")

    def test_rapid_transactions(self):
        transactions = []

        for i in range(6):
            transactions.append({
                "id": f"TXN{i + 1:03}",
                "account": "ACC303",
                "amount": 20000,
                "time": (
    datetime(2026, 10, 10, 10, 0, 0)
    + timedelta(seconds=i * 20)
).strftime("%Y-%m-%d %H:%M:%S")
            })

        result = detect_fraud(
            transactions[-1],
            transactions
        )

        self.assertEqual(result["risk_score"], 40)
        self.assertEqual(result["status"], "MEDIUM RISK")

        
    def test_large_and_rapid_transaction(self):
        transactions = []

        for i in range(6):
            transactions.append({
                "id": f"TXN{i + 1:03}",
                "account": "ACC404",
                "amount": 20000,
                "time": (
                    datetime(2026, 10, 10, 10, 0, 0)
                    + timedelta(seconds=i * 20)
                ).strftime("%Y-%m-%d %H:%M:%S")
            })

        # Make the final transaction unusually large
        transactions[-1]["amount"] = 950000

        result = detect_fraud(
            transactions[-1],
            transactions
        )

        self.assertEqual(result["risk_score"], 90)
        self.assertEqual(result["status"], "HIGH RISK")
        self.assertEqual(len(result["reasons"]), 2)



if __name__ == "__main__":
    unittest.main()

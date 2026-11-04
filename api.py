
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
import joblib

from db import get_connection
from redis_tracker import record_transaction
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Sentinel Fraud Detection API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained machine-learning model
model = joblib.load("sentinel_model.joblib")


class Transaction(BaseModel):
    id: str = Field(min_length=1, max_length=50)
    account: str = Field(min_length=1, max_length=50)
    amount: float = Field(gt=0)
    transaction_time: str


@app.post("/predict")
def predict_fraud(transaction: Transaction):

    # Count recent transactions using Redis
    rapid_count = record_transaction(
        transaction.account,
        transaction.id
    )

    # Prepare the model features
    features = pd.DataFrame(
        [[transaction.amount, rapid_count]],
        columns=["amount", "rapid_transaction_count"]
    )

    # Get the model prediction
    prediction = int(model.predict(features)[0])
    status = "SUSPICIOUS" if prediction == 1 else "LEGITIMATE"

    # Save the transaction and prediction in PostgreSQL
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO transactions
(id, account, amount, transaction_time,
 status, review_status, rapid_transaction_count)
VALUES (%s, %s, %s, %s, %s, %s, %s)
RETURNING id;
                    """,
                    (
    transaction.id,
    transaction.account,
    transaction.amount,
    transaction.transaction_time,
    status,
    "PENDING",
    rapid_count
)
                )

                saved_id = cursor.fetchone()[0]

    except Exception as error:
        print("Database operation failed:", error)
        raise HTTPException(
            status_code=500,
            detail="Could not save transaction to the database."
        )

    return {
        "transaction_id": saved_id,
        "amount": transaction.amount,
        "rapid_transaction_count": rapid_count,
        "prediction": prediction,
        "status": status,
        "review_status": "PENDING"
    }


@app.get("/transactions")
def get_transactions():
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT id, account, amount, transaction_time,
       status, review_status, rapid_transaction_count
FROM transactions
                """)

                rows = cursor.fetchall()

                transactions = []

                for row in rows:

                 transactions.append({
    "id": row[0],
    "account": row[1],
    "amount": float(row[2]),
    "transaction_time": row[3].isoformat(),
    "status": row[4],
    "review_status": row[5],
    "rapid_transaction_count": row[6]
})
                return {"transactions": transactions}

    except Exception as error:
        print("Database operation failed:", error)
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve transactions."
        )


    
@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, account, amount, transaction_time,
                           status, review_status, rapid_transaction_count
                    FROM transactions
                    WHERE id = %s;
                    """,
                    (transaction_id,)
                )

                row = cursor.fetchone()

                if row is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Transaction not found."
                    )

                return {
                    "id": row[0],
                    "account": row[1],
                    "amount": float(row[2]),
                    "transaction_time": row[3].isoformat(),
                    "status": row[4],
                    "review_status": row[5],
                    "rapid_transaction_count": row[6]
                }

    except HTTPException:
        raise

    except Exception as error:
        print("Database operation failed:", error)
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve transaction."
        )

@app.patch("/transactions/{transaction_id}/review")
def review_transaction(transaction_id: str):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE transactions
                    SET review_status = 'REVIEWED'
                    WHERE id = %s
                    RETURNING id, status, review_status;
                    """,
                    (transaction_id,)
                )

                transaction = cursor.fetchone()

                if transaction is None:
                    raise HTTPException(
                        status_code=404,
                        detail="Transaction not found."
                    )

                return {
                    "id": transaction[0],
                    "status": transaction[1],
                    "review_status": transaction[2]
                }

    except HTTPException:
        raise

    except Exception as error:
        print("Database operation failed:", error)
        raise HTTPException(
            status_code=500,
            detail="Could not update transaction review status."
        )

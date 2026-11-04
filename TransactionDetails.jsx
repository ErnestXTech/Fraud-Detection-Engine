import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

function TransactionDetails() {
  const { transactionId } = useParams();
  async function markAsReviewed() {
  try {
    const response = await fetch(
      `http://127.0.0.1:8000/transactions/${transactionId}/review`,
      {
        method: "PATCH",
      }
    );

    if (!response.ok) {
      throw new Error("Failed to update review status");
    }

    const data = await response.json();

    setTransaction((previousTransaction) => ({
      ...previousTransaction,
      review_status: data.review_status,
    }));
  } catch (err) {
    setError(err.message);
  }
}

  const [transaction, setTransaction] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchTransaction() {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/transactions/${transactionId}`
        );

        if (!response.ok) {
          throw new Error("Failed to fetch transaction details");
        }

        const data = await response.json();

        setTransaction(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchTransaction();
  }, [transactionId]);

  if (loading) {
    return <p className="dashboard-content">Loading transaction...</p>;
  }

  if (error) {
    return <p className="dashboard-content">{error}</p>;
  }

  if (!transaction) {
    return <p className="dashboard-content">Transaction not found.</p>;
  }

  return (
    <div className="dashboard-content">
      <Link to="/transactions" className="back-link">
        ← Back to transactions
      </Link>

      <div className="welcome-section">
        <h2>Transaction Details</h2>
        <p>Investigate individual transaction activity.</p>
      </div>

      <div className="transactions-section">
        <h2>Transaction Information</h2>
        <h1 style={{ color: "red" }}>
  BUTTON TEST
</h1>

<button onClick={markAsReviewed}>
  Mark as Reviewed
</button>

        <div className="details-grid">
          <div>
            <span>Transaction ID</span>
            <h3>{transaction.id}</h3>
          </div>

          <div>
            <span>Account</span>
            <h3>{transaction.account}</h3>
          </div>

          <div>
            <span>Amount</span>
            <h3>₦{Number(transaction.amount).toLocaleString()}</h3>
          </div>

          <div>
            <span>Risk Status</span>
            <h3>{transaction.status}</h3>
          </div>

          <div>
            <span>Recent Transaction Count</span>
            <h3>{transaction.rapid_transaction_count ?? "Unavailable"}</h3>
          </div>
<div>
  <span>Review Status</span>
  <h3>{transaction.review_status}</h3>

  {transaction.review_status === "PENDING" && (
  <button onClick={markAsReviewed}>
    Mark as Reviewed
  </button>
)}
</div>
          <div>
            <span>Transaction Time</span>
            <h3>{new Date(transaction.transaction_time).toLocaleString()}</h3>
          </div>
        </div>
      </div>
    </div>
  );
}

export default TransactionDetails;
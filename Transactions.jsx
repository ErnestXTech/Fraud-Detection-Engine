import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchTransactions() {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/transactions"
        );

        if (!response.ok) {
          throw new Error("Failed to fetch transactions");
        }

        const data = await response.json();

        setTransactions(data.transactions);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchTransactions();
  }, []);

  return (
    <div className="dashboard-content">
      <div className="welcome-section">
        <h2>All Transactions</h2>
        <p>Monitor and investigate transactions processed by Sentinel.</p>
      </div>

      <div className="transactions-section">
        <h2>Transaction Records</h2>

        {loading && <p>Loading transactions...</p>}

        {error && <p>{error}</p>}

        {!loading && !error && transactions.length === 0 && (
          <p>No transactions found.</p>
        )}

        {!loading && !error && transactions.length > 0 && (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Transaction ID</th>
                  <th>Account</th>
                  <th>Amount</th>
                  <th>Risk Status</th>
                  <th>Review Status</th>
                </tr>
              </thead>

              <tbody>
                {transactions.map((transaction) => (
                  <tr key={transaction.id}>
                    <td>
                      <Link to={`/transactions/${transaction.id}`}>
                        {transaction.id}
                      </Link>
                    </td>

                    <td>{transaction.account}</td>

                    <td>
                      ₦{Number(transaction.amount).toLocaleString()}
                    </td>

                    <td>{transaction.status}</td>

                    <td>{transaction.review_status}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default Transactions;

function Dashboard() {
  return (
    <section className="dashboard-content">
      <div className="welcome-section">
        <h2>Fraud Monitoring Overview</h2>
        <p>Monitor transaction activity and suspicious behavior.</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <span>Total Transactions</span>
          <h2>1,284</h2>
          <p>Transactions processed</p>
        </div>

        <div className="stat-card">
          <span>Suspicious Transactions</span>
          <h2>48</h2>
          <p>Flagged for investigation</p>
        </div>

        <div className="stat-card">
          <span>Legitimate Transactions</span>
          <h2>1,236</h2>
          <p>Passed fraud screening</p>
        </div>

        <div className="stat-card">
          <span>Pending Reviews</span>
          <h2>12</h2>
          <p>Awaiting analyst review</p>
        </div>
      </div>
    </section>
  );
}

export default Dashboard;

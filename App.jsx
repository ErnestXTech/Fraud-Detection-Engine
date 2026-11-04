
import {
  BrowserRouter,
  Routes,
  Route,
  NavLink,
} from "react-router-dom";

import {
  ShieldCheck,
  LayoutDashboard,
  ArrowLeftRight,
  AlertTriangle,
  Settings,
  Activity,
  Bell,
} from "lucide-react";

import Dashboard from "./pages/Dashboard";
import Transactions from "./pages/Transactions";
import "./App.css";
import TransactionDetails from "./pages/TransactionDetails";

function AppLayout() {
  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">
          <ShieldCheck size={30} />
          <h2>Sentinel</h2>
        </div>

        <nav>
          <NavLink to="/dashboard">
            <LayoutDashboard size={20} />
            Dashboard
          </NavLink>

          <NavLink to="/transactions">
            <ArrowLeftRight size={20} />
            Transactions
          </NavLink>

          <NavLink to="/alerts">
            <AlertTriangle size={20} />
            Fraud Alerts
          </NavLink>

          <NavLink to="/settings">
            <Settings size={20} />
            Settings
          </NavLink>
        </nav>

        <div className="sidebar-footer">
          <Activity size={18} />
          <span>Fraud Engine Active</span>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <h1>Sentinel</h1>
            <p>Real-time fraud monitoring system</p>
          </div>

          <button aria-label="Notifications">
            <Bell />
          </button>
        </header>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/transactions" element={<Transactions />} />
          <Route
  path="/transactions/:transactionId"
  element={<TransactionDetails />}
/>
<Route path="/transactionDetails/:transactionId" element={<TransactionDetails />} />
          <Route
            path="/alerts"
            element={<h2 className="dashboard-content">Fraud Alerts</h2>}
          />
          <Route
            path="/settings"
            element={<h2 className="dashboard-content">Settings</h2>}
          />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AppLayout />
    </BrowserRouter>
  );
}

export default App;

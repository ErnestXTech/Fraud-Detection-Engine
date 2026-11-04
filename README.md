Fraud Detection Engine

A machine learning-powered fraud detection engine designed to identify suspicious financial transactions, analyze transaction patterns, and support fraud investigation through real-time monitoring.

## Overview

Financial fraud is a major challenge for financial institutions and digital payment platforms. Sentinel addresses this challenge by combining machine learning, transaction monitoring, and backend infrastructure to identify potentially fraudulent activities.

The system analyzes transaction data, evaluates suspicious patterns, generates fraud predictions, and provides a dashboard for monitoring and reviewing transactions.

## Key Features

- **Fraud Detection:** Machine learning-based transaction classification.
- **Risk Classification:** Identifies transactions as legitimate or suspicious.
- **Transaction Monitoring:** Tracks transaction activity and frequency.
- **REST API:** Processes transactions and serves fraud predictions.
- **Transaction Storage:** Persistent storage using PostgreSQL.
- **Redis Integration:** Tracks transaction activity.
- **Monitoring Dashboard:** React-based interface for viewing transactions.
- **Transaction Review:** Allows suspicious transactions to be reviewed.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core backend logic |
| FastAPI | REST API development |
| Scikit-learn | Machine learning |
| Pandas | Data processing |
| PostgreSQL | Database management |
| Redis | Transaction tracking |
| React | Frontend development |
| JavaScript | Frontend functionality |

## System Architecture

Sentinel consists of three major components:

1. **Frontend:** React dashboard for transaction monitoring and investigation.
2. **Backend:** FastAPI handles transaction processing and communication between system components.
3. **Detection Engine:** Scikit-learn model analyzes transaction features and generates predictions.

## Fraud Classification

Transactions are classified into two categories:

- **LEGITIMATE:** Transactions classified as normal.
- **SUSPICIOUS:** Transactions flagged for potential fraudulent activity.

## API Documentation

The backend API is built with FastAPI.

Interactive API documentation is available through Swagger UI at:

`http://127.0.0.1:8000/docs`

## Future Improvements

- Advanced fraud detection algorithms.
- Improved model accuracy through larger datasets.
- Real-time event streaming.
- Automated fraud alerts.
- Advanced analytics and reporting.
- Scalable deployment infrastructure.
- CI/CD pipeline integration.

## Project Status

Working prototype – actively developing and improving the detection engine and supporting infrastructure.

## Author

**Ernest Ugbaja**

Software Engineer | Backend Engineering | System Architecture
## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.


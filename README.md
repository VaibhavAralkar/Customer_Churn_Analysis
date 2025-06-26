
# HG Insights - ETL & Analytics Pipeline

## 🚀 Overview

This project orchestrates a complete ETL pipeline for telecom customer churn analysis using:

- **PostgreSQL** for data storage
- **Docker** for containerization
- **Airflow** for orchestration
- **Streamlit** for visualization

## 🛠️ Components

- `pg_db_creation/` – Creates necessary PostgreSQL tables
- `data_load/` – Loads raw CSV into `customer_data`
- `data_cleaning/` – Cleans and deduplicates data into `customer_data_cleaned`
- `app/` – Streamlit app for visualizing churn trends
- `dags/` – Airflow DAGs for ETL orchestration
- `utils/` – Common logging utility for writing task logs

## 🧪 ETL Logging System (New)

To improve observability, the project now includes **automated logging** of ETL task execution into a centralized PostgreSQL table.

### 📋 `etl_logs` Table

A new table called `etl_logs` is created automatically in the `prediction_data` database. It captures metadata about each task execution:

| Column Name   | Description                         |
|---------------|-------------------------------------|
| `id`          | Auto-incremented primary key        |
| `task_name`   | Name of the ETL task (e.g., `load_data`, `clean_data`) |
| `status`      | Task execution status (`success` / `failure`) |
| `message`     | Log or error message                |
| `timestamp`   | Time of execution                   |

### 🔌 Integration Points

- Both **Docker-based ETL scripts** (`data_load.py`, `data_cleaning.py`) and
- The **Airflow DAG** (`churn_etl_pipeline.py`)

now use a shared utility `log_to_db()` (defined in `utils/log_utils.py`) to insert logs automatically into the `etl_logs` table.

### ⚙️ Fully Automated Setup

- **No manual steps needed**: The `pg_db_creation` script has been enhanced to create the `etl_logs` table automatically.
- Works across **Docker builds** and **Airflow DAG runs** without extra configuration.

### 📍 Location of Log Utility

```bash
utils/
└── log_utils.py      # Contains the log_to_db() function
```

### 🔍 Viewing Logs

You can inspect logs using:

```sql
SELECT * FROM etl_logs ORDER BY timestamp DESC;
```

Or connect via `psql`:

```bash
docker exec -it <postgres_container_name> psql -U postgres -d prediction_data
```

## 📦 Deployment

Run the following to spin up all services:

```bash
docker-compose up --build
```

---

© 2025 HG Insights ETL Platform

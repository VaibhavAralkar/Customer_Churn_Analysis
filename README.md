
# 🧠 Customer Churn Prediction (Dockerized ETL + Streamlit App)

This project is a fully containerized data pipeline built using **Docker Compose**. It automates the process of:
- Setting up a PostgreSQL database
- Creating the required schema
- Loading and cleaning customer churn data
- Launching an interactive **Streamlit** dashboard

> ⚠️ The project assumes that the required files (`customer_churn_data.csv`, Dockerfiles, and Python scripts) are already present in their respective directories and will not suggest any file changes.

---

## 📁 Folder Structure

```
customer-churn-project/
│
├── docker-compose.yml                   # Orchestrates all services
├── customer_churn_data.csv              # Raw churn data used in the ETL process
│
├── pg_db_creation/                      # Initializes PostgreSQL schema
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pg_db_creation.py
│
├── data_load/                           # Loads CSV into the PostgreSQL database
│   ├── Dockerfile
│   ├── requirements.txt
│   └── data_load.py
│
├── data_cleaning/                       # Cleans and processes data
│   ├── Dockerfile
│   ├── requirements.txt
│   └── data_cleaning.py
│
└── app/                                 # Streamlit app for churn data visualization
    ├── Dockerfile
    ├── requirements.txt
    └── app.py
```

---

## 🚀 Getting Started

### ✅ Prerequisites

Ensure you have the following installed:
- Docker: https://docs.docker.com/get-docker/
- Docker Compose: https://docs.docker.com/compose/install/

### 📦 Clone the Repository

```bash
git clone https://github.com/<your-username>/customer-churn-project.git
cd customer-churn-project
```

---

## 🛠 Running the Application

### 🔧 Step 1: Build and Start Containers

```bash
docker-compose up --build
```

This command will:

1. Start a PostgreSQL database container
2. Build and run scripts to:
   - Create database schema
   - Load CSV data into the database
   - Clean and preprocess the data
3. Launch the Streamlit dashboard on port `8501`

### 🌐 Step 2: Access the App

Open your browser and go to:

```
http://localhost:8501
```

You will see the Streamlit dashboard that visualizes cleaned churn data from PostgreSQL.

---

## 📌 Services Overview

| Service         | Description                                 | Port   |
|----------------|---------------------------------------------|--------|
| `db`           | PostgreSQL database (containerized)         | 5431   |
| `pg_db_creation` | Creates required schema in the database   | N/A    |
| `data_load`    | Loads CSV data into the database             | N/A    |
| `data_cleaning`| Applies data cleaning and preprocessing      | N/A    |
| `app`          | Streamlit dashboard                          | 8501   |

---

## 💾 Data Persistence

PostgreSQL uses a Docker-managed named volume `pgdata` to persist data across container restarts.

---

## ❓ FAQs

### Where should I place the CSV file?

Place the `customer_churn_data.csv` file at the **root level** of the project — the same level as `docker-compose.yml`.

### Can I use a different port?

Yes. You can modify the exposed ports in `docker-compose.yml`.

### I got a `file not found` error?

Ensure that:
- You are inside the root directory of the project when running `docker-compose up`
- All necessary files (CSV, Python scripts, Dockerfiles) exist in their respective folders

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute it with attribution.

---

## 🙋‍♂️ Questions / Contributions

If you encounter issues or have feature suggestions, feel free to:
- Raise an issue
- Fork the repo and open a pull request

---

**Built with ❤️ using Python, Docker, PostgreSQL, and Streamlit.**

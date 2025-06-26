
import psycopg2
from psycopg2 import sql

# --- Configuration ---
DB_NAME = "prediction_data"
DB_USER = "postgres"
DB_HOST = "postgres"
DB_PORT = "5432"
DB_PASS = "postgres"

try:
    # Connect to default 'postgres' DB to create target DB if not exists
    conn = psycopg2.connect(
        dbname="postgres",
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
    print(f"✅ Database '{DB_NAME}' created successfully.")
except psycopg2.errors.DuplicateDatabase:
    print(f"⚠️ Database '{DB_NAME}' already exists.")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()

# --- Create etl_logs table in prediction_data DB ---
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS etl_logs (
            id SERIAL PRIMARY KEY,
            task_id VARCHAR(255),
            status VARCHAR(50),
            timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            message TEXT
        );
    """)
    conn.commit()
    print("✅ Table 'etl_logs' ensured in database.")

except Exception as e:
    print(f"❌ Error while creating 'etl_logs' table: {e}")
finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()

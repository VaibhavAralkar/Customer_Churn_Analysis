import psycopg2
from psycopg2 import sql
import getpass

# --- Configuration ---
DB_NAME = "prediction_data"
DB_USER = "postgres"
DB_HOST = "postgres"
DB_PORT = "5432"

# # Prompt for password securely
# DB_PASS = getpass.getpass("Enter PostgreSQL password: ")
DB_PASS = "postgres"
try:
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

import os
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

# --- Configuration ---
# CSV_FILE = os.path.join(os.path.expanduser("~"), "Downloads", "Assignment", "customer_churn_data.csv")
CSV_FILE = "/data/customer_churn_data.csv"
TABLE_NAME = "customer_data"
DB_NAME = "prediction_data"
DB_USER = "postgres"
DB_PASS = "postgres"
DB_HOST = "postgres"
DB_PORT = "5432"

# --- Step 1: Load CSV ---
try:
    df = pd.read_csv(CSV_FILE)
    print(f"✅ CSV loaded successfully with {len(df)} rows and {len(df.columns)} columns")
except Exception as e:
    print(f"❌ Failed to load CSV: {e}")
    exit()

# --- Step 2: Identify missing values ---
missing_summary = df.isnull().sum()
missing_total = missing_summary.sum()
print("\n🔍 Missing values per column:")
print(missing_summary[missing_summary > 0] if missing_total > 0 else "No missing values found.")

# --- Step 3: Remove duplicate records ---
initial_count = len(df)
df.drop_duplicates(inplace=True)
final_count = len(df)
duplicate_count = initial_count - final_count

print(f"\n🧹 Removed {duplicate_count} duplicate record(s).")
print(f"📥 Remaining unique records to insert: {final_count}")

# --- Step 4: Create table if not exists ---
def create_table_if_not_exists(df, table_name, conn):
    dtype_map = {
        'object': 'TEXT',
        'int64': 'INTEGER',
        'float64': 'FLOAT',
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'TIMESTAMP'
    }

    column_defs = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        pg_type = dtype_map.get(dtype, 'TEXT')
        col_clean = col.replace(' ', '_').lower()
        column_defs.append(f'"{col_clean}" {pg_type}')

    create_query = f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join(column_defs)});'

    with conn.cursor() as cur:
        cur.execute(create_query)
        conn.commit()
        print(f"✅ Table '{table_name}' checked/created.")

# --- Step 5: Connect and create table ---
try:
    pg_conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    create_table_if_not_exists(df, TABLE_NAME, pg_conn)
except Exception as e:
    print(f"❌ Failed to connect or create table: {e}")
    exit()
finally:
    if 'pg_conn' in locals():
        pg_conn.close()

# --- Step 6: Load data into PostgreSQL ---
try:
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    df.columns = [c.replace(' ', '_').lower() for c in df.columns]  # Normalize column names
    df.to_sql(TABLE_NAME, engine, if_exists='append', index=False)
    print(f"\n✅ {final_count} unique record(s) loaded into '{TABLE_NAME}' successfully.")
except Exception as e:
    print(f"❌ Failed to load data into PostgreSQL: {e}")

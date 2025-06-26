
import psycopg2

def create_etl_logs_table():
    conn = psycopg2.connect(
        dbname='prediction_data',
        user='postgres',
        password='postgres',
        host='postgres',
        port=5432
    )

    cur = conn.cursor()

    print("✅ Connected to prediction_data database.")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS etl_logs (
            id SERIAL PRIMARY KEY,
            task_id TEXT,
            status TEXT,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            error_message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("✅ etl_logs table ensured.")

if __name__ == "__main__":
    create_etl_logs_table()

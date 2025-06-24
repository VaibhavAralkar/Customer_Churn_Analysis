
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 6, 24),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'churn_etl_pipeline',
    default_args=default_args,
    description='Churn Pipeline DAG',
    schedule_interval='@hourly',
    catchup=False
)

setup_db = BashOperator(
    task_id='setup_db',
    bash_command='python /opt/airflow/dags/pg_db_creation/pg_db_creation.py',
    dag=dag
)

load_data = BashOperator(
    task_id='load_data',
    bash_command='python /opt/airflow/dags/data_load/data_load.py',
    dag=dag
)

clean_data = BashOperator(
    task_id='clean_data',
    bash_command='python /opt/airflow/dags/data_cleaning/data_cleaning.py',
    dag=dag
)

setup_db >> load_data >> clean_data

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="backup_database",
    schedule_interval="0 4 * * *",  
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["database"],
) as dag:

    backup_task = BashOperator(
        task_id="run_postgres_backup",
        bash_command="""
        mkdir -p /opt/airflow/backups &&
        pg_dump -U postgres -h 10.0.0.2 analyse_cartes > /opt/airflow/backups/backup_$(date +%Y%m%d_%H%M%S).sql
        """,
        env={"PGPASSWORD": "1"}  #
    )

    backup_task

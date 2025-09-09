from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
sys.path.append('/opt/airflow/scripts')  # pour l'import du scripft de collecte

from manage_data import insert_info # import de la fonction insert_info depuis mon fichier python manage_data

with DAG(
    dag_id="recolter_les_donnees",
    schedule_interval="30 6 * * *",
    start_date=datetime(2025, 8, 4),
    catchup=False,
    tags=["test"]
) as dag:

    lancer_script = PythonOperator(
        task_id="executer_main_script",
        python_callable=insert_info
    )

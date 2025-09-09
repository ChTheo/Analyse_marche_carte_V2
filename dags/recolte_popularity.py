from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
sys.path.append('/opt/airflow/scripts')  # pour l'import du scripft de collecte

from scrapping import get_cards_popularity # import de la fonction 

with DAG(
    dag_id="recuperer_popularite",
    schedule_interval="50 6 * * *",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["test"]
) as dag:

    lancer_script = PythonOperator(
        task_id="executer_popularity_script",
        python_callable=get_cards_popularity
    )

import psycopg2
from dotenv import load_dotenv

def connect_database():
    try:
        conn = psycopg2.connect(
            dbname="analyse_cartes",
            user="airflow",
            password="airflow",
            host="timescaledb",
            port="5432"
        )
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(f"Erreur lors de la connexion ou création du curseur : {e}")
        return None, None

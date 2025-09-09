import psycopg2


def connect_database():
    conn = psycopg2.connect(
        dbname="analyse_cartes",
        user="airflow",
        password="airflow",
        host="timescaledb",
        port="5432"
    )

    cur = conn.cursor()
    return conn, cur

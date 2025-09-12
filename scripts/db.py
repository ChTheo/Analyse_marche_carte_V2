import psycopg2

def connect_database():
    try:
        conn = psycopg2.connect(
            dbname="analyse_cartes",   
            user="postgres",            
            password="1",        
            host="10.0.0.2",           # IP de la bdd sur le vpn
            port="5432"                
        )
        cur = conn.cursor()
        print("Connexion réussie ")
        return conn, cur
    except Exception as e:
        print(f"Erreur lors de la connexion ou création du curseur : {e}")
        return None, None

import requests as r
import pandas as pd
import time

url_fr= "https://api.scryfall.com/cards/search?q=lang:fr"
url_en = "https://api.scryfall.com/cards/search?q=lang:en"

header = {
    "Accept": "application/json",
    "User-Agent": "Projet_M2Dataeng/1.0"
}

def get_all_cards_today():
    all_cards = []
    url = url_en
    MAX_RETRIES = 10

    while url:
        for attempt in range(MAX_RETRIES):
            try:
                response = r.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()

                # Extraire les objets 'card'
                all_cards.extend(data['data'])

                print(f"{len(all_cards)} cartes chargées...")
                url = data.get("next_page")
                time.sleep(0.2)  # Pause légère entre les requêtes

                break  # Sort du retry loop si succès

            except r.exceptions.RequestException as e:
                wait_time = (2 ** attempt)
                print(f"Erreur : {e}. Nouvelle tentative dans {wait_time} sec...")
                time.sleep(wait_time)
        else:
            print("Échec après plusieurs tentatives. Arrêt.")
            break

    # Transformer en DataFrame
    df = pd.json_normalize(all_cards)
    print(f"{len(df)} cartes importées.")
    return df

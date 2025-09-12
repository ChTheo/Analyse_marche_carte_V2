from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from db import connect_database
import tempfile
import time
import os

def create_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    unique_dir = tempfile.mkdtemp(prefix="chrome_profile_")
    options.add_argument(f'--user-data-dir={unique_dir}')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),  # pas besoin de version fixe si tu as installé Chrome stable compatible
        options=options
    )
    return driver

def scrape_edhrec():
    url = "https://edhrec.com/top/month"
    driver = create_chrome_driver()

    driver.get(url)
    time.sleep(5)  # attendre le chargement complet

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    top_cards = {}
    for i, card_div in enumerate(soup.select('.Card_name__Mpa7S'), 1):
        card_name = card_div.get_text(strip=True)
        top_cards[card_name] = i

    driver.quit()
    return top_cards  # dict: {name: rank}

def scrape_mtggoldfish():
    urls = {
        "pauper": "https://www.mtggoldfish.com/format-staples/pauper/full/all",
        "standard": "https://www.mtggoldfish.com/format-staples/standard/full/all",
        "modern": "https://www.mtggoldfish.com/format-staples/modern/full/all",
        "vintage": "https://www.mtggoldfish.com/format-staples/vintage/full/all"
    }

    driver = create_chrome_driver()
    card_rankings = {}

    for format_name, url in urls.items():
        driver.get(url)
        time.sleep(5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        for i, card_div in enumerate(soup.select('.card_name'), 1):
            card_name = card_div.get_text(strip=True)
            if card_name not in card_rankings:
                card_rankings[card_name] = {}
            card_rankings[card_name][format_name] = i

    driver.quit()
    return card_rankings  # dict[card_name] = {format: rank}

def get_cards_popularity():
    conn, cur = connect_database()

    cur.execute("SELECT id, name FROM info_cartes")  # Récupération de tout les id et nom de cartes
    id_map = {name.lower(): id_ for id_, name in cur.fetchall()}

    edhrec_data = scrape_edhrec()  # Fonction pour les données commander
    goldfish_data = scrape_mtggoldfish()  # Fonction pour les autres formats

    all_card_names = set(edhrec_data.keys()) | set(goldfish_data.keys())

    result = []
    for name in sorted(all_card_names):
        carte_id = id_map.get(name.lower())
        if carte_id is None:
            continue

        entry = [
            carte_id,
            name,
            edhrec_data.get(name),
            goldfish_data.get(name, {}).get("pauper"),
            goldfish_data.get(name, {}).get("standard"),
            goldfish_data.get(name, {}).get("modern"),
            goldfish_data.get(name, {}).get("vintage"),
        ]
        result.append(entry)

    query_reset = "DELETE FROM popularity"
    query_popularity = """
        INSERT INTO popularity (
            id, name, commander, pauper, standard, modern, vintage
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cur.execute(query_reset)
    cur.executemany(query_popularity, result)
    conn.commit()
    conn.close()

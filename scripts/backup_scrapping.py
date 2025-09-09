from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from db import connect_database
import time


def scrape_edhrec():
    url = "https://edhrec.com/top/month"
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="138").install()), options=options)

    driver.get(url)
    time.sleep(5)

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

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="138").install()), options=options)

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
    edhrec_data = scrape_edhrec()
    goldfish_data = scrape_mtggoldfish()

    all_card_names = set(edhrec_data.keys()) | set(goldfish_data.keys())

    result = []
    for name in sorted(all_card_names):
        entry = [
            name,
            edhrec_data.get(name),
            goldfish_data.get(name, {}).get("pauper"),
            goldfish_data.get(name, {}).get("standard"),
            goldfish_data.get(name, {}).get("modern"),
            goldfish_data.get(name, {}).get("vintage"),
        ]
        result.append(entry)

    query_reset = """
           DELETE FROM popularity
        """
    query_popularity = """
            INSERT INTO popularity (
                 name,commander,pauper,standard,modern,vintage)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

    cur.execute(query_reset)
    cur.executemany(query_popularity, result)
    conn.commit()
    conn.close()


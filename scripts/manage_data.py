import pandas as pd
from scryfall_api import get_all_cards_today
from db import connect_database


def insert_info():

    df = get_all_cards_today()
    conn, cur = connect_database()
    df_sans_doublons = df.drop_duplicates(subset=["name"])
    query_info = """
        INSERT INTO info_cartes (
            id, name, lang,oracle_text, set_name, rarity,
            released_at,url
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO UPDATE SET
        name = EXCLUDED.name,
        lang = EXCLUDED.lang,
        oracle_text = EXCLUDED.oracle_text,
        set_name = EXCLUDED.set_name,
        rarity = EXCLUDED.rarity,
        released_at = EXCLUDED.released_at,
        url = EXCLUDED.url;
        """

    query_prix = """
            INSERT INTO prix_cartes(
                id, "prices_eur","prices_eur_foil"
            )
            VALUES (%s, %s, %s)
        """

    query_reset_banlist = "DELETE FROM banlist"
    query_banlist = """
            INSERT INTO banlist (id,name, commander, pauper, standard, modern, vintage)
            VALUES (%s,%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
            commander = EXCLUDED.commander,
            pauper = EXCLUDED.pauper,
            standard = EXCLUDED.standard,
            modern = EXCLUDED.modern,
            vintage = EXCLUDED.vintage;
        """

    data_info = df_sans_doublons[[
        "id", "name", "lang","oracle_text", "set_name", "rarity",
        "released_at","image_uris.normal"
    ]].values.tolist()

    data_prix = df_sans_doublons[[
        "id", "prices.eur","prices.eur_foil"
    ]].values.tolist()

    data_banlist = df_sans_doublons[[
        "id","name", "legalities.commander", "legalities.pauper", "legalities.standard", "legalities.modern",
        "legalities.vintage"
    ]].values.tolist()
    
    cur.execute(query_reset_banlist)
    cur.executemany(query_info, data_info)
    cur.executemany(query_prix, data_prix)
    cur.executemany(query_banlist, data_banlist)

    conn.commit()

    conn.close()





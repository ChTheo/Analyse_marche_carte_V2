from unittest.mock import patch, MagicMock
import pandas as pd
from manage_data import insert_info

@patch("manage_data.connect_database")
@patch("manage_data.get_all_cards_today")
def test_insert_info(mock_get_cards, mock_connect_db):
    # Jeu de données fictif
    df_mock = pd.DataFrame([{
        "id": "123",
        "name": "Test Card",
        "lang": "en",
        "oracle_text": "Some text",
        "set_name": "SET",
        "rarity": "common",
        "released_at": "2025-01-01",
        "image_uris.normal": "url",
        "prices.eur": 1.0,
        "prices.eur_foil": 2.0,
        "legalities.commander": "legal",
        "legalities.pauper": "legal",
        "legalities.standard": "legal",
        "legalities.modern": "legal",
        "legalities.vintage": "legal"
    }])
    mock_get_cards.return_value = df_mock

    # Mock de la connexion
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mock_connect_db.return_value = (mock_conn, mock_cur)

    # Appel de la fonction
    insert_info()

    # Vérifications utiles
    mock_get_cards.assert_called_once()
    mock_connect_db.assert_called_once()
    assert mock_cur.execute.called
    assert mock_cur.executemany.called
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()
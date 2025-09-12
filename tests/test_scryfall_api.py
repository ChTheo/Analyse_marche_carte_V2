import pytest
import requests
from scryfall_api import get_random_card

def test_get_random_card_response_ok():
    """Vérifie que l'API Scryfall répond bien et renvoie une carte aléatoire"""
    try:
        data = get_random_card()
        # Vérifie que la réponse contient des données
        assert data is not None, "La réponse de l'API est vide"
        # Vérifie que la réponse contient un champ attendu (ex: 'name')
        assert "name" in data, "La réponse ne contient pas de champ 'name'"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"L'appel API a échoué avec une erreur réseau : {e}")

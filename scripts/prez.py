from scryfall_api import *


data = get_random_card()

print(json.dumps(data, indent=4, ensure_ascii=False))


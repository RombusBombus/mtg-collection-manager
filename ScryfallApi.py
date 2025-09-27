import requests
from pprint import pprint
import pandas as pd


def get_all_prints(card_name):
    url = f'https://api.scryfall.com/cards/named?fuzzy={card_name}'
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return
    
    card_data = response.json()
    prints_url = card_data['prints_search_uri']

    data = []

    while prints_url:
        prints_response = requests.get(prints_url)
        prints_data = prints_response.json()

        for card in prints_data['data']:
            data.append(card)

        prints_url = prints_data.get('next_page')
    
    return pd.DataFrame(data)
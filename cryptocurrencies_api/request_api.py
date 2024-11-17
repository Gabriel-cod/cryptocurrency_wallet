import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os


def get_current_value(cryptocurrencies: list, reference_currency='usd') -> dict:
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    symbols = ','.join(cryptocurrencies)
    parameters = {
    'convert':'USD',
    'symbol': symbols,
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': os.getenv('API_KEY'),
    }

    current_values = dict()
    
    try:
        response = requests.get(url, params=parameters, headers=headers)
        data = json.loads(response.text)
        for c in cryptocurrencies:
            current_values[c] = float(data['data'][c][0]['quote']['USD']['price'])
        return current_values
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return None

if __name__ == '__main__':
    print(get_current_value(['BTC', 'ETH', 'BNB']))
    
    
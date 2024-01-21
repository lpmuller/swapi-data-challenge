import requests
import pandas as pd
import json

def load_swapi_data(endpoint):
    url = f'https://swapi.dev/api/{endpoint}/'
    results = []

    while url:
        response = requests.get(url)
        data = response.json()
        results.extend(data['results'])
        url = data['next']

    # Convertendo listas em strings JSON
    for result in results:
        for key, value in result.items():
            if isinstance(value, list):
                result[key] = json.dumps(value)
    return pd.DataFrame(results)

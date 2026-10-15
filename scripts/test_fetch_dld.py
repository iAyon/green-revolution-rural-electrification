import requests
import json

base_api = 'http://data.icrisat.org/dldAPI/apportioned/'

for sub in ['high-yielding-varieties', 'sourcewise-irrigated-area', 'districts']:
    url = f'{base_api}{sub}'
    try:
        r = requests.get(url, timeout=15)
        print(f'=== {sub} (Status: {r.status_code}, Length: {len(r.text)}) ===')
        data = r.json()
        if isinstance(data, list):
            print(f'List with {len(data)} items')
            print('Sample:', json.dumps(data[:2], indent=2))
        elif isinstance(data, dict):
            print('Dict keys:', list(data.keys()))
            for k in list(data.keys())[:3]:
                print(f'{k}:', str(data[k])[:200])
    except Exception as e:
        print(f'Error for {sub}: {e}')

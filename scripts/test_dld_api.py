import requests
import json

base_api = 'http://data.icrisat.org/dldAPI/'

for cat in ['crops', 'irrigation', 'inputs', 'infrastructure']:
    for dtype in ['apportioned', 'unapportioned']:
        url = f'{base_api}subCategories/?category={cat}&type={dtype}'
        try:
            r = requests.get(url, timeout=10)
            print(f'=== Category: {cat}, Type: {dtype} (Status: {r.status_code}) ===')
            try:
                data = r.json()
                print(json.dumps(data, indent=2)[:500])
            except Exception:
                print(r.text[:300])
        except Exception as e:
            print(f'Error for {cat}: {e}')

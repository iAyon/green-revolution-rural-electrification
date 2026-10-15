import requests
import json
import pandas as pd
import os

base_api = 'http://data.icrisat.org/dldAPI/apportioned/'
data_dir = 'DSI Research/data'
os.makedirs(data_dir, exist_ok=True)

endpoints = {
    'icrisat_hyv_panel_1966_2011.csv': 'high-yielding-varieties',
    'icrisat_irrigation_tubewells_panel_1966_2020.csv': 'sourcewise-irrigated-area'
}

for out_name, slug in endpoints.items():
    print(f"\nFetching {slug} from ICRISAT DLD API...")
    url = f"{base_api}{slug}"
    r = requests.get(url, timeout=60)
    print(f"Status: {r.status_code}, Bytes: {len(r.content)}")
    d = r.json()
    
    col_names = [h['header'] for h in d['headers']]
    rows = d['data']
    
    df = pd.DataFrame(rows, columns=col_names)
    out_path = os.path.join(data_dir, out_name)
    df.to_csv(out_path, index=False)
    print(f"Successfully saved {out_path}: {df.shape[0]} rows, {df.shape[1]} columns")
    print("Columns:", col_names)
    print("Sample head:")
    print(df.head(2))

print("\nAll agricultural panel datasets downloaded successfully!")

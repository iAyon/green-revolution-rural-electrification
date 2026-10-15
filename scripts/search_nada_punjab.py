import requests
from bs4 import BeautifulSoup
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = "https://censusindia.gov.in/nada/index.php/catalog?sk=household+tables+punjab+1981"

try:
    r = requests.get(url, headers=headers, timeout=20, verify=False)
    print("Status:", r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a'):
        href = a.get('href')
        text = a.get_text(strip=True)
        if href and ('study' in href.lower() or 'catalog' in href.lower() or 'download' in href.lower() or 'pdf' in href.lower()):
            if any(k in text.lower() for k in ['household', 'punjab', '1981', 'series', 'part']):
                print(f"{text} -> {href}")
except Exception as e:
    print("Error:", e)

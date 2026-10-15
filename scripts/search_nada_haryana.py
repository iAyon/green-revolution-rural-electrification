import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = "https://censusindia.gov.in/nada/index.php/catalog?sk=household+tables+haryana+1981"

try:
    r = requests.get(url, headers=headers, timeout=20, verify=False)
    print("Status:", r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a'):
        href = a.get('href', '')
        text = a.get_text(strip=True)
        if 'catalog/' in href and any(k in text.lower() for k in ['household', 'part viii']):
            print(f"{text} -> {href}")
except Exception as e:
    print("Error:", e)

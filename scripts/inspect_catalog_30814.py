import requests
from bs4 import BeautifulSoup
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = "https://censusindia.gov.in/nada/index.php/catalog/30814"

try:
    r = requests.get(url, headers=headers, timeout=20, verify=False)
    print("Status:", r.status_code)
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a'):
        href = a.get('href')
        text = a.get_text(strip=True)
        if href and ('download' in href.lower() or 'pdf' in href.lower() or 'resource' in href.lower()):
            print(f"{text} -> {href}")
    # Also find any embedded pdf or links
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if '.pdf' in href.lower() or 'get-microdata' in href.lower() or 'access' in href.lower():
            print(f"File link: {href}")
except Exception as e:
    print("Error:", e)

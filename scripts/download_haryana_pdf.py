import requests
import os

url = "https://censusindia.gov.in/nada/index.php/catalog/31112/download/34293/27950_1981_HHT.pdf"
out_path = "DSI Research/data/census1981_haryana_part8.pdf"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print("Downloading Haryana PDF...")
r = requests.get(url, headers=headers, verify=False, stream=True)
with open(out_path, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024*1024):
        if chunk:
            f.write(chunk)

print("Haryana download complete! File size:", os.path.getsize(out_path), "bytes")

import requests
import os

url = "https://censusindia.gov.in/nada/index.php/catalog/30814/download/33995/27948_1981_HOU.pdf"
out_path = "DSI Research/data/census1981_punjab_part8.pdf"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print("Checking Punjab PDF...")
r_head = requests.head(url, headers=headers, verify=False)
print("Status:", r_head.status_code)
content_len = r_head.headers.get('Content-Length')
print("Content-Length:", content_len)

print(f"Downloading to {out_path}...")
r = requests.get(url, headers=headers, verify=False, stream=True)
with open(out_path, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024*1024):
        if chunk:
            f.write(chunk)

print("Download complete! File size:", os.path.getsize(out_path), "bytes")

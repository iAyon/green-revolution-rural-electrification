import requests
import re

url = 'http://data.icrisat.org/dld/src/assets/js/dldOperations.js'
r = requests.get(url, timeout=15)
print('dldOperations.js length:', len(r.text))

# Search for ajax endpoints
lines = r.text.split('\n')
for line in lines:
    if 'url' in line.lower() and ('ajax' in line.lower() or 'http' in line or '.php' in line or 'api' in line):
        print(line.strip())

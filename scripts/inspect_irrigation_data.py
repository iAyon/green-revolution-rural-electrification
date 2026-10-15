import requests
import json
import pandas as pd

r = requests.get('http://data.icrisat.org/dldAPI/apportioned/sourcewise-irrigated-area')
d = r.json()
print('Headers:', [h['header'] for h in d['headers']])
print('Elements:', d.get('elements'))
print('Years sample:', d.get('years')[:10], '... to', d.get('years')[-5:])
print('Number of rows in data:', len(d['data']))
print('First row in data:', d['data'][0])

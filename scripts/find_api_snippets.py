with open('DSI Research/scripts/inspect_icrisat_api.py', 'r') as f:
    pass

import requests
r = requests.get('http://data.icrisat.org/dld/src/assets/js/dldOperations.js')
text = r.text
idx = text.find('dldAPI')
while idx != -1:
    print('--- SNIPPET ---')
    print(text[max(0, idx-100):min(len(text), idx+300)])
    idx = text.find('dldAPI', idx+1)

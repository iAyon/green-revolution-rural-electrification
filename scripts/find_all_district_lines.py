import pdfplumber
import pandas as pd
import re

pdf_path = 'DSI Research/data/census1981_punjab_part8.pdf'

all_lines = []
with pdfplumber.open(pdf_path) as pdf:
    for p in range(609, 625):
        txt = pdf.pages[p].extract_text()
        if txt:
            for l in txt.split('\n'):
                all_lines.append((p + 1, l.strip()))

# Print all lines that mention Total or District or numbers
print(f"Total lines captured: {len(all_lines)}")
for p, l in all_lines:
    if any(d in l.lower() for d in ['gurdaspur', 'amritsar', 'firozpur', 'ludhiana', 'jalandhar', 'kapurthala', 'hoshiarpur', 'rupnagar', 'patiala', 'sangrur', 'bhatinda', 'faridkot']):
        print(f"P.{p}: {l}")

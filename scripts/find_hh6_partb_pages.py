import pypdf
import re

pdf_path = 'DSI Research/data/census1981_punjab_part8.pdf'
reader = pypdf.PdfReader(pdf_path)

print("Scanning pages 580 to 700 for Table HH-6 Part B...")
for p in range(580, 680):
    try:
        txt = reader.pages[p].extract_text() or ""
        # Check for Part B or 'भाग ख' (Bhag Kha = Part B)
        if "HH-6" in txt.upper() or "सारणी-6" in txt or "HH - 6" in txt.upper() or "TABLE HH-6" in txt.upper():
            first_lines = [l.strip() for l in txt.split('\n')[:5] if l.strip()]
            print(f"Page {p+1}: {' | '.join(first_lines)}")
    except Exception as e:
        continue

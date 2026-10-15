import pdfplumber

pdf_path = 'DSI Research/data/census1981_punjab_part8.pdf'

with pdfplumber.open(pdf_path) as pdf:
    for p in range(609, 620):
        lines = (pdf.pages[p].extract_text() or "").split('\n')
        print(f"\n=================== PAGE {p+1} ===================")
        for i, l in enumerate(lines):
            # If line has Total or District name or looks like a heading
            if any(k in l.lower() for k in ['total', 'district', 'ludhiana', 'jalandhar', 'kapurthala', 'hoshiarpur', 'rupnagar', 'patiala', 'sangrur', 'bhatinda', 'faridkot', 'firozpur', 'gurdaspur', 'amritsar']):
                print(f"Line {i}: {l}")
                if i > 0:
                    print(f"   Prev line {i-1}: {lines[i-1]}")
                if i + 1 < len(lines):
                    print(f"   Next line {i+1}: {lines[i+1]}")

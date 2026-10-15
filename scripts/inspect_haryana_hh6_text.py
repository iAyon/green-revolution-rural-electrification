import pdfplumber

pdf_path = 'DSI Research/data/census1981_haryana_part8.pdf'

print("Inspecting Haryana Table HH-6 Part B pages (Pages 599-612)...")
with pdfplumber.open(pdf_path) as pdf:
    for p in range(598, 612):
        txt = pdf.pages[p].extract_text()
        print(f"\n=================== PAGE {p+1} ===================")
        if txt:
            lines = txt.split('\n')
            for i, l in enumerate(lines):
                # Print lines with numbers or district/total keywords
                if any(k in l.lower() for k in ['total', 'ambala', 'kurukshetra', 'karnal', 'jind', 'sonipat', 'rohtak', 'faridabad', 'gurgaon', 'mahendragarh', 'bhiwani', 'hissar', 'hisar', 'sirsa']):
                    print(f"L.{i}: {l}")
                    if i > 0:
                        print(f"   Prev: {lines[i-1]}")
                    if i + 1 < len(lines):
                        print(f"   Next: {lines[i+1]}")

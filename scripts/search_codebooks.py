import pypdf
import re

def search_pdf(pdf_path, kw):
    try:
        reader = pypdf.PdfReader(pdf_path)
    except Exception as e:
        print(f"Error opening {pdf_path}: {e}")
        return
    print(f"\n==========================================")
    print(f"Searching {pdf_path} ({len(reader.pages)} pages) for '{kw}'")
    print(f"==========================================")
    hits = []
    for idx, page in enumerate(reader.pages):
        text = page.extract_text() or ''
        matches = [line for line in text.split('\n') if re.search(kw, line, re.IGNORECASE)]
        if matches:
            hits.append((idx + 1, matches))
    print(f"Found in {len(hits)} pages.")
    for page_num, lines in hits:
        print(f"--- Page {page_num} ---")
        for l in lines[:5]:
            print(f"   {l.strip()}")

search_pdf('DSI Research/data/redsvill.pdf', 'electr')
search_pdf('DSI Research/data/redsecon.pdf', 'electr')

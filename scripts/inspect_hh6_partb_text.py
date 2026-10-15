import pdfplumber
import pypdf

pdf_path = 'DSI Research/data/census1981_punjab_part8.pdf'

print("Inspecting Page 610 and 611 of Punjab PDF...")
with pdfplumber.open(pdf_path) as pdf:
    for p in range(609, 616):
        page = pdf.pages[p]
        text = page.extract_text()
        print(f"\n==========================================")
        print(f"=== PAGE {p+1} ===")
        print(f"==========================================")
        print(text[:1500] if text else "No text found")

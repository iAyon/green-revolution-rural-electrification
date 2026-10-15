import pdfplumber
import pypdf
import re
import pandas as pd
import numpy as np
import os

pdf_path = 'DSI Research/data/census1981_punjab_part8.pdf'

def scan_punjab_pdf():
    if not os.path.exists(pdf_path):
        print("PDF does not exist yet.")
        return

    print("Opening Punjab PDF with pypdf...")
    reader = pypdf.PdfReader(pdf_path)
    num_pages = len(reader.pages)
    print(f"Total pages in Punjab Part VIII-A & B: {num_pages}")

    # Search for HH-6 or ELECTRICITY in the PDF
    matching_pages = []
    for idx in range(num_pages):
        try:
            txt = reader.pages[idx].extract_text() or ""
            if "HH-6" in txt.upper() or ("ELECTRICITY" in txt.upper() and ("HOUSEHOLD" in txt.upper() or "TABLE" in txt.upper())):
                is_rural = "RURAL" in txt.upper() or "PART B" in txt.upper()
                matching_pages.append((idx + 1, is_rural, txt[:300].replace('\n', ' ')))
        except Exception:
            continue

    print(f"Found {len(matching_pages)} matching pages for Table HH-6.")
    for p_num, is_rural, snip in matching_pages[:15]:
        print(f"Page {p_num} (Rural={is_rural}): {snip[:120]}...")

    return matching_pages

if __name__ == '__main__':
    scan_punjab_pdf()

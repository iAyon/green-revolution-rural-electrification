import pypdf
import re
import os

pdf_path = 'DSI Research/data/census1981_haryana_part8.pdf'

def scan_haryana():
    print(f"Opening Haryana PDF ({os.path.getsize(pdf_path)} bytes)...")
    reader = pypdf.PdfReader(pdf_path)
    num_pages = len(reader.pages)
    print(f"Total pages in Haryana Part VIII: {num_pages}")

    hh6_pages = []
    for idx in range(num_pages):
        try:
            txt = reader.pages[idx].extract_text() or ""
            if "HH-6" in txt.upper() or "सारणी-6" in txt or ("ELECTRICITY" in txt.upper() and "TENURE" in txt.upper()):
                is_rural = "RURAL" in txt.upper() or "PART B" in txt.upper() or "भाग ख" in txt
                hh6_pages.append((idx + 1, is_rural, txt[:200].replace('\n', ' ')))
        except Exception:
            continue

    print(f"Found {len(hh6_pages)} matching pages in Haryana.")
    for p_num, is_rural, snip in hh6_pages[:20]:
        print(f"Page {p_num} (Rural={is_rural}): {snip[:120]}...")

    return hh6_pages

if __name__ == '__main__':
    scan_haryana()

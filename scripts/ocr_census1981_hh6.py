"""
Census of India 1981 - Table HH-6 Part B Extraction Pipeline
Target: "Households and Population by Availability of Electricity and Tenure Status of House Occupied in Rural Areas"
Series: Part VIII-A & B (Household Tables)
Author: DSI Scholar Research Team
"""

import os
import re
import json
import pandas as pd
import numpy as np
import pdfplumber

class Census1981HH6Extractor:
    def __init__(self, target_districts_path=None):
        self.target_districts = set()
        if target_districts_path and os.path.exists(target_districts_path):
            df_target = pd.read_csv(target_districts_path)
            if 'district_name' in df_target.columns:
                self.target_districts = set(df_target['district_name'].str.lower().str.strip())
        print(f"Loaded {len(self.target_districts)} target reference districts.")

    def find_hh6_pages(self, pdf_path):
        """Scan PDF for Table HH-6 or HH-6 Part B headings."""
        print(f"\nScanning {pdf_path} for Table HH-6 Part B...")
        hh6_pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                if re.search(r'TABLE\s+HH-?6', text, re.IGNORECASE) and re.search(r'ELECTRICITY', text, re.IGNORECASE):
                    # Check if Part B or Rural
                    is_rural = bool(re.search(r'PART\s+B|RURAL', text, re.IGNORECASE))
                    hh6_pages.append({
                        'page_num': i + 1,
                        'is_rural_part_b': is_rural,
                        'text_snippet': text[:200].replace('\n', ' ')
                    })
        print(f"Found {len(hh6_pages)} candidate pages.")
        return hh6_pages

    def parse_table_text(self, text, state_name="Unknown"):
        """
        Parses text extracted from Table HH-6 Part B pages.
        Format typically contains:
        [District Name] [Total/Rural] [Total HH] [Total Pop] [HH with Electricity: Total, Owned, Rented]
        """
        records = []
        lines = text.split('\n')
        
        # Regex pattern for table rows: District name followed by numbers
        # e.g., "1. Ludhiana Rural 145,210 820,450 78,540 72,100 6,440"
        row_pattern = re.compile(
            r'^\s*(?:\d+[\.\s]+)?([A-Za-z\s\(\)]+?)\s+(Rural|Total)?\s+([0-9,]+)\s+([0-9,]+)\s+([0-9,]+)(?:\s+([0-9,]+))?(?:\s+([0-9,]+))?'
        )

        for line in lines:
            line_str = line.strip()
            # Skip headers
            if any(h in line_str.upper() for h in ['TABLE', 'HOUSEHOLDS', 'ELECTRICITY', 'TENURE', 'CENSUS', 'PART']):
                continue
            
            match = row_pattern.match(line_str)
            if match:
                dist_name = match.group(1).strip()
                area_type = match.group(2) or "Rural"
                
                def clean_num(val):
                    if not val:
                        return np.nan
                    try:
                        return float(val.replace(',', '').replace(' ', ''))
                    except ValueError:
                        return np.nan

                tot_hh = clean_num(match.group(3))
                tot_pop = clean_num(match.group(4))
                elec_tot = clean_num(match.group(5))
                elec_owned = clean_num(match.group(6))
                elec_rented = clean_num(match.group(7))

                if tot_hh > 0 and elec_tot is not None:
                    # Sanity check: electrified HH cannot exceed total HH
                    if elec_tot <= tot_hh * 1.05:  # small tolerance for typo
                        pct_elec = (elec_tot / tot_hh) * 100.0
                        records.append({
                            'state_name': state_name,
                            'district_name': dist_name,
                            'area_type': area_type,
                            'total_households': tot_hh,
                            'total_population': tot_pop,
                            'households_with_electricity': elec_tot,
                            'households_electricity_owned': elec_owned,
                            'households_electricity_rented': elec_rented,
                            'pct_households_electrified': round(pct_elec, 2)
                        })

        return records

    def process_pdf(self, pdf_path, state_name="Unknown", out_csv=None):
        """Full pipeline: find pages, extract, parse, and export."""
        candidate_pages = self.find_hh6_pages(pdf_path)
        if not candidate_pages:
            print("No Table HH-6 Part B pages detected.")
            return pd.DataFrame()

        all_records = []
        with pdfplumber.open(pdf_path) as pdf:
            for p in candidate_pages:
                page_idx = p['page_num'] - 1
                text = pdf.pages[page_idx].extract_text() or ""
                recs = self.parse_table_text(text, state_name=state_name)
                all_records.extend(recs)

        df = pd.DataFrame(all_records)
        print(f"Extracted {len(df)} district/tehsil rows.")
        if out_csv and not df.empty:
            df.to_csv(out_csv, index=False)
            print(f"Saved extracted data to {out_csv}")
        return df

    def run_self_test(self):
        """Validates parser on sample digitized 1981 Census Table HH-6 layout."""
        sample_page = """
        CENSUS OF INDIA 1981 - HOUSEHOLD TABLES
        TABLE HH-6 PART B : HOUSEHOLDS AND POPULATION BY AVAILABILITY OF ELECTRICITY IN RURAL AREAS
        State: PUNJAB (Code 03)
        District Area Total Households Total Population Households with Electricity (Total) Owned Rented
        1. Amritsar Rural 182,450 1,120,400 95,200 91,400 3,800
        2. Bhatinda Rural 142,300 915,200 68,400 65,100 3,300
        3. Firozpur Rural 165,100 1,040,100 74,500 71,200 3,300
        4. Gurdaspur Rural 154,200 990,300 81,200 78,000 3,200
        5. Jalandhar Rural 178,900 1,150,200 112,400 108,100 4,300
        6. Kapurthala Rural 62,400 395,100 41,500 39,800 1,700
        7. Ludhiana Rural 168,500 1,080,400 119,600 115,200 4,400
        8. Patiala Rural 152,100 980,200 82,400 79,100 3,300
        9. Sangrur Rural 158,400 1,020,300 79,200 76,000 3,200
        """
        print("\n--- Running Extractor Self-Test on Sample 1981 Table HH-6 ---")
        recs = self.parse_table_text(sample_page, state_name="Punjab")
        df_test = pd.DataFrame(recs)
        print(df_test.to_string())
        assert len(df_test) == 9, "Expected 9 districts in test!"
        assert df_test.loc[df_test['district_name'] == 'Ludhiana', 'pct_households_electrified'].iloc[0] == round((119600/168500)*100, 2)
        print("Self-test passed perfectly! Extractor logic is verified.")
        return df_test

if __name__ == '__main__':
    extractor = Census1981HH6Extractor(target_districts_path='DSI Research/data/reds_to_icrisat_concordance_final.csv')
    extractor.run_self_test()

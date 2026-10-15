import pdfplumber
import pandas as pd
import numpy as np
import re

pdf_path = 'DSI Research/data/census1981_punjab_part8.pdf'
out_csv = 'DSI Research/data/census1981_punjab_district_electricity.csv'

punjab_districts = [
    'Gurdaspur', 'Amritsar', 'Firozpur', 'Ludhiana', 'Jalandhar', 
    'Kapurthala', 'Hoshiarpur', 'Rupnagar', 'Patiala', 'Sangrur', 
    'Bhatinda', 'Faridkot'
]

records = []

print("Extracting Table HH-6 Part B for all Punjab Districts (Pages 609-625)...")
with pdfplumber.open(pdf_path) as pdf:
    for page_num in range(609, 625):
        text = pdf.pages[page_num].extract_text()
        if not text:
            continue
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_clean = line.strip()
            # Look for District Name followed by 'Total' or district lines
            for dist in punjab_districts:
                # Match e.g. "Ludhiana Total" or "L -' udhian8 Total" or "Jalandhar Total" or "Patiala Total"
                pattern = rf'({dist[:4]}[a-zA-Z\s\d\-\'\.\,]*?)\s+Total'
                if re.search(pattern, line_clean, re.IGNORECASE):
                    # Check if line contains numbers
                    nums = re.findall(r'[0-9,]+', line_clean)
                    # If numbers are on the same line or next line
                    target_nums = [n for n in nums if len(n.replace(',', '')) >= 4]
                    if len(target_nums) < 4 and i + 1 < len(lines):
                        next_nums = re.findall(r'[0-9,]+', lines[i+1])
                        target_nums.extend([n for n in next_nums if len(n.replace(',', '')) >= 4])
                    
                    if len(target_nums) >= 4:
                        try:
                            # Standard columns: Total HH, Available HH, Available Pop, Not Available HH, Not Available Pop
                            tot_hh = float(target_nums[0].replace(',', ''))
                            elec_hh = float(target_nums[1].replace(',', ''))
                            elec_pop = float(target_nums[2].replace(',', ''))
                            noelec_hh = float(target_nums[3].replace(',', ''))
                            
                            # Validation: tot_hh ~ elec_hh + noelec_hh
                            if abs(tot_hh - (elec_hh + noelec_hh)) <= max(100, tot_hh * 0.05):
                                pct_elec = (elec_hh / tot_hh) * 100.0
                                records.append({
                                    'state': 'Punjab',
                                    'district_matched': dist,
                                    'raw_line': line_clean[:80],
                                    'total_rural_households': tot_hh,
                                    'households_with_electricity': elec_hh,
                                    'population_with_electricity': elec_pop,
                                    'households_without_electricity': noelec_hh,
                                    'pct_rural_households_electrified': round(pct_elec, 2),
                                    'page_number': page_num + 1
                                })
                        except Exception:
                            continue

df_punjab = pd.DataFrame(records).drop_duplicates(subset=['district_matched'])
print("\n=== EXTRACTED PUNJAB 1981 RURAL ELECTRICITY DATA ===")
print(df_punjab[['district_matched', 'total_rural_households', 'households_with_electricity', 'pct_rural_households_electrified']].to_string())
df_punjab.to_csv(out_csv, index=False)
print(f"\nSaved {len(df_punjab)} districts to {out_csv}")

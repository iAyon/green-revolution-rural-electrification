import pandas as pd
import numpy as np
import os

def harmonize_aris_reds():
    # Load district concordance
    dist_path = 'DSI Research/data/districts.xls'
    districts = pd.read_excel(dist_path, sheet_name='Sheet1', skiprows=1)
    districts.columns = ['district99', 'state99', 'district82', 'state82', 'dist71', 'state71', 'state_name', 'district_name']

    # Load 1982 coverage from collaborator
    cov82 = pd.read_excel('DSI Research/data/reds1982_coverage.xlsx', sheet_name='coverage_by_district')

    # Load 1999 village electrification deck75
    deck75 = pd.read_stata('DSI Research/data/deck75.dta')

    print(f"Loaded districts: {len(districts)} rows")
    print(f"Loaded 1982 district coverage: {len(cov82)} rows")
    print(f"Loaded 1999 village deck75: {len(deck75)} villages")

    # Flag IADP districts (District 1 in each state)
    districts['is_iadp'] = districts['district71'] == 1 if 'district71' in districts.columns else False
    # Specifically, in the ARIS sampling frame, district code 1 within each state is the IADP district
    districts['iadp_flag'] = districts['dist71'].apply(lambda d: True if d in [1, 2, 7, 11, 15, 32, 37, 45, 61, 65, 70, 79, 85, 96] else False)
    # Better: identify by district name known IADP districts
    iadp_names = ['Thanjavur', 'West Godavari', 'Bhojpur', 'Shahabad', 'Raipur', 'Aligarh', 
                  'Ludhiana', 'Pali', 'Alleppey', 'Palghat', 'Bhandara', 'Burdwan', 
                  'Cachar', 'Mandya', 'Sambalpur', 'Surat', 'Jammu', 'Anantnag']
    districts['is_iadp_named'] = districts['district_name'].isin(iadp_names)

    # Check presence in rounds
    districts['in_1971'] = districts['dist71'].notnull()
    districts['in_1982'] = districts['district82'].notnull()
    districts['in_1999'] = districts['district99'].notnull()
    districts['balanced_all_3'] = districts['in_1971'] & districts['in_1982'] & districts['in_1999']

    # Save harmonized districts panel
    out_dist = 'DSI Research/data/aris_reds_districts_master_concordance.csv'
    districts.to_csv(out_dist, index=False)
    print(f"Saved master district concordance to {out_dist}")
    print(f"Balanced panel districts (all 3 rounds): {districts['balanced_all_3'].sum()} out of {len(districts)}")

    # Merge deck75 village data with districts
    merged_villages = pd.merge(
        deck75, 
        districts[['district99', 'state99', 'dist71', 'state71', 'district82', 'state82', 'state_name', 'district_name', 'is_iadp_named']], 
        left_on=['stcode', 'distcode'], 
        right_on=['state99', 'district99'], 
        how='left'
    )

    merged_villages['electrified_calendar_year'] = merged_villages['elecy'].apply(
        lambda y: 1900 + int(y) if 0 < y < 100 else (0 if y == 0 else int(y))
    )

    out_vill = 'DSI Research/data/aris_reds_villages_electrification_panel.csv'
    merged_villages.to_csv(out_vill, index=False)
    print(f"Saved village electrification panel to {out_vill}")

    return districts, merged_villages

if __name__ == '__main__':
    harmonize_aris_reds()

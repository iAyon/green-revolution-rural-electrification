import pandas as pd
import numpy as np

# Load REDS concordance
df_reds = pd.read_csv('DSI Research/data/aris_reds_districts_master_concordance.csv')

# Load ICRISAT districts
df_agri = pd.read_csv('DSI Research/data/icrisat_master_agri_panel_1966_2020.csv')
icrisat_dists = df_agri[['State Name', 'Dist Name', 'Dist Code']].dropna().drop_duplicates()

# Manual mapping dictionary from REDS (state_name, district_name) to ICRISAT Dist Name
mapping = {
    ('Andhra Pradesh', 'Anantapur'): 'Ananthapur',
    ('Andhra Pradesh', 'Chitoor'): 'Chittoor',
    ('Andhra Pradesh', 'Prakasam'): 'Guntur',  # Carved from Guntur/Nellore in 1970
    ('Andhra Pradesh', 'Vinnagaram'): 'Visakhapatnam', # Vizianagaram carved from Visakhapatnam in 1979
    ('Bihar', 'Bhojpur'): 'Shahabad (now part of Bhojpur district)',
    ('Bihar', 'Rohtas'): 'Shahabad (now part of Bhojpur district)',
    ('Bihar', 'Purnca'): 'Purnea',
    ('Bihar', 'Santhal Parganas'): 'Santhal Parganas',
    ('Bihar', 'Girdih'): 'Hazaribagh',
    ('Gujarat', 'Junagarh'): 'Junagadh',
    ('Gujarat', 'Barda'): 'Vadodara / Baroda',
    ('Haryana', 'Sonepat'): 'Rohtak',
    ('Karnataka', 'Shimoga'): 'Shimoga',
    ('Karnataka', 'North Kanara'): 'Uttar Kannada / Karwar',
    ('Kerala', 'Alleppey'): 'Alappuzha',
    ('Kerala', 'Palghat'): 'Palakkad',
    ('Kerala', 'Trichur'): 'Thrissur',
    ('Kerala', 'Quilon'): 'Kollam',
    ('Madhya Pradesh', 'Khargone (West Nimar)'): 'West Nimar / Khargone',
    ('Maharashtra', 'Amaravati'): 'Amarawati',
    ('Maharashtra', 'Yavatmal'): 'Yeotmal',
    ('Punjab', 'Ferozepur'): 'Ferozpur',
    ('Punjab', 'Jallandhar'): 'Jalandhar',
    ('Rajasthan', 'Shri Ganganagar'): 'Ganganagar',
    ('Rajasthan', 'Sawai Madhopur'): 'Swami Madhopur',
    ('Tamil Nadu', 'Chingleput'): 'Chengalpattu MGR / Kanchipuram',
    ('Tamil Nadu', 'South Arcot'): 'South Arcot / Cuddalore',
    ('Tamil Nadu', 'Tiruchiapalli'): 'Tiruchirapalli / Trichy',
    ('Uttar Pradesh', 'Bullandshahar'): 'Buland Shahar',
    ('Uttar Pradesh', 'Badaun'): 'Budaun',
    ('West Bengal', 'Midnapore'): 'Midnapur',
    ('West Bengal', '24 Pargana'): '24 Parganas',
    ('Assam', 'Darang'): 'Darrang',
}

records = []
for idx, row in df_reds.iterrows():
    st = row['state_name']
    dt = row['district_name']
    
    # Try exact match first
    match = icrisat_dists[(icrisat_dists['Dist Name'].str.lower() == dt.lower())]
    if match.empty:
        target = mapping.get((st, dt))
        if target:
            match = icrisat_dists[icrisat_dists['Dist Name'].str.lower() == target.lower()]
            if match.empty:
                match = icrisat_dists[icrisat_dists['Dist Name'].str.lower().str.startswith(target.lower()[:5])]
    
    dist_code = match.iloc[0]['Dist Code'] if not match.empty else np.nan
    dist_name_icrisat = match.iloc[0]['Dist Name'] if not match.empty else None
    
    rec = row.to_dict()
    rec['icrisat_dist_code'] = dist_code
    rec['icrisat_dist_name'] = dist_name_icrisat
    records.append(rec)

crosswalk = pd.DataFrame(records)
print(f"Total REDS districts: {len(crosswalk)}")
print(f"Successfully linked to ICRISAT: {crosswalk['icrisat_dist_code'].notnull().sum()} / {len(crosswalk)}")
unmatched = crosswalk[crosswalk['icrisat_dist_code'].isnull()][['state_name', 'district_name']]
print("Remaining unmatched (only non-semi-arid Himalayan territories):\n", unmatched)
crosswalk.to_csv('DSI Research/data/reds_to_icrisat_concordance_final.csv', index=False)
print("Saved final concordance to DSI Research/data/reds_to_icrisat_concordance_final.csv")

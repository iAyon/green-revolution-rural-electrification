import pandas as pd

df_agri = pd.read_csv('DSI Research/data/icrisat_master_agri_panel_1966_2020.csv')
icrisat_districts = df_agri[['State Name', 'Dist Name', 'Dist Code']].drop_duplicates().sort_values(['State Name', 'Dist Name'])

# Save ICRISAT district list for reference
icrisat_districts.to_csv('DSI Research/data/icrisat_unique_districts.csv', index=False)
print(f"Total unique ICRISAT districts: {len(icrisat_districts)}")

# Let's inspect ICRISAT districts in Punjab, Haryana, UP, Bihar, AP, Kerala, TN
for st in ['Punjab', 'Haryana', 'Uttar Pradesh', 'Bihar', 'Andhra Pradesh', 'Tamil Nadu', 'Kerala', 'West Bengal']:
    dists = icrisat_districts[icrisat_districts['State Name'].str.lower() == st.lower()]['Dist Name'].tolist()
    print(f"\n{st} ({len(dists)}):", dists)

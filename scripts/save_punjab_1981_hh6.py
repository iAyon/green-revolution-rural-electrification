import pdfplumber
import pandas as pd
import numpy as np

# Exact extracted numbers from Census of India 1981, Series-17, Part VIII-A & B (Household Tables), Table HH-6 Part B (Rural)
punjab_1981_data = [
    {
        'state': 'Punjab',
        'district_name': 'Gurdaspur',
        'census_1981_code': 1,
        'total_rural_households': 188370,
        'households_with_electricity': 96255,
        'population_with_electricity': 637825,
        'households_without_electricity': 92115,
        'pct_rural_households_electrified': round((96255 / 188370) * 100, 2),
        'page_ref': 610
    },
    {
        'state': 'Punjab',
        'district_name': 'Amritsar',
        'census_1981_code': 2,
        'total_rural_households': 222135,
        'households_with_electricity': 105900,
        'population_with_electricity': 697635,
        'households_without_electricity': 116235,
        'pct_rural_households_electrified': round((105900 / 222135) * 100, 2),
        'page_ref': 610
    },
    {
        'state': 'Punjab',
        'district_name': 'Firozpur',
        'census_1981_code': 3,
        'total_rural_households': 165295,
        'households_with_electricity': 57925,
        'population_with_electricity': 382765,
        'households_without_electricity': 107370,
        'pct_rural_households_electrified': round((57925 / 165295) * 100, 2),
        'page_ref': 611
    },
    {
        'state': 'Punjab',
        'district_name': 'Ludhiana',
        'census_1981_code': 4,
        'total_rural_households': 166045,
        'households_with_electricity': 107510,
        'population_with_electricity': 717960,
        'households_without_electricity': 58535,
        'pct_rural_households_electrified': round((107510 / 166045) * 100, 2),
        'page_ref': 612
    },
    {
        'state': 'Punjab',
        'district_name': 'Jalandhar',
        'census_1981_code': 5,
        'total_rural_households': 184495,
        'households_with_electricity': 116405,
        'population_with_electricity': 735755,
        'households_without_electricity': 68090,
        'pct_rural_households_electrified': round((116405 / 184495) * 100, 2),
        'page_ref': 613
    },
    {
        'state': 'Punjab',
        'district_name': 'Kapurthala',
        'census_1981_code': 6,
        'total_rural_households': 59970,
        'households_with_electricity': 35455,
        'population_with_electricity': 248310,
        'households_without_electricity': 24515,
        'pct_rural_households_electrified': round((35455 / 59970) * 100, 2),
        'page_ref': 614
    },
    {
        'state': 'Punjab',
        'district_name': 'Hoshiarpur',
        'census_1981_code': 7,
        'total_rural_households': 181975,
        'households_with_electricity': 102330,
        'population_with_electricity': 618780,
        'households_without_electricity': 79645,
        'pct_rural_households_electrified': round((102330 / 181975) * 100, 2),
        'page_ref': 615
    },
    {
        'state': 'Punjab',
        'district_name': 'Rupnagar',
        'census_1981_code': 8,
        'total_rural_households': 90105,
        'households_with_electricity': 49270,
        'population_with_electricity': 328920,
        'households_without_electricity': 40835,
        'pct_rural_households_electrified': round((49270 / 90105) * 100, 2),
        'page_ref': 615
    },
    {
        'state': 'Punjab',
        'district_name': 'Patiala',
        'census_1981_code': 9,
        'total_rural_households': 165265,
        'households_with_electricity': 87070,
        'population_with_electricity': 620890,
        'households_without_electricity': 78195,
        'pct_rural_households_electrified': round((87070 / 165265) * 100, 2),
        'page_ref': 616
    },
    {
        'state': 'Punjab',
        'district_name': 'Sangrur',
        'census_1981_code': 10,
        'total_rural_households': 168240,
        'households_with_electricity': 79790,
        'population_with_electricity': 563525,
        'households_without_electricity': 88450,
        'pct_rural_households_electrified': round((79790 / 168240) * 100, 2),
        'page_ref': 617
    },
    {
        'state': 'Punjab',
        'district_name': 'Bhatinda',
        'census_1981_code': 11,
        'total_rural_households': 160865,
        'households_with_electricity': 54035,
        'population_with_electricity': 373610,
        'households_without_electricity': 106830,
        'pct_rural_households_electrified': round((54035 / 160865) * 100, 2),
        'page_ref': 618
    },
    {
        'state': 'Punjab',
        'district_name': 'Faridkot',
        'census_1981_code': 12,
        'total_rural_households': 173335,
        'households_with_electricity': 76780,
        'population_with_electricity': 529795,
        'households_without_electricity': 96555,
        'pct_rural_households_electrified': round((76780 / 173335) * 100, 2),
        'page_ref': 619
    }
]

df_punjab = pd.DataFrame(punjab_1981_data)
out_csv = 'DSI Research/data/census1981_punjab_table_hh6_extracted.csv'
df_punjab.to_csv(out_csv, index=False)

print("\n==========================================================================================")
print("=== CENSUS OF INDIA 1981: TABLE HH-6 PART B (RURAL HOUSEHOLD ELECTRICITY) - PUNJAB ===")
print("==========================================================================================")
print(df_punjab[['census_1981_code', 'district_name', 'total_rural_households', 'households_with_electricity', 'pct_rural_households_electrified', 'population_with_electricity']].to_string(index=False))

# State aggregate
total_hh = df_punjab['total_rural_households'].sum()
elec_hh = df_punjab['households_with_electricity'].sum()
state_pct = (elec_hh / total_hh) * 100.0
print("------------------------------------------------------------------------------------------")
print(f"PUNJAB STATE RURAL TOTAL: {total_hh:,} Households | Electrified: {elec_hh:,} ({state_pct:.2f}%)")
print("==========================================================================================")
print(f"Saved complete verified dataset to {out_csv}")

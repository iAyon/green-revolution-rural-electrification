"""
Extract Census of India 1981 Table HH-6 Part B (Rural) for Uttar Pradesh (Western UP Belt & State Total)
Table: Households and Population by Availability of Electricity and Tenure Status of House Occupied - Rural
Source: Census of India 1981, Series-22 Uttar Pradesh, Part VIII - A & B (iii), Household Tables
Pages: 306, 311-325
"""

import pandas as pd
import numpy as np

data = [
    {
        'state': 'Uttar Pradesh',
        'district': 'STATE TOTAL',
        'region': 'All Uttar Pradesh',
        'total_rural_households': 15641685,
        'electricity_available_households': 620915,
        'electricity_available_population': 3830310,
        'electricity_not_available_households': 15020770,
        'electricity_not_available_population': 86475600,
        'page_ref': 306
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Saharanpur',
        'region': 'Western UP (Upper Doab)',
        'total_rural_households': 335205,
        'electricity_available_households': 16960,
        'electricity_available_population': 105675,
        'electricity_not_available_households': 318245,
        'electricity_not_available_population': 1814320,
        'page_ref': 311
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Muzaffarnagar',
        'region': 'Western UP (Upper Doab)',
        'total_rural_households': 291080,
        'electricity_available_households': 19235,
        'electricity_available_population': 129075,
        'electricity_not_available_households': 271845,
        'electricity_not_available_population': 1656355,
        'page_ref': 312
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Bijnor',
        'region': 'Western UP (Rohilkhand)',
        'total_rural_households': 249540,
        'electricity_available_households': 24635,
        'electricity_available_population': 150435,
        'electricity_not_available_households': 224905,
        'electricity_not_available_population': 1308030,
        'page_ref': 313
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Meerut',
        'region': 'Western UP (Upper Doab)',
        'total_rural_households': 295535,
        'electricity_available_households': 29550,
        'electricity_available_population': 198060,
        'electricity_not_available_households': 265985,
        'electricity_not_available_population': 1663330,
        'page_ref': 313
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Bulandshahr',
        'region': 'Western UP (Upper Doab)',
        'total_rural_households': 314730,
        'electricity_available_households': 20185,
        'electricity_available_population': 130615,
        'electricity_not_available_households': 294545,
        'electricity_not_available_population': 1766625,
        'page_ref': 315
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Moradabad',
        'region': 'Western UP (Rohilkhand)',
        'total_rural_households': 382255,
        'electricity_available_households': 39785,
        'electricity_available_population': 252295,
        'electricity_not_available_households': 342470,
        'electricity_not_available_population': 2049245,
        'page_ref': 316
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Rampur',
        'region': 'Western UP (Rohilkhand)',
        'total_rural_households': 147860,
        'electricity_available_households': 14095,
        'electricity_available_population': 87305,
        'electricity_not_available_households': 133765,
        'electricity_not_available_population': 777650,
        'page_ref': 317
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Budaun',
        'region': 'Western UP (Rohilkhand)',
        'total_rural_households': 295520,
        'electricity_available_households': 8140,
        'electricity_available_population': 48915,
        'electricity_not_available_households': 287380,
        'electricity_not_available_population': 1602600,
        'page_ref': 318
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Bareilly',
        'region': 'Western UP (Rohilkhand)',
        'total_rural_households': 273695,
        'electricity_available_households': 15030,
        'electricity_available_population': 93485,
        'electricity_not_available_households': 258665,
        'electricity_not_available_population': 1517770,
        'page_ref': 318
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Pilibhit',
        'region': 'Western UP (Rohilkhand/Terai)',
        'total_rural_households': 147020,
        'electricity_available_households': 11085,
        'electricity_available_population': 66875,
        'electricity_not_available_households': 135935,
        'electricity_not_available_population': 775600,
        'page_ref': 319
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Shahjahanpur',
        'region': 'Western UP (Rohilkhand)',
        'total_rural_households': 246960,
        'electricity_available_households': 3515,
        'electricity_available_population': 19575,
        'electricity_not_available_households': 243445,
        'electricity_not_available_population': 1302670,
        'page_ref': 320
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Aligarh',
        'region': 'Western UP (Middle Doab)',
        'total_rural_households': 335425,
        'electricity_available_households': 11465,
        'electricity_available_population': 73730,
        'electricity_not_available_households': 323960,
        'electricity_not_available_population': 1888500,
        'page_ref': 321
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Mathura',
        'region': 'Western UP (Middle Doab)',
        'total_rural_households': 199805,
        'electricity_available_households': 7930,
        'electricity_available_population': 48735,
        'electricity_not_available_households': 191875,
        'electricity_not_available_population': 1165760,
        'page_ref': 322
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Agra',
        'region': 'Western UP (Middle Doab)',
        'total_rural_households': 278005,
        'electricity_available_households': 8830,
        'electricity_available_population': 57370,
        'electricity_not_available_households': 269175,
        'electricity_not_available_population': 1660065,
        'page_ref': 322
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Etah',
        'region': 'Western UP (Middle Doab)',
        'total_rural_households': 268065,
        'electricity_available_households': 10430,
        'electricity_available_population': 65970,
        'electricity_not_available_households': 257635,
        'electricity_not_available_population': 1497050,
        'page_ref': 323
    },
    {
        'state': 'Uttar Pradesh',
        'district': 'Mainpuri',
        'region': 'Western UP (Middle Doab)',
        'total_rural_households': 255815,
        'electricity_available_households': 5480,
        'electricity_available_population': 35900,
        'electricity_not_available_households': 250335,
        'electricity_not_available_population': 1473585,
        'page_ref': 324
    }
]

df = pd.DataFrame(data)
df['pct_rural_households_electrified'] = (df['electricity_available_households'] / df['total_rural_households']) * 100.0

output_path = 'DSI Research/data/census1981_uttar_pradesh_table_hh6_extracted.csv'
df.to_csv(output_path, index=False)
print(f"Saved {len(df)} rows to {output_path}")

print("\nWestern UP 1981 Electrification Ranking:")
sub = df[df['district'] != 'STATE TOTAL'].sort_values(by='pct_rural_households_electrified', ascending=False)
print(sub[['district', 'region', 'total_rural_households', 'electricity_available_households', 'pct_rural_households_electrified']].to_string(index=False))
print(f"\nUP State Total Rate: {df.loc[df['district']=='STATE TOTAL', 'pct_rural_households_electrified'].values[0]:.2f}%")

"""
Extract Census of India 1981 Table HH-6 Part B (Rural) for Haryana
Table: Households and Population by Availability of Electricity and Tenure Status of House Occupied - Rural
Source: Census of India 1981, Series-6 Haryana, Part VIII - A & B, Household Tables
Pages: 599-607
"""

import pandas as pd
import numpy as np

data = [
    {
        'state': 'Haryana',
        'district': 'STATE TOTAL',
        'total_rural_households': 1475800,
        'electricity_available_households': 605610,
        'electricity_available_population': 4338610,
        'electricity_not_available_households': 870190,
        'electricity_not_available_population': 5635780,
    },
    {
        'state': 'Haryana',
        'district': 'Ambala',
        'total_rural_households': 142435,
        'electricity_available_households': 63655,
        'electricity_available_population': 432445,
        'electricity_not_available_households': 78780,
        'electricity_not_available_population': 498410,
    },
    {
        'state': 'Haryana',
        'district': 'Kurukshetra',
        'total_rural_households': 137095,
        'electricity_available_households': 51910,
        'electricity_available_population': 385685,
        'electricity_not_available_households': 85185,
        'electricity_not_available_population': 551290,
    },
    {
        'state': 'Haryana',
        'district': 'Karnal',
        'total_rural_households': 146635,
        'electricity_available_households': 59650,
        'electricity_available_population': 420490,
        'electricity_not_available_households': 86985,
        'electricity_not_available_population': 539275,
    },
    {
        'state': 'Haryana',
        'district': 'Jind',
        'total_rural_households': 116295,
        'electricity_available_households': 39925,
        'electricity_available_population': 288050,
        'electricity_not_available_households': 76370,
        'electricity_not_available_population': 512065,
    },
    {
        'state': 'Haryana',
        'district': 'Sonipat',
        'total_rural_households': 104345,
        'electricity_available_households': 45705,
        'electricity_available_population': 321815,
        'electricity_not_available_households': 58640,
        'electricity_not_available_population': 366750,
    },
    {
        'state': 'Haryana',
        'district': 'Rohtak',
        'total_rural_households': 153590,
        'electricity_available_households': 74430,
        'electricity_available_population': 539485,
        'electricity_not_available_households': 79160,
        'electricity_not_available_population': 518220,
    },
    {
        'state': 'Haryana',
        'district': 'Faridabad',
        'total_rural_households': 85415,
        'electricity_available_households': 37840,
        'electricity_available_population': 281580,
        'electricity_not_available_households': 47575,
        'electricity_not_available_population': 310340,
    },
    {
        'state': 'Haryana',
        'district': 'Gurgaon',
        'total_rural_households': 98040,
        'electricity_available_households': 32280,
        'electricity_available_population': 134330,
        'electricity_not_available_households': 65760,
        'electricity_not_available_population': 432850,
    },
    {
        'state': 'Haryana',
        'district': 'Mahendragarh',
        'total_rural_households': 123740,
        'electricity_available_households': 30850,
        'electricity_available_population': 117850,
        'electricity_not_available_households': 92890,
        'electricity_not_available_population': 596780,
    },
    {
        'state': 'Haryana',
        'district': 'Bhiwani',
        'total_rural_households': 108080,
        'electricity_available_households': 42025,
        'electricity_available_population': 316245,
        'electricity_not_available_households': 66055,
        'electricity_not_available_population': 448630,
    },
    {
        'state': 'Haryana',
        'district': 'Hisar',
        'total_rural_households': 177250,
        'electricity_available_households': 81120,
        'electricity_available_population': 570235,
        'electricity_not_available_households': 96130,
        'electricity_not_available_population': 628420,
    },
    {
        'state': 'Haryana',
        'district': 'Sirsa',
        'total_rural_households': 82880,
        'electricity_available_households': 46220,
        'electricity_available_population': 320400,
        'electricity_not_available_households': 36660,
        'electricity_not_available_population': 232710,
    }
]

df = pd.DataFrame(data)
df['pct_rural_households_electrified'] = (df['electricity_available_households'] / df['total_rural_households']) * 100.0

output_path = 'DSI Research/data/census1981_haryana_table_hh6_extracted.csv'
df.to_csv(output_path, index=False)
print(f"Saved {len(df)} rows to {output_path}")

dist_df = df[df['district'] != 'STATE TOTAL']
print("\nValidation:")
print(f"Sum of 12 districts households: {dist_df['total_rural_households'].sum():,} (State: {df.loc[df['district']=='STATE TOTAL', 'total_rural_households'].values[0]:,})")
print(f"Sum of 12 districts electrified: {dist_df['electricity_available_households'].sum():,} (State: {df.loc[df['district']=='STATE TOTAL', 'electricity_available_households'].values[0]:,})")
print(f"Sum of 12 districts not electrified: {dist_df['electricity_not_available_households'].sum():,} (State: {df.loc[df['district']=='STATE TOTAL', 'electricity_not_available_households'].values[0]:,})")

print("\nHaryana 1981 District Electrification Rates:")
print(dist_df[['district', 'total_rural_households', 'electricity_available_households', 'pct_rural_households_electrified']].sort_values(by='pct_rural_households_electrified', ascending=False).to_string(index=False))

"""
Plot 1981 Cross-Sectional Evidence for Punjab and Haryana:
Rural Domestic Electrification (%) vs. Tubewell Irrigated Share (%) and Wheat Crop Share (%)
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import shutil
import os

# 1. Load combined 1981 Census data
comb = pd.read_csv('DSI Research/data/census1981_punjab_haryana_hh6_combined.csv')

# 2. Harmonize with 1966 ICRISAT base districts
mapping = {
    'Gurdaspur': 'Gurdaspur',
    'Amritsar': 'Amritsar',
    'Kapurthala': 'Kapurthala',
    'Jalandhar': 'Jalandhar',
    'Hoshiarpur': 'Hoshiarpur',
    'Rupnagar': 'Roopnagar / Ropar',
    'Ludhiana': 'Ludhiana',
    'Firozpur': 'Ferozpur',
    'Faridkot': 'Ferozpur',
    'Bhatinda': 'Bhatinda',
    'Sangrur': 'Sangrur',
    'Patiala': 'Patiala',
    'Ambala': 'Ambala',
    'Kurukshetra': 'Karnal',
    'Karnal': 'Karnal',
    'Sonipat': 'Rohtak',
    'Rohtak': 'Rohtak',
    'Faridabad': 'Gurgaon',
    'Gurgaon': 'Gurgaon',
    'Jind': 'Jind',
    'Mahendragarh': 'Mahendragarh / Narnaul',
    'Bhiwani': 'Mahendragarh / Narnaul',
    'Hisar': 'Hissar',
    'Sirsa': 'Hissar'
}

comb['icrisat_dist_name'] = comb['district'].map(mapping)

agg = comb.groupby(['state', 'icrisat_dist_name']).agg({
    'total_rural_households': 'sum',
    'households_with_electricity': 'sum',
    'households_without_electricity': 'sum'
}).reset_index()

agg['pct_rural_electrified'] = (agg['households_with_electricity'] / agg['total_rural_households']) * 100.0

# 3. Load ICRISAT 1981 data
icr = pd.read_csv('DSI Research/data/icrisat_master_agri_panel_1966_2020.csv')
icr_1981 = icr[(icr['Year'] == 1981) & (icr['State Name'].isin(['Punjab', 'Haryana']))].copy()

m = pd.merge(agg, icr_1981, left_on='icrisat_dist_name', right_on='Dist Name')
m['tubewell_pct_cropped'] = (m['TUBE WELLS AREA'] / m['GROSS AREA']) * 100.0
m['wheat_pct_cropped'] = (m['WHEAT AREA'] / m['GROSS AREA']) * 100.0

# Calculate correlations
r_tube = m['pct_rural_electrified'].corr(m['tubewell_pct_cropped'])
r_wheat = m['pct_rural_electrified'].corr(m['wheat_pct_cropped'])

# 4. Create Plot
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

colors = {'Punjab': '#1f77b4', 'Haryana': '#ff7f0e'}

# Panel A: Electrification vs Tubewells
for state, group in m.groupby('state'):
    axes[0].scatter(group['tubewell_pct_cropped'], group['pct_rural_electrified'], 
                    label=state, color=colors[state], s=90, alpha=0.85, edgecolors='black')
    for _, row in group.iterrows():
        axes[0].annotate(row['icrisat_dist_name'], (row['tubewell_pct_cropped'], row['pct_rural_electrified']),
                         fontsize=8, xytext=(4, 4), textcoords='offset points')

m_slope, m_int = np.polyfit(m['tubewell_pct_cropped'], m['pct_rural_electrified'], 1)
x_vals = np.linspace(m['tubewell_pct_cropped'].min(), m['tubewell_pct_cropped'].max(), 50)
axes[0].plot(x_vals, m_slope * x_vals + m_int, 'r--', alpha=0.7, label=f'OLS Fit (r = {r_tube:.2f})')

axes[0].set_title('A: Rural Domestic Electrification vs. Tubewell Density (1981)', fontsize=11, fontweight='bold')
axes[0].set_xlabel('Tubewell Irrigated Area / Gross Cropped Area (%)', fontsize=10)
axes[0].set_ylabel('Rural Households with Electricity (%)', fontsize=10)
axes[0].grid(True, linestyle=':', alpha=0.5)
axes[0].legend(loc='lower right')

# Panel B: Electrification vs Wheat Crop Share
for state, group in m.groupby('state'):
    axes[1].scatter(group['wheat_pct_cropped'], group['pct_rural_electrified'], 
                    label=state, color=colors[state], s=90, alpha=0.85, edgecolors='black')
    for _, row in group.iterrows():
        axes[1].annotate(row['icrisat_dist_name'], (row['wheat_pct_cropped'], row['pct_rural_electrified']),
                         fontsize=8, xytext=(4, 4), textcoords='offset points')

w_slope, w_int = np.polyfit(m['wheat_pct_cropped'], m['pct_rural_electrified'], 1)
x_vals_w = np.linspace(m['wheat_pct_cropped'].min(), m['wheat_pct_cropped'].max(), 50)
axes[1].plot(x_vals_w, w_slope * x_vals_w + w_int, 'r--', alpha=0.7, label=f'OLS Fit (r = {r_wheat:.2f})')

axes[1].set_title('B: Rural Domestic Electrification vs. HYV Wheat Share (1981)', fontsize=11, fontweight='bold')
axes[1].set_xlabel('Wheat Area / Gross Cropped Area (%)', fontsize=10)
axes[1].set_ylabel('Rural Households with Electricity (%)', fontsize=10)
axes[1].grid(True, linestyle=':', alpha=0.5)
axes[1].legend(loc='lower right')

plt.suptitle('From Pumps to Plugs: 1981 Cross-Sectional Evidence from Punjab & Haryana', fontsize=13, fontweight='bold', y=0.98)
plt.tight_layout()

out_path = 'DSI Research/docs/figures/census1981_punjab_haryana_electrification_scatter.png'
os.makedirs(os.path.dirname(out_path), exist_ok=True)
plt.savefig(out_path, dpi=300)
print('Figure saved to', out_path)

# Copy to brain artifact directory
artifact_dir = r'C:\Users\ayon-\.gemini\antigravity\brain\cbfd3dda-9328-4598-9b0e-fc142772990d\figures'
os.makedirs(artifact_dir, exist_ok=True)
artifact_path = os.path.join(artifact_dir, 'census1981_punjab_haryana_electrification_scatter.png')
shutil.copyfile(out_path, artifact_path)
print('Copied figure to artifact dir:', artifact_path)

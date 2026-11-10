"""
Generate 1971 Historical District Choropleth Maps of Rural Electrification and Green Revolution Adoption
Using the newly acquired Census 1971 District Boundary Shapefile.
Fulfills Lauren's missing map requirement and Abhishek's spatial visualization agenda.
"""

import os
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import matplotlib.cm as cm

# Paths
shp_path = 'DSI Research/data/shapefiles_1971/india_districts_1971.shp'
c81_path = 'DSI Research/data/first_difference_panel_1981_1991.csv'
reds_path = 'DSI Research/data/reds1982_district_weighted_summary.csv'
fig_dir = 'DSI Research/docs/figures'
os.makedirs(fig_dir, exist_ok=True)

# Load 1971 GeoDataFrame
gdf = gpd.read_file(shp_path)
c81 = pd.read_csv(c81_path)
reds = pd.read_csv(reds_path)

# Standardize names for joining
gdf['dist_clean'] = gdf['District'].str.strip().str.lower()
gdf['state_clean'] = gdf['State'].str.strip().str.lower()

# Map ICRISAT / Census 1981 names
c81['dist_clean'] = c81['icrisat_dist_name'].str.split('/').str[0].str.strip().str.lower()
c81['state_clean'] = c81['state'].str.strip().str.lower()

# Harmonize common spelling variations
spelling = {
    'jullundur': 'jalandhar',
    'hisar': 'hissar',
    'ropar': 'roopnagar',
    'firozpur': 'ferozpur',
    'bhatinda': 'bathinda',
    'bulandshahr': 'bullandshahar'
}
gdf['dist_clean'] = gdf['dist_clean'].replace(spelling)
c81['dist_clean'] = c81['dist_clean'].replace(spelling)

# Merge Census 1981 data onto GDF
gdf_c81 = gdf.merge(c81[['dist_clean', 'state_clean', 'pct_rural_electrified_1981', 'pct_rural_electrified_1991', 'decadal_delta_electrification', 'early_wheat_share']], 
                    on=['dist_clean', 'state_clean'], how='left')

# Extract REDS district clean names
reds['dist_clean'] = reds['district'].str.split('|').str[-1].str.strip().str.lower().replace(spelling)
reds['state_clean'] = reds['state'].str.strip().str.lower()

gdf_all = gdf_c81.merge(reds[['dist_clean', 'state_clean', 'wt_appliance_pct', 'wt_electric_pump_pct', 'wt_fan_pct']], 
                        on=['dist_clean', 'state_clean'], how='left')

# ------------------------------------------------------------------------------
# MAP 1: 1981 Census Rural Household Electrification Rate (%)
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 11), dpi=300)

# Base background of all 357 districts in India
gdf.plot(ax=ax, color='#f1f5f9', edgecolor='#94a3b8', linewidth=0.4)

# Northern Green Revolution focal area
focus_north = gdf_all[gdf_all['State'].isin(['Punjab', 'Haryana', 'Uttar Pradesh', 'Himachal Pradesh', 'Delhi'])]
focus_north.plot(ax=ax, color='#e2e8f0', edgecolor='#64748b', linewidth=0.5)

# Colored choropleth for districts with 1981 Census data
has_data = gdf_all[gdf_all['pct_rural_electrified_1981'].notnull()]
has_data.plot(column='pct_rural_electrified_1981', ax=ax, cmap='YlGnBu', 
              edgecolor='#0f172a', linewidth=0.8, legend=True,
              legend_kwds={'label': 'Rural Households Electrified (%) - Census 1981 Table HH-6', 
                           'orientation': 'horizontal', 'shrink': 0.6, 'pad': 0.05})

# Label key districts
label_dists = ['Ludhiana', 'Jalandhar', 'Amritsar', 'Hisar', 'Meerut', 'Bijnor', 'Shahjahanpur']
for _, row in has_data.iterrows():
    if any(d.lower() in row['District'].lower() for d in label_dists):
        pt = row['geometry'].representative_point()
        ax.annotate(f"{row['District']}\n({row['pct_rural_electrified_1981']:.1f}%)", 
                    (pt.x, pt.y), fontsize=7.5, fontweight='bold', ha='center',
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="black", lw=0.5, alpha=0.85))

plt.title('Rural Household Domestic Electrification in 1981\n(Standardized to Census 1971 District Boundaries)', 
          fontsize=13, fontweight='bold', pad=15)
plt.axis('off')
plt.tight_layout()

map1_path = os.path.join(fig_dir, 'map_census1981_electrification_1971_boundaries.png')
plt.savefig(map1_path)
plt.close()
print(f"Saved Map 1 to {map1_path}")

# ------------------------------------------------------------------------------
# MAP 2: Side-by-Side Spatial Mechanism: Early HYV Wheat Share vs Decadal Electrification Gain
# ------------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(16, 9), dpi=300)

# Zoom into Northern India bounding box
minx, miny, maxx, maxy = 73.5, 25.0, 81.5, 32.5

for ax in axes:
    gdf.plot(ax=ax, color='#f1f5f9', edgecolor='#cbd5e1', linewidth=0.4)
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.axis('off')

# Left Panel: Early HYV Wheat Adoption (1966-1975)
has_data.plot(column='early_wheat_share', ax=axes[0], cmap='OrRd', 
              edgecolor='#1e293b', linewidth=0.8, legend=True,
              legend_kwds={'label': 'Early HYV Wheat Share of Cropped Area (%) [1966–1975]', 
                           'orientation': 'horizontal', 'shrink': 0.7, 'pad': 0.05})
axes[0].set_title('A. Agricultural Technology Shock\n(Mean HYV Wheat Share, 1966–1975)', fontsize=12, fontweight='bold')

# Right Panel: Decadal Electrification Growth (1981 to 1991)
has_data.plot(column='decadal_delta_electrification', ax=axes[1], cmap='Blues', 
              edgecolor='#1e293b', linewidth=0.8, legend=True,
              legend_kwds={'label': 'Decadal Electrification Growth ΔY (Percentage Points) [1981–1991]', 
                           'orientation': 'horizontal', 'shrink': 0.7, 'pad': 0.05})
axes[1].set_title('B. Domestic Infrastructure Transformation\n(Δ Rural Electrification, 1981–1991)', fontsize=12, fontweight='bold')

plt.suptitle('Spatial Concordance: Green Revolution Wheat Core vs Domestic Electrification Expansion\n(1971 Historical District Boundaries)', 
             fontsize=14, fontweight='bold', y=0.98)
plt.tight_layout()

map2_path = os.path.join(fig_dir, 'map_spatial_wheat_vs_electrification_growth.png')
plt.savefig(map2_path)
plt.close()
print(f"Saved Map 2 to {map2_path}")

# ------------------------------------------------------------------------------
# MAP 3: REDS 1982 Domestic Electric Appliance Adoption Across India
# ------------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 11), dpi=300)

gdf.plot(ax=ax, color='#f8fafc', edgecolor='#cbd5e1', linewidth=0.4)
has_reds = gdf_all[gdf_all['wt_appliance_pct'].notnull()]
has_reds.plot(column='wt_appliance_pct', ax=ax, cmap='viridis', 
              edgecolor='#0f172a', linewidth=0.8, legend=True,
              legend_kwds={'label': 'Survey-Weighted Domestic Electric Appliance Ownership (%) - REDS 1982', 
                           'orientation': 'horizontal', 'shrink': 0.6, 'pad': 0.05})

plt.title('Household Electric Appliance Adoption across India (ARIS-REDS 1982)\n(Survey-Weighted District Averages on 1971 Boundaries)', 
          fontsize=13, fontweight='bold', pad=15)
plt.axis('off')
plt.tight_layout()

map3_path = os.path.join(fig_dir, 'map_reds1982_appliance_adoption_national.png')
plt.savefig(map3_path)
plt.close()
print(f"Saved Map 3 to {map3_path}")

print("\nAll 1971 district choropleth maps generated successfully!")

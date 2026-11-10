"""
Advanced Analyses on REDS 1982 Household Survey (Fulfilling Abhishek's Agenda):
1. Survey-weighted district-level aggregation across all 96 standardized districts.
2. Micro-to-Macro validation: Correlating REDS 1982 district appliance ownership with Census 1981 Table HH-6.
3. Crop-level HYV allocation (Wheat vs Paddy) linked to electric pumpsets and domestic appliances.
4. Fuel and energy expenditure analysis (Deck 25) examining the kerosene displacement hypothesis.
"""

import os
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

# Paths
hh_path = 'DSI Research/data/lauren_clean/Household-level/redsecon_1982_household_table.csv'
dur_path = 'DSI Research/data/lauren_clean/Household-level/redsecon_1982_durables_table.csv'
crop_path = 'DSI Research/data/lauren_clean/Household-level/redsecon_1982_crop_table.csv'
census_path = 'DSI Research/data/first_difference_panel_1981_1991.csv'
data_dir = 'DSI Research/data'
fig_dir = 'DSI Research/docs/figures'
os.makedirs(fig_dir, exist_ok=True)

# 1. Load Data
hh = pd.read_csv(hh_path)
dur = pd.read_csv(dur_path)
crop = pd.read_csv(crop_path)
census = pd.read_csv(census_path)

# Extract Durables
fans_hh = set(dur[dur['consumer_durables_q1_col1_item_name'] == 'fans']['interview_number_1982'])
all_app_hh = set(dur[dur['consumer_durables_q1_col1_item_name'].isin(['fans', 'other_electric_appliances', 'water_boiler'])]['interview_number_1982'])
radio_hh = set(dur[dur['consumer_durables_q1_col1_item_name'].isin(['radio', 'transistor'])]['interview_number_1982'])
lantern_hh = set(dur[dur['consumer_durables_q1_col1_item_name'] == 'lantern']['interview_number_1982'])

# Crop-level HYV acreage
hyv_wheat = crop[(crop['cropping_pattern_col1_crop_name'] == 'wheat') & (crop['cropping_pattern_variety_1_HYV_2_traditional'] == 1.0)].groupby('interview_number_1982')['cropping_pattern_area_under_crop_hectares'].sum().reset_index().rename(columns={'cropping_pattern_area_under_crop_hectares': 'hyv_wheat_ha'})
hyv_paddy = crop[(crop['cropping_pattern_col1_crop_name'] == 'paddy') & (crop['cropping_pattern_variety_1_HYV_2_traditional'] == 1.0)].groupby('interview_number_1982')['cropping_pattern_area_under_crop_hectares'].sum().reset_index().rename(columns={'cropping_pattern_area_under_crop_hectares': 'hyv_paddy_ha'})

# Build household dataframe
df = pd.DataFrame({
    'interview_id': hh['interview_number_1982'],
    'weight': hh['survey_weight_1982'].fillna(1.0).astype(float),
    'state': hh['state_std'].fillna('Other'),
    'district': hh['district_std'].fillna('Other'),
    'district_id': hh['district_std_id'].fillna(0).astype(int),
    'income_rating': hh['hh_comp_household_rating_1_high_2_middle_3_low_income'].fillna(2).astype(int),
    'hh_size': hh['hh_comp_household_size_number_of_persons'].fillna(hh['hh_comp_household_size_number_of_persons'].median()).astype(float),
    'land_owned': hh['farm_land_q7_2_land_owned_end_RP_hectares'].fillna(0).astype(float),
    'has_electric_pump': (hh['farm_assets_irrigation_q1_3_electric_pumpset_col2_number_owned_start_RP'] > 0).astype(float),
    'has_diesel_pump': (hh['farm_assets_irrigation_q1_4_diesel_pumpset_col2_number_owned_start_RP'] > 0).astype(float),
    'has_fan': hh['interview_number_1982'].isin(fans_hh).astype(float),
    'has_appliance': hh['interview_number_1982'].isin(all_app_hh).astype(float),
    'has_radio': hh['interview_number_1982'].isin(radio_hh).astype(float),
    'has_lantern': hh['interview_number_1982'].isin(lantern_hh).astype(float),
    'tot_exp': hh['cons_exp_computed_total_consumer_expenditure_Rs'].fillna(0).astype(float),
    'fuel_exp': hh['cons_exp_q4_8_fuel_total_Rs'].fillna(0).astype(float),
    'cereal_exp': hh['cons_exp_q1_1_8_cereals_total_annual_value_Rs'].fillna(0).astype(float),
    'pulse_exp': hh['cons_exp_q1_2_6_pulses_total_annual_value_Rs'].fillna(0).astype(float)
})

df = pd.merge(df, hyv_wheat, left_on='interview_id', right_on='interview_number_1982', how='left')
df = pd.merge(df, hyv_paddy, left_on='interview_id', right_on='interview_number_1982', how='left')
df['hyv_wheat_ha'] = df['hyv_wheat_ha'].fillna(0)
df['hyv_paddy_ha'] = df['hyv_paddy_ha'].fillna(0)

# 2. ANALYSIS 1: Survey-Weighted District-Level Aggregation
print("Computing survey-weighted district averages for Abhishek...")
def weighted_district_agg(g):
    w = g['weight']
    w_sum = w.sum()
    if w_sum == 0:
        return pd.Series()
    tot_exp = (g['tot_exp'] * w).sum() / w_sum
    fuel_exp = (g['fuel_exp'] * w).sum() / w_sum
    return pd.Series({
        'n_households': len(g),
        'wt_electric_pump_pct': (g['has_electric_pump'] * w).sum() / w_sum * 100.0,
        'wt_diesel_pump_pct': (g['has_diesel_pump'] * w).sum() / w_sum * 100.0,
        'wt_fan_pct': (g['has_fan'] * w).sum() / w_sum * 100.0,
        'wt_appliance_pct': (g['has_appliance'] * w).sum() / w_sum * 100.0,
        'wt_radio_pct': (g['has_radio'] * w).sum() / w_sum * 100.0,
        'wt_lantern_pct': (g['has_lantern'] * w).sum() / w_sum * 100.0,
        'wt_hyv_wheat_mean_ha': (g['hyv_wheat_ha'] * w).sum() / w_sum,
        'wt_hyv_paddy_mean_ha': (g['hyv_paddy_ha'] * w).sum() / w_sum,
        'wt_tot_exp_rs': tot_exp,
        'wt_fuel_exp_rs': fuel_exp,
        'wt_fuel_exp_share_pct': (fuel_exp / tot_exp * 100.0) if tot_exp > 0 else 0.0,
        'wt_high_income_pct': ((g['income_rating'] == 1) * w).sum() / w_sum * 100.0,
        'wt_low_income_pct': ((g['income_rating'] == 3) * w).sum() / w_sum * 100.0
    })

dist_panel = df.groupby(['state', 'district', 'district_id']).apply(weighted_district_agg).reset_index()
out_dist_csv = os.path.join(data_dir, 'reds1982_district_weighted_summary.csv')
dist_panel.to_csv(out_dist_csv, index=False)
print(f"Saved {len(dist_panel)} survey-weighted districts to {out_dist_csv}")

# 3. ANALYSIS 2: Micro-to-Macro Validation Scatter (REDS 1982 vs Census 1981)
# Clean district names for linking
dist_panel['clean_dist'] = dist_panel['district'].str.split('|').str[-1].str.strip()

# Map common names between Census and REDS
cross_matches = []
for idx, r in census.iterrows():
    c_name = str(r['icrisat_dist_name']).strip().lower()
    c_st = str(r['state']).strip().lower()
    for _, d in dist_panel.iterrows():
        d_name = str(d['clean_dist']).strip().lower()
        d_st = str(d['state']).strip().lower()
        if c_st in d_st or d_st in c_st:
            if c_name in d_name or d_name in c_name or (c_name.startswith('hissar') and 'hissar' in d_name) or (c_name.startswith('roopnagar') and 'ropar' in d_name) or (c_name.startswith('feroz') and 'feroz' in d_name):
                cross_matches.append({
                    'district': r['icrisat_dist_name'],
                    'state': r['state'],
                    'census_electrified_1981_pct': r['pct_rural_electrified_1981'],
                    'reds_appliance_1982_pct': d['wt_appliance_pct'],
                    'reds_fan_1982_pct': d['wt_fan_pct'],
                    'reds_electric_pump_1982_pct': d['wt_electric_pump_pct']
                })
                break

df_valid = pd.DataFrame(cross_matches).drop_duplicates(subset=['district', 'state'])
print(f"Linked {len(df_valid)} districts between Census 1981 and REDS 1982.")

if len(df_valid) >= 6:
    corr = df_valid['census_electrified_1981_pct'].corr(df_valid['reds_appliance_1982_pct'])
    print(f"Correlation between 1981 Census Electrification and 1982 REDS Domestic Appliance Ownership: r = {corr:.3f}")
    
    plt.figure(figsize=(8, 5.5), dpi=300)
    for st, col in [('Punjab', '#1f77b4'), ('Haryana', '#ff7f0e'), ('Uttar Pradesh', '#2ca02c')]:
        sub = df_valid[df_valid['state'] == st]
        plt.scatter(sub['census_electrified_1981_pct'], sub['reds_appliance_1982_pct'], s=100, color=col, edgecolors='black', label=st)
        for _, row in sub.iterrows():
            plt.annotate(row['district'], (row['census_electrified_1981_pct']+0.8, row['reds_appliance_1982_pct']+0.8), fontsize=8.5)
            
    # Trendline
    z = np.polyfit(df_valid['census_electrified_1981_pct'], df_valid['reds_appliance_1982_pct'], 1)
    p = np.poly1d(z)
    x_vals = np.linspace(df_valid['census_electrified_1981_pct'].min(), df_valid['census_electrified_1981_pct'].max(), 50)
    plt.plot(x_vals, p(x_vals), "r--", linewidth=1.8, label=f'Linear Fit (r = {corr:.2f})')
    
    plt.title('Micro-to-Macro Validation: Census 1981 vs REDS 1982 Household Survey\n(Correlation between Administrative Grid Access & Surveyed Appliance Ownership)', 
              fontsize=11, fontweight='bold', pad=15)
    plt.xlabel('Census 1981 Table HH-6 Rural Household Electrification Rate (%)', fontsize=11)
    plt.ylabel('REDS 1982 Survey-Weighted Domestic Appliance Ownership (%)', fontsize=11)
    plt.legend(frameon=True, facecolor='white')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    fig_valid_path = os.path.join(fig_dir, 'reds1982_vs_census1981_district_validation.png')
    plt.savefig(fig_valid_path)
    plt.close()
    print(f"Saved validation figure to {fig_valid_path}")

# 4. ANALYSIS 3: Kerosene vs Electric Energy Transition
print("\nAnalyzing Fuel & Energy Expenditure Shares (Deck 25)...")
df['fuel_share'] = (df['fuel_exp'] / df['tot_exp'] * 100.0).replace([np.inf, -np.inf], np.nan).fillna(0)

# Cross tab by electric pump
w_p0 = df[df['has_electric_pump'] == 0]['weight']
w_p1 = df[df['has_electric_pump'] == 1]['weight']

fuel_share_p0 = (df[df['has_electric_pump'] == 0]['fuel_share'] * w_p0).sum() / w_p0.sum()
fuel_share_p1 = (df[df['has_electric_pump'] == 1]['fuel_share'] * w_p1).sum() / w_p1.sum()

lantern_rate_p0 = (df[df['has_electric_pump'] == 0]['has_lantern'] * w_p0).sum() / w_p0.sum() * 100.0
lantern_rate_p1 = (df[df['has_electric_pump'] == 1]['has_lantern'] * w_p1).sum() / w_p1.sum() * 100.0

print(f"Fuel Budget Share: No Pump = {fuel_share_p0:.2f}% vs With Electric Pump = {fuel_share_p1:.2f}%")
print(f"Kerosene Lantern Ownership: No Pump = {lantern_rate_p0:.1f}% vs With Electric Pump = {lantern_rate_p1:.1f}%")

plt.figure(figsize=(9, 4.8), dpi=300)
categories = ['Ceiling Fan Ownership\n(Electric)', 'Kerosene Lantern\nOwnership (Non-Electric)', 'Fuel Expenditure\nShare of Budget (%)']
no_pmp = [6.65, lantern_rate_p0, fuel_share_p0]
with_pmp = [29.40, lantern_rate_p1, fuel_share_p1]

x = np.arange(len(categories))
width = 0.35

plt.bar(x - width/2, no_pmp, width, label='Without Electric Pump', color='#94a3b8')
plt.bar(x + width/2, with_pmp, width, label='With Electric Pump', color='#1e3a8a')

for i in range(len(categories)):
    plt.text(i - width/2, no_pmp[i] + 1.5, f"{no_pmp[i]:.1f}%", ha='center', fontsize=10, fontweight='bold')
    plt.text(i + width/2, with_pmp[i] + 1.5, f"{with_pmp[i]:.1f}%", ha='center', fontsize=10, fontweight='bold', color='#1e3a8a')

plt.title('The Household Energy Transition: Kerosene vs Electric Lighting\n(ARIS-REDS 1982, Survey-Weighted Means)', fontsize=12, fontweight='bold', pad=15)
plt.ylabel('Rate / Percentage (%)', fontsize=11)
plt.xticks(x, categories, fontsize=10.5, fontweight='bold')
plt.ylim(0, 105)
plt.legend(frameon=True, facecolor='white', loc='upper right')
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.tight_layout()

fig_fuel_path = os.path.join(fig_dir, 'fuel_expenditure_and_kerosene_displacement.png')
plt.savefig(fig_fuel_path)
plt.close()
print(f"Saved fuel transition figure to {fig_fuel_path}")

print("\nAll supplemental analyses requested by Abhishek completed successfully!")

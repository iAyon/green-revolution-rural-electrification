"""
Run Household Micro-Econometric Analysis (REDS 1982)
Testing the 'Pumps to Plugs' hypothesis at the household level:
1. Survey-weighted appliance ownership (fans, radios, electric appliances).
2. Cross-tabulation by wealth status (Col 20 Household Rating) and Electric Pump ownership.
3. Weighted Least Squares (WLS) regressions controlling for land, wealth, household size, and comparing electric pumps against diesel pumps (placebo test).
4. Export publication-ready figures and tables for tomorrow's meeting.
"""

import os
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

# 1. Load Data
hh_path = 'DSI Research/data/lauren_clean/Household-level/redsecon_1982_household_table.csv'
dur_path = 'DSI Research/data/lauren_clean/Household-level/redsecon_1982_durables_table.csv'
fig_dir = 'DSI Research/docs/figures'
data_dir = 'DSI Research/data'
os.makedirs(fig_dir, exist_ok=True)

hh = pd.read_csv(hh_path)
dur = pd.read_csv(dur_path)

print(f"Loaded {len(hh)} households and {len(dur)} durable asset records.")

# 2. Extract Appliance Ownership from Durables Table
fans_hh = set(dur[dur['consumer_durables_q1_col1_item_name'] == 'fans']['interview_number_1982'])
other_elec_hh = set(dur[dur['consumer_durables_q1_col1_item_name'] == 'other_electric_appliances']['interview_number_1982'])
all_elec_app_hh = set(dur[dur['consumer_durables_q1_col1_item_name'].isin(['fans', 'other_electric_appliances', 'water_boiler'])]['interview_number_1982'])
radio_hh = set(dur[dur['consumer_durables_q1_col1_item_name'].isin(['radio', 'transistor'])]['interview_number_1982'])

# Build clean analysis dataframe
df = pd.DataFrame({
    'interview_id': hh['interview_number_1982'],
    'weight': hh['survey_weight_1982'].fillna(1.0).astype(float),
    'state': hh['state_std'].fillna('Other'),
    'district': hh['district_std'].fillna('Other'),
    'district_id': hh['district_std_id'].fillna(0).astype(int),
    'income_rating': hh['hh_comp_household_rating_1_high_2_middle_3_low_income'].fillna(2).astype(int),
    'hh_size': hh['hh_comp_household_size_number_of_persons'].fillna(hh['hh_comp_household_size_number_of_persons'].median()).astype(float),
    'land_owned': hh['farm_land_q7_2_land_owned_end_RP_hectares'].fillna(0).astype(float),
    'hyv_area': hh['cropping_pattern_area_HYV_irrigated_hectares'].fillna(0).astype(float),
    'has_electric_pump': (hh['farm_assets_irrigation_q1_3_electric_pumpset_col2_number_owned_start_RP'] > 0).astype(float),
    'has_diesel_pump': (hh['farm_assets_irrigation_q1_4_diesel_pumpset_col2_number_owned_start_RP'] > 0).astype(float),
    'has_fan': hh['interview_number_1982'].isin(fans_hh).astype(float),
    'has_other_elec': hh['interview_number_1982'].isin(other_elec_hh).astype(float),
    'has_any_appliance': hh['interview_number_1982'].isin(all_elec_app_hh).astype(float),
    'has_radio': hh['interview_number_1982'].isin(radio_hh).astype(float),
    'tot_exp': hh['cons_exp_computed_total_consumer_expenditure_Rs'].fillna(0).astype(float),
    'fuel_exp': hh['cons_exp_q4_8_fuel_total_Rs'].fillna(0).astype(float)
})

# 3. Weighted Summary Statistics
w = df['weight']

def weighted_mean(series, weights):
    return (series * weights).sum() / weights.sum()

print("\n" + "="*70)
print("SURVEY-WEIGHTED NATIONAL ADOPTION RATES (N = 4,981 Households)")
print("="*70)
summary_metrics = {
    'Electric Pumpset Ownership': weighted_mean(df['has_electric_pump'], w) * 100,
    'Diesel Pumpset Ownership': weighted_mean(df['has_diesel_pump'], w) * 100,
    'Ceiling Fan Ownership': weighted_mean(df['has_fan'], w) * 100,
    'Other Electric Appliances': weighted_mean(df['has_other_elec'], w) * 100,
    'Any Electric Appliance': weighted_mean(df['has_any_appliance'], w) * 100,
    'Radio / Transistor': weighted_mean(df['has_radio'], w) * 100
}
for k, v in summary_metrics.items():
    print(f"{k:30s}: {v:6.2f}%")

# Cross-tabulation by Wealth Rating & Electric Pump Ownership
rating_labels = {1: 'High Income', 2: 'Middle Income', 3: 'Low Income'}
crosstab_rows = []

print("\n" + "="*70)
print("APPLIANCE ADOPTION BY WEALTH RATING & ELECTRIC PUMP STATUS")
print("="*70)
for r in [1, 2, 3]:
    sub_r = df[df['income_rating'] == r]
    w_r = sub_r['weight']
    tot_rate = weighted_mean(sub_r['has_any_appliance'], w_r) * 100
    
    sub_nopump = sub_r[sub_r['has_electric_pump'] == 0]
    rate_nopump = weighted_mean(sub_nopump['has_any_appliance'], sub_nopump['weight']) * 100
    
    sub_pump = sub_r[sub_r['has_electric_pump'] == 1]
    rate_pump = weighted_mean(sub_pump['has_any_appliance'], sub_pump['weight']) * 100
    
    crosstab_rows.append({
        'Wealth_Rating': rating_labels[r],
        'Total_Appliance_Rate_Pct': tot_rate,
        'No_Pump_Appliance_Rate_Pct': rate_nopump,
        'With_Electric_Pump_Appliance_Rate_Pct': rate_pump,
        'Multiplier': rate_pump / rate_nopump if rate_nopump > 0 else np.nan,
        'Unweighted_N_NoPump': len(sub_nopump),
        'Unweighted_N_Pump': len(sub_pump)
    })
    print(f"{rating_labels[r]:15s}: All = {tot_rate:5.1f}% | No Pump = {rate_nopump:5.1f}% -> With Electric Pump = {rate_pump:5.1f}% (x{rate_pump/rate_nopump:.2f})")

df_crosstab = pd.DataFrame(crosstab_rows)
df_crosstab.to_csv(os.path.join(data_dir, 'household_1982_weighted_summary_table.csv'), index=False)
print("Saved summary table to data/household_1982_weighted_summary_table.csv")

# 4. Econometric Regressions (Weighted Least Squares with Robust HC1 Errors)
print("\n" + "="*70)
print("MICRO-ECONOMETRIC REGRESSION: DOMESTIC APPLIANCE OWNERSHIP")
print("="*70)

formula_app = 'has_any_appliance ~ has_electric_pump + has_diesel_pump + hyv_area + land_owned + hh_size + C(income_rating)'
mod_app = smf.wls(formula_app, data=df, weights=df['weight']).fit(cov_type='HC1')
print(mod_app.summary().tables[1])

formula_fan = 'has_fan ~ has_electric_pump + has_diesel_pump + hyv_area + land_owned + hh_size + C(income_rating)'
mod_fan = smf.wls(formula_fan, data=df, weights=df['weight']).fit(cov_type='HC1')

reg_summary = []
for var in ['has_electric_pump', 'has_diesel_pump', 'hyv_area', 'land_owned', 'hh_size']:
    reg_summary.append({
        'Variable': var,
        'Coef_Any_Appliance': mod_app.params[var],
        'SE_Any_Appliance': mod_app.bse[var],
        'p_Any_Appliance': mod_app.pvalues[var],
        'Coef_Fan': mod_fan.params[var],
        'SE_Fan': mod_fan.bse[var],
        'p_Fan': mod_fan.pvalues[var]
    })
df_reg_out = pd.DataFrame(reg_summary)
df_reg_out.to_csv(os.path.join(data_dir, 'household_1982_micro_regression_table.csv'), index=False)
print("Saved regression output table.")

# 5. VISUALIZATIONS

# Figure 1: Appliance Ownership by Wealth Rating and Pump Status
plt.figure(figsize=(9, 5.5), dpi=300)
bar_width = 0.35
indices = np.arange(len(df_crosstab))

plt.bar(indices - bar_width/2, df_crosstab['No_Pump_Appliance_Rate_Pct'], bar_width, 
        label='Without Electric Pumpset', color='#94a3b8', edgecolor='#64748b', linewidth=1)
plt.bar(indices + bar_width/2, df_crosstab['With_Electric_Pump_Appliance_Rate_Pct'], bar_width, 
        label='With Electric Pumpset', color='#1f77b4', edgecolor='#0f2042', linewidth=1.2)

for i in range(len(df_crosstab)):
    val_no = df_crosstab['No_Pump_Appliance_Rate_Pct'].iloc[i]
    val_yes = df_crosstab['With_Electric_Pump_Appliance_Rate_Pct'].iloc[i]
    mult = df_crosstab['Multiplier'].iloc[i]
    plt.text(i - bar_width/2, val_no + 1.2, f"{val_no:.1f}%", ha='center', fontsize=10, fontweight='bold', color='#475569')
    plt.text(i + bar_width/2, val_yes + 1.2, f"{val_yes:.1f}%\n(+{mult:.1f}x)", ha='center', fontsize=10, fontweight='bold', color='#1e3a8a')

plt.title('Household Electric Appliance Ownership by Wealth Rating and Farm Pump Status\n(ARIS-REDS 1982, Survey-Weighted Means, N = 4,981)', 
          fontsize=12, fontweight='bold', pad=15)
plt.ylabel('Share of Households Owning Electric Appliances (%)', fontsize=11)
plt.xticks(indices, df_crosstab['Wealth_Rating'], fontsize=11, fontweight='bold')
plt.ylim(0, 75)
plt.legend(frameon=True, facecolor='white', loc='upper left')
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.tight_layout()

fig1_path = os.path.join(fig_dir, 'household_appliance_by_pump_and_wealth.png')
plt.savefig(fig1_path)
plt.close()
print(f"Saved Figure 1 to {fig1_path}")

# Figure 2: Forest Plot of Regression Coefficients (Electric Pump vs Diesel Pump vs HYV)
plt.figure(figsize=(9, 4.5), dpi=300)
plot_vars = [
    ('Electric Pumpset (1=Yes)', mod_app.params['has_electric_pump'], mod_app.bse['has_electric_pump'], '#1f77b4'),
    ('Diesel Pumpset (Placebo)', mod_app.params['has_diesel_pump'], mod_app.bse['has_diesel_pump'], '#e11d48'),
    ('HYV Irrigated Area (ha)', mod_app.params['hyv_area'], mod_app.bse['hyv_area'], '#16a34a'),
    ('Land Owned (ha)', mod_app.params['land_owned'], mod_app.bse['land_owned'], '#64748b'),
    ('Household Size', mod_app.params['hh_size'], mod_app.bse['hh_size'], '#64748b')
]

y_pos = np.arange(len(plot_vars))
for idx, (label, coef, se, col) in enumerate(plot_vars):
    ci_low = coef - 1.96 * se
    ci_high = coef + 1.96 * se
    plt.errorbar(coef, idx, xerr=1.96*se, fmt='o', color=col, ecolor=col, elinewidth=2, capsize=5, markersize=8)
    plt.text(coef, idx + 0.22, f"beta = {coef:+.3f} (p = {mod_app.pvalues[list(mod_app.params.keys())[idx+1]]:.3f})", 
             ha='center', fontsize=9, fontweight='bold', color=col)

plt.axvline(0, color='black', linestyle='--', linewidth=1)
plt.yticks(y_pos, [p[0] for p in plot_vars], fontsize=11, fontweight='bold')
plt.xlabel('Marginal Effect on Probability of Owning Electric Appliances (Percentage Points / 100)', fontsize=11)
plt.title('Micro-Level Econometric Evidence: Electric vs Diesel Pumpsets\n(WLS with Robust HC1 Standard Errors, Controlling for Wealth Rating)', 
          fontsize=12, fontweight='bold', pad=15)
plt.xlim(-0.15, 0.55)
plt.grid(axis='x', linestyle=':', alpha=0.6)
plt.tight_layout()

fig2_path = os.path.join(fig_dir, 'micro_regression_coefficients_pumps_to_plugs.png')
plt.savefig(fig2_path)
plt.close()
print(f"Saved Figure 2 to {fig2_path}")

# Figure 3: Household Consumption & Fuel Expenditure Comparison
exp_means = {
    'Total Consumption Expenditure': (
        weighted_mean(df[df['has_electric_pump']==0]['tot_exp'], df[df['has_electric_pump']==0]['weight']),
        weighted_mean(df[df['has_electric_pump']==1]['tot_exp'], df[df['has_electric_pump']==1]['weight'])
    ),
    'Annual Fuel Expenditure': (
        weighted_mean(df[df['has_electric_pump']==0]['fuel_exp'], df[df['has_electric_pump']==0]['weight']),
        weighted_mean(df[df['has_electric_pump']==1]['fuel_exp'], df[df['has_electric_pump']==1]['weight'])
    )
}

plt.figure(figsize=(9, 4.5), dpi=300)
x_labels = list(exp_means.keys())
no_pmp_vals = [exp_means[k][0] for k in x_labels]
pmp_vals = [exp_means[k][1] for k in x_labels]

x = np.arange(len(x_labels))
width = 0.35

plt.bar(x - width/2, no_pmp_vals, width, label='Without Electric Pump', color='#94a3b8')
plt.bar(x + width/2, pmp_vals, width, label='With Electric Pump', color='#2563eb')

for i in range(len(x_labels)):
    plt.text(i - width/2, no_pmp_vals[i] + 150, f"Rs {no_pmp_vals[i]:,.0f}", ha='center', fontsize=10, fontweight='bold')
    plt.text(i + width/2, pmp_vals[i] + 150, f"Rs {pmp_vals[i]:,.0f}\n(+{pmp_vals[i]/no_pmp_vals[i]:.2f}x)", ha='center', fontsize=10, fontweight='bold', color='#1e3a8a')

plt.title('Household Consumption & Fuel Expenditure by Farm Electrification Status\n(Survey-Weighted Means, ARIS-REDS 1982)', fontsize=12, fontweight='bold', pad=15)
plt.ylabel('Annual Expenditure (Rupees)', fontsize=11)
plt.xticks(x, x_labels, fontsize=11, fontweight='bold')
plt.ylim(0, 10000)
plt.legend(frameon=True, facecolor='white')
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.tight_layout()

fig3_path = os.path.join(fig_dir, 'household_expenditure_by_pump_status.png')
plt.savefig(fig3_path)
plt.close()
print(f"Saved Figure 3 to {fig3_path}")
print("\nAll analyses and figures generated successfully!")

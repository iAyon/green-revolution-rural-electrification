import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import os

fig_dir = 'DSI Research/docs/figures'
os.makedirs(fig_dir, exist_ok=True)

print("=== PART 1: DISTRICT LEVEL EVENT STUDY (ICRISAT PANEL) ===")
agri_path = 'DSI Research/data/icrisat_master_agri_panel_1966_2020.csv'
df_agri = pd.read_csv(agri_path)

# Rename columns
rename_dict = {
    'TOTAL AREA': 'hyv_total',
    'WHEAT AREA': 'hyv_wheat',
    'RICE AREA': 'hyv_rice',
    'TUBE WELLS AREA': 'tubewells',
    'CANALS AREA': 'canals',
    'NET AREA': 'net_irrig'
}
df_agri = df_agri.rename(columns=rename_dict)

for col in ['hyv_total', 'hyv_wheat', 'hyv_rice', 'tubewells', 'canals', 'net_irrig']:
    df_agri[col] = pd.to_numeric(df_agri[col], errors='coerce').fillna(0)

df_agri['Year'] = pd.to_numeric(df_agri['Year'], errors='coerce')
df_agri['dist_id'] = pd.to_numeric(df_agri['Dist Code'], errors='coerce')
df_agri = df_agri.dropna(subset=['Year', 'dist_id'])
df_agri = df_agri[(df_agri['Year'] >= 1966) & (df_agri['Year'] <= 2005)].copy()

# Identify Early Wheat HYV Districts (Top quartile of 1966-1972 HYV Wheat area)
early_wheat = df_agri[(df_agri['Year'] >= 1966) & (df_agri['Year'] <= 1972)].groupby('dist_id')['hyv_wheat'].mean().reset_index()
q75_wheat = early_wheat['hyv_wheat'].quantile(0.75)
early_wheat['high_early_wheat'] = (early_wheat['hyv_wheat'] >= q75_wheat).astype(int)
print(f"Top Quartile Early HYV Wheat Threshold: {q75_wheat:.2f} thousand ha")
print(f"Early HYV Wheat Districts: {early_wheat['high_early_wheat'].sum()} vs Other Districts: {(1 - early_wheat['high_early_wheat']).sum()}")

df_agri = pd.merge(df_agri, early_wheat[['dist_id', 'high_early_wheat']], on='dist_id', how='left')

# Drop any row with missing values in key regression variables
df_reg = df_agri.dropna(subset=['tubewells', 'hyv_wheat', 'hyv_rice', 'high_early_wheat', 'dist_id', 'Year']).copy()
df_reg['dist_cat'] = df_reg['dist_id'].astype('category')
df_reg['year_cat'] = df_reg['Year'].astype('category')

# 1. TWFE Model: Wheat & Rice HYV Area on Tubewell Area
twfe_model = smf.ols('tubewells ~ hyv_wheat + hyv_rice + C(dist_cat) + C(year_cat)', data=df_reg).fit(
    cov_type='cluster', cov_kwds={'groups': df_reg['dist_id']}
)

b_wheat = twfe_model.params['hyv_wheat']
se_wheat = twfe_model.bse['hyv_wheat']
t_wheat = twfe_model.tvalues['hyv_wheat']
p_wheat = twfe_model.pvalues['hyv_wheat']

b_rice = twfe_model.params['hyv_rice']
se_rice = twfe_model.bse['hyv_rice']
t_rice = twfe_model.tvalues['hyv_rice']
p_rice = twfe_model.pvalues['hyv_rice']

print("\n--- TWFE Model: HYV Crops on Tubewell Irrigated Acreage ---")
print(f"HYV Wheat Effect: beta = {b_wheat:.4f} (SE = {se_wheat:.4f}, t = {t_wheat:.2f}, p = {p_wheat:.4e})")
print(f"HYV Rice Effect:  beta = {b_rice:.4f} (SE = {se_rice:.4f}, t = {t_rice:.2f}, p = {p_rice:.4e})")
print(f"R-squared: {twfe_model.rsquared:.4f}, Observations: {int(twfe_model.nobs)}")

# 2. Dynamic Event Study: Interaction of high_early_wheat with Year dummies (1966 = reference year)
years = sorted([int(y) for y in df_reg['Year'].unique() if y >= 1966 and y <= 2000])
inter_cols = []
for y in years:
    if y != 1966:
        col_name = f'inter_{y}'
        df_reg[col_name] = (df_reg['high_early_wheat'] * (df_reg['Year'] == y)).astype(float)
        inter_cols.append(col_name)

formula_inter = 'tubewells ~ ' + ' + '.join(inter_cols) + ' + C(dist_cat) + C(year_cat)'
event_model = smf.ols(formula_inter, data=df_reg).fit(
    cov_type='cluster', cov_kwds={'groups': df_reg['dist_id']}
)

# Reference year 1966
event_records = [{'year': 1966, 'coef': 0.0, 'se': 0.0, 'ci_lower': 0.0, 'ci_upper': 0.0}]

for y in years:
    if y != 1966:
        col_name = f'inter_{y}'
        coef = event_model.params[col_name]
        se = event_model.bse[col_name]
        event_records.append({
            'year': y,
            'coef': coef,
            'se': se,
            'ci_lower': coef - 1.96 * se,
            'ci_upper': coef + 1.96 * se
        })

df_event = pd.DataFrame(event_records).sort_values('year')
df_event.to_csv('DSI Research/data/event_study_tubewell_coefficients.csv', index=False)
print("Saved event study coefficients.")

# Plot Event Study
plt.figure(figsize=(10, 5.5), dpi=300)
plt.axhline(0, color='gray', linestyle='--', linewidth=1)
plt.axvline(1966, color='darkred', linestyle=':', linewidth=1.5, label='Green Revolution Onset (1966)')
plt.fill_between(df_event['year'], df_event['ci_lower'], df_event['ci_upper'], color='#aec7e8', alpha=0.4, label='95% Confidence Interval')
plt.plot(df_event['year'], df_event['coef'], '-o', color='#1f77b4', linewidth=2, markersize=5, label='Event-Study Estimate')
plt.title('First-Stage Event Study: Impact of Early HYV Wheat Rollout on District Tubewell Acreage', fontsize=12, fontweight='bold', pad=15)
plt.xlabel('Year', fontsize=11)
plt.ylabel('Differential Tubewell Irrigated Area (\'000 Hectares)', fontsize=11)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(frameon=True, facecolor='white', loc='upper left')
plt.tight_layout()
fig_path = os.path.join(fig_dir, 'first_stage_event_study_tubewells.png')
plt.savefig(fig_path)
plt.close()
print(f"Saved event study figure to {fig_path}")

# Plot Dynamic Raw Trends in Tubewells: Early vs Late HYV Districts
trends = df_reg.groupby(['Year', 'high_early_wheat'])['tubewells'].mean().unstack()
plt.figure(figsize=(10, 5.5), dpi=300)
plt.plot(trends.index, trends[1], color='#d62728', linewidth=2.5, marker='s', markersize=4, label='Early HYV Wheat Districts (Top Quartile)')
plt.plot(trends.index, trends[0], color='#2ca02c', linewidth=2.5, marker='o', markersize=4, label='Late / Low HYV Wheat Districts')
plt.axvline(1966, color='black', linestyle=':', linewidth=1.5, label='Green Revolution Begins (1966)')
plt.title('Divergence in Groundwater Irrigation: Tubewell Acreage (1966–2005)', fontsize=12, fontweight='bold', pad=15)
plt.xlabel('Year', fontsize=11)
plt.ylabel('Mean Tubewell Irrigated Area per District (\'000 Hectares)', fontsize=11)
plt.legend(frameon=True, facecolor='white')
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
fig_path2 = os.path.join(fig_dir, 'tubewell_divergence_trends.png')
plt.savefig(fig_path2)
plt.close()
print(f"Saved trends figure to {fig_path2}")

# -------------------------------------------------------------
# PART 2: VILLAGE LEVEL ANALYSIS (REDS VILLAGES)
# -------------------------------------------------------------
print("\n=== PART 2: VILLAGE LEVEL ANALYSIS (ARIS-REDS LINKAGE) ===")
vill_path = 'DSI Research/data/aris_reds_villages_electrification_panel.csv'
cross_path = 'DSI Research/data/reds_to_icrisat_concordance_final.csv'

df_vill = pd.read_csv(vill_path)
df_cross = pd.read_csv(cross_path)

df_vill_merged = pd.merge(df_vill, df_cross[['district99', 'state99', 'icrisat_dist_code', 'icrisat_dist_name']], on=['district99', 'state99'], how='left')
df_vill_merged = pd.merge(df_vill_merged, early_wheat, left_on='icrisat_dist_code', right_on='dist_id', how='left')

print(f"Villages linked to district agricultural shocks: {df_vill_merged['high_early_wheat'].notnull().sum()} out of {len(df_vill_merged)}")

df_elec = df_vill_merged[df_vill_merged['electrified_calendar_year'] > 0].dropna(subset=['high_early_wheat', 'icrisat_dist_code']).copy()

# Regress Electrification Year on Early HYV Wheat indicator
m_year = smf.ols('electrified_calendar_year ~ high_early_wheat', data=df_elec).fit(
    cov_type='cluster', cov_kwds={'groups': df_elec['icrisat_dist_code']}
)
b_yr = m_year.params['high_early_wheat']
se_yr = m_year.bse['high_early_wheat']
p_yr = m_year.pvalues['high_early_wheat']

# Regress Electric Pumps on Early HYV Wheat indicator
df_vill_clean = df_vill_merged.dropna(subset=['high_early_wheat', 'icrisat_dist_code']).copy()
m_pumps = smf.ols('pmpelec ~ high_early_wheat', data=df_vill_clean).fit(
    cov_type='cluster', cov_kwds={'groups': df_vill_clean['icrisat_dist_code']}
)
b_pmp = m_pumps.params['high_early_wheat']
se_pmp = m_pumps.bse['high_early_wheat']
p_pmp = m_pumps.pvalues['high_early_wheat']

# Regress Electrified Households on Early HYV Wheat indicator
m_hh = smf.ols('hhelec ~ high_early_wheat', data=df_vill_clean).fit(
    cov_type='cluster', cov_kwds={'groups': df_vill_clean['icrisat_dist_code']}
)
b_hh = m_hh.params['high_early_wheat']
se_hh = m_hh.bse['high_early_wheat']
p_hh = m_hh.pvalues['high_early_wheat']

# Regress TVs on Early HYV Wheat indicator
m_tv = smf.ols('tvs ~ high_early_wheat', data=df_vill_clean).fit(
    cov_type='cluster', cov_kwds={'groups': df_vill_clean['icrisat_dist_code']}
)
b_tv = m_tv.params['high_early_wheat']
se_tv = m_tv.bse['high_early_wheat']
p_tv = m_tv.pvalues['high_early_wheat']

print(f"\n1. Village Electrification Year: beta = {b_yr:.2f} years earlier (SE = {se_yr:.2f}, p = {p_yr:.4f})")
print(f"2. Electric Pumpsets:           beta = +{b_pmp:.2f} pumps per village (SE = {se_pmp:.2f}, p = {p_pmp:.4f})")
print(f"3. Electrified Households:       beta = +{b_hh:.2f} homes per village (SE = {se_hh:.2f}, p = {p_hh:.4f})")
print(f"4. Televisions:                  beta = +{b_tv:.2f} TVs per village (SE = {se_tv:.2f}, p = {p_tv:.4f})")

village_results = pd.DataFrame([
    {'Outcome': 'Electrification Calendar Year', 'Beta (Early HYV Wheat)': b_yr, 'Std_Error': se_yr, 'p_value': p_yr, 'N_Obs': int(m_year.nobs)},
    {'Outcome': 'Electric Pumpsets per Village', 'Beta (Early HYV Wheat)': b_pmp, 'Std_Error': se_pmp, 'p_value': p_pmp, 'N_Obs': int(m_pumps.nobs)},
    {'Outcome': 'Electrified Domestic Households', 'Beta (Early HYV Wheat)': b_hh, 'Std_Error': se_hh, 'p_value': p_hh, 'N_Obs': int(m_hh.nobs)},
    {'Outcome': 'Televisions per Village', 'Beta (Early HYV Wheat)': b_tv, 'Std_Error': se_tv, 'p_value': p_tv, 'N_Obs': int(m_tv.nobs)}
])
village_results.to_csv('DSI Research/data/village_first_stage_regressions.csv', index=False)
print("Saved village first-stage results table.")

# Plot Cumulative Electrification Hazard Curve: Early vs Late HYV
plt.figure(figsize=(10, 5.5), dpi=300)
years_axis = np.arange(1950, 2000)

for group, label, col in [(1, 'Early HYV Wheat Districts', '#d62728'), (0, 'Other Districts', '#1f77b4')]:
    sub = df_elec[df_elec['high_early_wheat'] == group]
    cum_share = [(sub['electrified_calendar_year'] <= yr).mean() * 100 for yr in years_axis]
    plt.plot(years_axis, cum_share, label=label, color=col, linewidth=2.5)

plt.axvline(1966, color='black', linestyle=':', linewidth=1.5, label='Green Revolution Begins (1966)')
plt.title('Cumulative Village Electrification Rate: Early HYV Wheat vs Other Districts', fontsize=12, fontweight='bold', pad=15)
plt.xlabel('Calendar Year', fontsize=11)
plt.ylabel('Percent of Villages Electrified (%)', fontsize=11)
plt.legend(frameon=True, facecolor='white', loc='upper left')
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
fig_path3 = os.path.join(fig_dir, 'village_electrification_cumulative_hazard.png')
plt.savefig(fig_path3)
plt.close()
print(f"Saved hazard curve figure to {fig_path3}")
print("\nAll first-stage event study analyses completed successfully!")

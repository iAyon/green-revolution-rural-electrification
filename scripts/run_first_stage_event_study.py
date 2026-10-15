import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import os

# Create figures directory
fig_dir = 'DSI Research/docs/figures'
os.makedirs(fig_dir, exist_ok=True)

# 1. Load Data
agri_path = 'DSI Research/data/icrisat_master_agri_panel_1966_2020.csv'
df_agri = pd.read_csv(agri_path)

# Rename columns to avoid spaces
rename_map = {
    'TOTAL AREA': 'hyv_total_area',
    'WHEAT AREA': 'hyv_wheat_area',
    'RICE AREA': 'hyv_rice_area',
    'TUBE WELLS AREA': 'tubewells_area',
    'CANALS AREA': 'canals_area',
    'NET AREA': 'net_irrig_area',
    'GROSS AREA': 'gross_irrig_area'
}
df_agri = df_agri.rename(columns=rename_map)

num_cols = list(rename_map.values())
for c in num_cols:
    df_agri[c] = pd.to_numeric(df_agri[c], errors='coerce').fillna(0)

df_agri['Year'] = pd.to_numeric(df_agri['Year'], errors='coerce')
df_agri['Dist_Code_Num'] = pd.to_numeric(df_agri['Dist Code'], errors='coerce')
df_agri = df_agri.dropna(subset=['Year', 'Dist_Code_Num'])
df_agri = df_agri[(df_agri['Year'] >= 1966) & (df_agri['Year'] <= 2011)].copy()

print(f"Sample size for panel analysis: {len(df_agri)} district-years")

# Calculate Early HYV adoption (1966-1975 mean HYV area)
early_hyv = df_agri[(df_agri['Year'] >= 1966) & (df_agri['Year'] <= 1975)].groupby('Dist_Code_Num')['hyv_total_area'].mean().reset_index()
early_hyv.columns = ['Dist_Code_Num', 'early_hyv_mean']

median_hyv = early_hyv['early_hyv_mean'].median()
early_hyv['early_adopter'] = (early_hyv['early_hyv_mean'] > median_hyv).astype(int)
print(f"Early HYV Adopter threshold (median): {median_hyv:.2f} thousand ha")
print(f"Districts in High Early HYV: {early_hyv['early_adopter'].sum()}, Low Early HYV: {(1 - early_hyv['early_adopter']).sum()}")

df_agri = pd.merge(df_agri, early_hyv, on='Dist_Code_Num', how='left')

# District-level Panel Regression: Tubewells on HYV Area with District and Year FEs
print("\n--- Running District Panel TWFE Regression ---")
model_twfe = smf.ols('tubewells_area ~ hyv_total_area + C(Dist_Code_Num) + C(Year)', data=df_agri).fit(
    cov_type='cluster', cov_kwds={'groups': df_agri['Dist_Code_Num']}
)

beta = model_twfe.params['hyv_total_area']
se = model_twfe.bse['hyv_total_area']
t_stat = model_twfe.tvalues['hyv_total_area']
pval = model_twfe.pvalues['hyv_total_area']

print(f"Coefficient on HYV Area: {beta:.4f}")
print(f"Std Error (clustered by district): {se:.4f}")
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {pval:.4e}")
print(f"R-squared: {model_twfe.rsquared:.4f}")
print(f"Number of observations: {int(model_twfe.nobs)}")

# Save regression summary
with open('DSI Research/data/first_stage_panel_regression.txt', 'w') as f:
    f.write(model_twfe.summary().as_text())

print("Saved regression output.")

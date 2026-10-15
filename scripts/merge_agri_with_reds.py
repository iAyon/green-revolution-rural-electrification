import pandas as pd
import numpy as np
import os

def run_merge():
    data_dir = 'DSI Research/data'
    hyv_path = os.path.join(data_dir, 'icrisat_hyv_panel_1966_2011.csv')
    irrig_path = os.path.join(data_dir, 'icrisat_irrigation_tubewells_panel_1966_2020.csv')
    concord_path = os.path.join(data_dir, 'aris_reds_districts_master_concordance.csv')
    vill_path = os.path.join(data_dir, 'aris_reds_villages_electrification_panel.csv')

    if not os.path.exists(hyv_path) or not os.path.exists(irrig_path):
        print("Agri files not ready yet.")
        return

    print("Loading datasets...")
    df_hyv = pd.read_csv(hyv_path)
    df_irrig = pd.read_csv(irrig_path)
    df_concord = pd.read_csv(concord_path)
    df_vill = pd.read_csv(vill_path)

    print(f"HYV panel: {df_hyv.shape}")
    print(f"Irrigation panel: {df_irrig.shape}")
    print(f"Concordance: {df_concord.shape}")
    print(f"Village panel: {df_vill.shape}")

    # Standardize names for merging
    df_hyv['dist_clean'] = df_hyv['Dist Name'].str.lower().str.strip()
    df_irrig['dist_clean'] = df_irrig['Dist Name'].str.lower().str.strip()
    df_concord['dist_clean'] = df_concord['district_name'].str.lower().str.strip()

    # Merge HYV and Irrigation
    df_agri = pd.merge(
        df_hyv,
        df_irrig[['Dist Code', 'Year', 'CANALS AREA', 'TANKS AREA', 'TUBE WELLS AREA', 'OTHER WELLS AREA', 'TOTAL WELLS AREA', 'NET AREA', 'GROSS AREA']],
        on=['Dist Code', 'Year'],
        how='outer'
    )
    print(f"Merged Agri panel: {df_agri.shape}")
    df_agri.to_csv(os.path.join(data_dir, 'icrisat_master_agri_panel_1966_2020.csv'), index=False)
    print("Saved master agricultural panel.")

    # Match ARIS-REDS districts to ICRISAT districts
    matched = pd.merge(df_concord, df_agri[['dist_clean', 'State Name', 'Dist Name', 'Dist Code']].drop_duplicates(), on='dist_clean', how='left')
    print(f"Matched {matched['Dist Code'].notnull().sum()} out of {len(df_concord)} REDS districts on exact name.")
    
    # Save match table
    matched.to_csv(os.path.join(data_dir, 'reds_icrisat_district_crosswalk.csv'), index=False)
    print("Saved reds_icrisat_district_crosswalk.csv")

if __name__ == '__main__':
    run_merge()

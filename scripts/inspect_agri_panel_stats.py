import pandas as pd
import numpy as np

df = pd.read_csv('DSI Research/data/icrisat_master_agri_panel_1966_2020.csv')
print(f"Master Agri Panel Shape: {df.shape}")
print("Columns:", df.columns.tolist())

# Inspect Year distribution
print("Years range:", df['Year'].min(), "to", df['Year'].max())

# Inspect HYV and Tubewell columns
for col in ['TOTAL AREA', 'WHEAT AREA', 'RICE AREA', 'TUBE WELLS AREA', 'CANALS AREA', 'NET AREA']:
    if col in df.columns:
        s = pd.to_numeric(df[col], errors='coerce')
        print(f"{col}: count non-null={s.notnull().sum()}, mean={s.mean():.2f}, max={s.max():.2f}")

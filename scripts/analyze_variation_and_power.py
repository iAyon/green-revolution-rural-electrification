import pandas as pd
import numpy as np

def analyze_variation():
    df = pd.read_csv('DSI Research/data/aris_reds_villages_electrification_panel.csv')
    print(f"Total villages analyzed: {len(df)}")

    # Electrification status
    df['is_electrified_by_1999'] = df['elecy'] > 0
    df['electrified_pre1975'] = (df['elecy'] > 0) & (df['elecy'] <= 75)
    df['electrified_pre1985'] = (df['elecy'] > 0) & (df['elecy'] <= 85)

    print("\n--- National Electrification Milestones in REDS Villages ---")
    print(f"Electrified before 1975 (Early Green Revolution): {df['electrified_pre1975'].sum()} ({df['electrified_pre1975'].mean()*100:.1f}%)")
    print(f"Electrified before 1985 (Mid-Green Revolution): {df['electrified_pre1985'].sum()} ({df['electrified_pre1985'].mean()*100:.1f}%)")
    print(f"Electrified by 1999: {df['is_electrified_by_1999'].sum()} ({df['is_electrified_by_1999'].mean()*100:.1f}%)")
    print(f"Still un-electrified in 1999: {(~df['is_electrified_by_1999']).sum()} ({(~df['is_electrified_by_1999']).mean()*100:.1f}%)")

    # Group by IADP (Intensive Agricultural District Programme - Earliest HYV adopters)
    print("\n--- Comparison: IADP (Pioneer HYV) vs Non-IADP Districts ---")
    iadp_comp = df.groupby('is_iadp_named').agg(
        villages_count=('vill_id', 'count'),
        pct_electrified_pre1975=('electrified_pre1975', lambda x: x.mean() * 100),
        pct_electrified_pre1985=('electrified_pre1985', lambda x: x.mean() * 100),
        mean_year_electrified=('electrified_calendar_year', lambda x: x[x > 0].mean()),
        median_year_electrified=('electrified_calendar_year', lambda x: x[x > 0].median()),
        mean_electric_pumps=('pmpelec', 'mean'),
        median_electric_pumps=('pmpelec', 'median'),
        mean_electrified_hhs=('hhelec', 'mean'),
        median_electrified_hhs=('hhelec', 'median'),
        mean_tvs=('tvs', 'mean')
    ).rename(index={True: 'IADP Districts (Pioneer Green Rev)', False: 'Non-IADP Districts'})
    print(iadp_comp.to_string())

    # State-level variation table
    state_table = df.groupby('state_name').agg(
        total_villages=('vill_id', 'count'),
        pct_elec_pre1975=('electrified_pre1975', lambda x: round(x.mean() * 100, 1)),
        pct_elec_pre1985=('electrified_pre1985', lambda x: round(x.mean() * 100, 1)),
        mean_year=('electrified_calendar_year', lambda x: round(x[x > 0].mean(), 1) if (x > 0).any() else np.nan),
        mean_pumps=('pmpelec', lambda x: round(x.mean(), 1)),
        mean_domestic_hhs=('hhelec', lambda x: round(x.mean(), 1)),
        mean_tvs=('tvs', lambda x: round(x.mean(), 1))
    ).sort_values('pct_elec_pre1975', ascending=False)

    print("\n--- State-by-State Variation in Rural Electrification ---")
    print(state_table.to_string())

    # Save summary tables
    iadp_comp.to_csv('DSI Research/data/iadp_vs_non_iadp_variation.csv')
    state_table.to_csv('DSI Research/data/state_electrification_variation.csv')
    print("\nSaved variation tables to CSV.")

if __name__ == '__main__':
    analyze_variation()

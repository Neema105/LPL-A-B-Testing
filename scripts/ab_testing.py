import pandas as pd
import numpy as np
from scipy import stats
from sqlalchemy import create_engine, text
import os
from pathlib import Path

DB_URL = os.environ['DATABASE_URL']
BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR  = BASE_DIR / 'outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

engine = create_engine(DB_URL)

print('Pulling data from PostgreSQL...')
with engine.connect() as conn:
    df = pd.read_sql(text('SELECT * FROM lpl_ab_analysis'), conn)
print(f'  {len(df)} rows loaded')
print()

print('=' * 55)
print('A/B TEST 1: FIRST DRAGON')
print('=' * 55)

ab_results = []

for side in ['Blue', 'Red']:
    s = df[df['side'] == side]

    treatment = s[s['got_fd'] == 1]['result']
    control   = s[s['got_fd'] == 0]['result']

    contingency = pd.crosstab(s['got_fd'], s['result'])
    chi2, p, _, _ = stats.chi2_contingency(contingency)

    p1 = treatment.mean()
    p2 = control.mean()
    cohens_h = abs(2 * np.arcsin(np.sqrt(p1)) - 2 * np.arcsin(np.sqrt(p2)))

    n1, n2   = len(treatment), len(control)
    se       = np.sqrt((p1 * (1 - p1) / n1) + (p2 * (1 - p2) / n2))
    ci_lower = round((p1 - p2) - 1.96 * se, 4)
    ci_upper = round((p1 - p2) + 1.96 * se, 4)

    significant = 'YES' if p < 0.05 else 'NO'

    print(f'\n  {side} Side')
    print(f'    Treatment (Got FD) : {p1:.1%} win rate  (n={n1})')
    print(f'    Control (No FD)    : {p2:.1%} win rate  (n={n2})')
    print(f'    Delta              : +{p1-p2:.1%}')
    print(f'    95% CI             : [{ci_lower}, {ci_upper}]')
    print(f'    Chi-squared        : {chi2:.4f}')
    print(f'    P-value            : {p:.6f}')
    print(f'    Effect size (h)    : {cohens_h:.4f}')
    print(f'    Significant        : {significant}')

    ab_results.append({
        'side': side, 'objective': 'First Dragon',
        'treatment_label': 'Got FD', 'control_label': 'No FD',
        'treatment_n': n1, 'control_n': n2,
        'treatment_wr': round(p1, 4), 'control_wr': round(p2, 4),
        'delta': round(p1 - p2, 4),
        'ci_lower': ci_lower, 'ci_upper': ci_upper,
        'chi2': round(chi2, 4), 'p_value': round(p, 6),
        'cohens_h': round(cohens_h, 4),
        'significant': 'YES' if p < 0.05 else 'NO'
    })

print()
print('=' * 55)
print('A/B TEST 2: VOID GRUBS')
print('=' * 55)

for side in ['Blue', 'Red']:
    s = df[df['side'] == side]

    treatment = s[s['got_more_grubs'] == 1]['result']
    control   = s[s['got_more_grubs'] == 0]['result']

    contingency = pd.crosstab(s['got_more_grubs'], s['result'])
    chi2, p, _, _ = stats.chi2_contingency(contingency)

    p1 = treatment.mean()
    p2 = control.mean()
    cohens_h = abs(2 * np.arcsin(np.sqrt(p1)) - 2 * np.arcsin(np.sqrt(p2)))

    n1, n2   = len(treatment), len(control)
    se       = np.sqrt((p1 * (1 - p1) / n1) + (p2 * (1 - p2) / n2))
    ci_lower = round((p1 - p2) - 1.96 * se, 4)
    ci_upper = round((p1 - p2) + 1.96 * se, 4)

    significant = 'YES' if p < 0.05 else 'NO'

    print(f'\n  {side} Side')
    print(f'    Treatment (More Grubs) : {p1:.1%} win rate  (n={n1})')
    print(f'    Control (Fewer Grubs)  : {p2:.1%} win rate  (n={n2})')
    print(f'    Delta                  : +{p1-p2:.1%}')
    print(f'    95% CI                 : [{ci_lower}, {ci_upper}]')
    print(f'    Chi-squared            : {chi2:.4f}')
    print(f'    P-value                : {p:.6f}')
    print(f'    Effect size (h)        : {cohens_h:.4f}')
    print(f'    Significant            : {significant}')

    ab_results.append({
        'side': side, 'objective': 'More Grubs',
        'treatment_label': 'More Grubs', 'control_label': 'Fewer Grubs',
        'treatment_n': n1, 'control_n': n2,
        'treatment_wr': round(p1, 4), 'control_wr': round(p2, 4),
        'delta': round(p1 - p2, 4),
        'ci_lower': ci_lower, 'ci_upper': ci_upper,
        'chi2': round(chi2, 4), 'p_value': round(p, 6),
        'cohens_h': round(cohens_h, 4),
        'significant': 'YES' if p < 0.05 else 'NO'
    })

print()
print('=' * 55)
print('SCENARIO BREAKDOWN BY SIDE')
print('=' * 55)

scenario_summary = df.groupby(['side', 'scenario'])['result'].agg(
    win_rate='mean',
    games='count',
    wins='sum'
).round(4).reset_index()

print()
print(scenario_summary.to_string(index=False))

print()
print('Exporting CSVs...')

df.to_csv(OUTPUT_DIR / 'lpl_ab_game_level.csv', index=False)
print(f'  {OUTPUT_DIR / "lpl_ab_game_level.csv"}')

ab_df = pd.DataFrame(ab_results)
ab_df.to_csv(OUTPUT_DIR / 'lpl_ab_stats_results.csv', index=False)
print(f'  {OUTPUT_DIR / "lpl_ab_stats_results.csv"}')

scenario_summary.to_csv(OUTPUT_DIR / 'lpl_scenario_summary.csv', index=False)
print(f'  {OUTPUT_DIR / "lpl_scenario_summary.csv"}')

print()
print('All done. Run 02_export_for_excel.py next.')

import pandas as pd
import numpy as np

df = pd.read_csv('/home/user/workspace/global_ads.csv')

# Filter Google Ads
g = df[df['platform'] == 'Google Ads'].copy()

# Recompute metrics (handle div-by-zero safely)
def safe_div(n, d):
    return np.where(d == 0, np.nan, n / d)

g['CTR'] = safe_div(g['clicks'], g['impressions'])
g['CPC'] = safe_div(g['ad_spend'], g['clicks'])
g['CPA'] = safe_div(g['ad_spend'], g['conversions'])
g['ROAS'] = safe_div(g['revenue'], g['ad_spend'])
g['Conversion_Rate'] = safe_div(g['conversions'], g['clicks'])

# Round for cleanliness
g['CTR'] = g['CTR'].round(4)
g['CPC'] = g['CPC'].round(2)
g['CPA'] = g['CPA'].round(2)
g['ROAS'] = g['ROAS'].round(2)
g['Conversion_Rate'] = g['Conversion_Rate'].round(4)

# Platform mean CPA (Google Ads only)
mean_cpa = g['CPA'].mean()
threshold_cpa = 1.3 * mean_cpa

def flag_row(row):
    flags = []
    if pd.notna(row['ROAS']) and row['ROAS'] < 2.0:
        flags.append('Underperforming')
    if pd.notna(row['CPA']) and row['CPA'] > threshold_cpa:
        flags.append('High Cost')
    if pd.notna(row['CTR']) and row['CTR'] < 0.01:
        flags.append('Low Relevance')
    return ', '.join(flags)

g['Flags'] = g.apply(flag_row, axis=1)

# Reorder columns
cols = ['date', 'platform', 'campaign_type', 'industry', 'country',
        'impressions', 'clicks', 'ad_spend', 'conversions', 'revenue',
        'CTR', 'CPC', 'CPA', 'ROAS', 'Conversion_Rate', 'Flags']
g = g[cols]

g.to_csv('/home/user/workspace/google_ads_analysis.csv', index=False)

print(f"Total Google Ads rows: {len(g)}")
print(f"Platform mean CPA: {mean_cpa:.2f}")
print(f"High Cost threshold (1.3x mean): {threshold_cpa:.2f}")
print("\nFlag distribution:")
print(g['Flags'].value_counts(dropna=False).to_string())
print("\nSample:")
print(g.head().to_string())

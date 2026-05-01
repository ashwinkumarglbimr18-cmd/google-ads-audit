import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('google_ads_analysis.csv')

# Account-level metrics
account_avg_roas = df['ROAS'].mean()
account_avg_cpa = df['CPA'].mean()
account_avg_ctr = df['CTR'].mean()

# Flag underperformers
df['High_CPA_Flag'] = df['CPA'] > account_avg_cpa
df['Low_ROAS_Flag'] = df['ROAS'] < account_avg_roas

# Campaign type breakdown
ct_roas = df.groupby('campaign_type')['ROAS'].mean().sort_values(ascending=False)
ct_cpa = df.groupby('campaign_type')['CPA'].mean().sort_values()
ct_spend = df.groupby('campaign_type')['ad_spend'].sum()
ct_conv = df.groupby('campaign_type')['conversions'].sum()

# Industry breakdown
ind_roas = df.groupby('industry')['ROAS'].mean().sort_values(ascending=False)
ind_cpa = df.groupby('industry')['CPA'].mean().sort_values()

# Country breakdown
country_roas = df.groupby('country')['ROAS'].mean().sort_values(ascending=False)
country_spend = df.groupby('country')['ad_spend'].sum().sort_values(ascending=False)

# Top and bottom performers by ROAS
top_performers = df.nlargest(10, 'ROAS')[['campaign_type', 'industry', 'country', 'ad_spend', 'ROAS', 'CPA']]
bottom_performers = df.nsmallest(10, 'ROAS')[['campaign_type', 'industry', 'country', 'ad_spend', 'ROAS', 'CPA']]

# Budget reallocation estimate
total_spend = df['ad_spend'].sum()
optimal_alloc = (ct_roas / ct_roas.sum()) * total_spend

# Chart 1: ROAS by Campaign Type
plt.figure(figsize=(10, 5))
bars = plt.bar(ct_roas.index, ct_roas.values, color='steelblue', edgecolor='white')
plt.axhline(account_avg_roas, color='red', linestyle='--', linewidth=1.5, label=f'Avg ROAS: {account_avg_roas:.2f}')
for bar, val in zip(bars, ct_roas.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, f'{val:.2f}', ha='center', va='bottom', fontsize=9)
plt.title('ROAS by Campaign Type', fontsize=13, fontweight='bold')
plt.ylabel('ROAS')
plt.xlabel('Campaign Type')
plt.legend()
plt.tight_layout()
plt.savefig('p1_chart1_roas_by_campaign_type.png', dpi=150)
plt.close()

# Chart 2: CPA vs Conversions scatter
plt.figure(figsize=(10, 6))
colors = df['campaign_type'].astype('category').cat.codes
scatter = plt.scatter(df['conversions'], df['CPA'], c=colors, cmap='tab10', s=60, alpha=0.7)
plt.axhline(account_avg_cpa, color='red', linestyle='--', linewidth=1.2, label=f'Avg CPA: {account_avg_cpa:.2f}')
plt.title('CPA vs Conversions by Campaign', fontsize=13, fontweight='bold')
plt.xlabel('Conversions')
plt.ylabel('CPA')
plt.legend()
plt.tight_layout()
plt.savefig('p1_chart2_cpa_vs_conversions.png', dpi=150)
plt.close()

# Chart 3: Spend distribution by industry
ind_spend = df.groupby('industry')['ad_spend'].sum().sort_values(ascending=False)
plt.figure(figsize=(10, 5))
plt.barh(ind_spend.index, ind_spend.values, color='mediumseagreen', edgecolor='white')
plt.title('Total Spend by Industry', fontsize=13, fontweight='bold')
plt.xlabel('Total Ad Spend')
plt.tight_layout()
plt.savefig('p1_chart3_spend_by_industry.png', dpi=150)
plt.close()

# Chart 4: ROAS by Country
plt.figure(figsize=(10, 5))
bars = plt.bar(country_roas.index, country_roas.values, color='mediumpurple', edgecolor='white')
plt.axhline(account_avg_roas, color='red', linestyle='--', linewidth=1.2, label=f'Avg ROAS: {account_avg_roas:.2f}')
for bar, val in zip(bars, country_roas.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, f'{val:.2f}', ha='center', va='bottom', fontsize=8)
plt.title('ROAS by Country', fontsize=13, fontweight='bold')
plt.ylabel('ROAS')
plt.xlabel('Country')
plt.xticks(rotation=30, ha='right')
plt.legend()
plt.tight_layout()
plt.savefig('p1_chart4_roas_by_country.png', dpi=150)
plt.close()

# Flagged campaigns summary
high_cpa_campaigns = df[df['High_CPA_Flag'] == True]
low_roas_campaigns = df[df['Low_ROAS_Flag'] == True]
underperforming = df[df['Flags'].notna() & df['Flags'].str.contains('Underperforming', na=False)]

print('=== Google Ads Account Audit ===')
print(f'Account Avg ROAS: {account_avg_roas:.2f}')
print(f'Account Avg CPA: {account_avg_cpa:.2f}')
print(f'Account Avg CTR: {account_avg_ctr:.4f}')
print(f'Total Spend: {total_spend:,.2f}')
print(f'\nCampaign Type ROAS Breakdown:')
print(ct_roas)
print(f'\nIndustry ROAS Breakdown:')
print(ind_roas)
print(f'\nCountry ROAS Breakdown:')
print(country_roas)
print(f'\nOptimal Budget Reallocation by Campaign Type:')
print(optimal_alloc)
print(f'\nHigh CPA Campaigns: {len(high_cpa_campaigns)}')
print(f'Low ROAS Campaigns: {len(low_roas_campaigns)}')
print(f'Flagged Underperforming Rows: {len(underperforming)}')
print('\nTop 5 Performers by ROAS:')
print(top_performers.head())
print('\nBottom 5 Performers by ROAS:')
print(bottom_performers.head())

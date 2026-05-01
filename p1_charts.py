import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'axes.edgecolor': '#333333',
    'axes.labelcolor': '#222222',
    'xtick.color': '#222222',
    'ytick.color': '#222222',
    'axes.titleweight': 'bold',
    'axes.titlesize': 16,
})

DPI = 100
FIG_W, FIG_H = 12, 7  # 1200 x 700 at dpi=100

df = pd.read_csv('/home/user/workspace/google_ads_analysis.csv')
df['Flags'] = df['Flags'].fillna('').replace('', 'Healthy')

def add_footer(fig):
    fig.text(0.99, 0.01, 'Ashwin Kumar', ha='right', va='bottom',
             fontsize=9, color='#666666')

# -------- Chart 1: Horizontal bar — avg ROAS by campaign_type --------
avg_roas = df.groupby('campaign_type')['ROAS'].mean().sort_values()
colors = ['#d9534f' if v < 2.0 else '#5cb85c' for v in avg_roas.values]

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor='white')
ax.set_facecolor('white')
bars = ax.barh(avg_roas.index, avg_roas.values, color=colors, edgecolor='white')
ax.axvline(2.0, color='#888888', linestyle='--', linewidth=1, alpha=0.7)
ax.text(2.0, len(avg_roas) - 0.4, ' ROAS = 2.0 threshold',
        color='#666666', fontsize=9, va='top')

for bar, v in zip(bars, avg_roas.values):
    ax.text(v + max(avg_roas.values) * 0.01, bar.get_y() + bar.get_height() / 2,
            f'{v:.2f}', va='center', fontsize=10, color='#222222')

ax.set_title('ROAS by Campaign Type', pad=15)
ax.set_xlabel('Average ROAS')
ax.set_ylabel('Campaign Type')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', linestyle=':', alpha=0.5)
ax.set_axisbelow(True)
plt.tight_layout(rect=[0, 0.03, 1, 1])
add_footer(fig)
fig.savefig('/home/user/workspace/p1_chart1_roas.png', dpi=DPI,
            facecolor='white', bbox_inches=None)
plt.close(fig)

# -------- Chart 2: Scatter — CPA vs Conversions, size=ad_spend, color=Flags --------
flag_colors = {
    'Healthy': '#5cb85c',
    'Underperforming': '#f0ad4e',
    'High Cost': '#5bc0de',
    'Underperforming, High Cost': '#d9534f',
    'Low Relevance': '#9b59b6',
}

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor='white')
ax.set_facecolor('white')

# Scale bubble sizes
spend = df['ad_spend'].values
sizes = 20 + (spend - spend.min()) / (spend.max() - spend.min()) * 480

for flag, group in df.groupby('Flags'):
    s = 20 + (group['ad_spend'] - spend.min()) / (spend.max() - spend.min()) * 480
    ax.scatter(group['conversions'], group['CPA'],
               s=s, c=flag_colors.get(flag, '#888888'),
               alpha=0.55, edgecolors='white', linewidths=0.6,
               label=flag)

ax.set_title('CPA vs Conversions by Campaign', pad=15)
ax.set_xlabel('Conversions')
ax.set_ylabel('CPA')
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(linestyle=':', alpha=0.5)
ax.set_axisbelow(True)

leg = ax.legend(title='Flags', loc='upper right', frameon=True,
                framealpha=0.95, edgecolor='#cccccc')
# Normalize legend marker sizes
for handle in leg.legend_handles:
    handle.set_sizes([80])

# Bubble-size note
ax.text(0.01, 0.98, 'Bubble size ∝ ad spend',
        transform=ax.transAxes, fontsize=9, color='#666666',
        va='top', ha='left',
        bbox=dict(facecolor='white', edgecolor='#dddddd', boxstyle='round,pad=0.3'))

plt.tight_layout(rect=[0, 0.03, 1, 1])
add_footer(fig)
fig.savefig('/home/user/workspace/p1_chart2_cpa_vs_conv.png', dpi=DPI,
            facecolor='white', bbox_inches=None)
plt.close(fig)

# -------- Chart 3: Top 10 high-spend low-ROAS --------
low = df[df['ROAS'] < 2.0].sort_values('ad_spend', ascending=False).head(10).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI, facecolor='white')
ax.set_facecolor('white')

# Distinct color per campaign_type
unique_types = low['campaign_type'].unique()
palette = ['#4e79a7', '#f28e2b', '#e15759', '#76b7b2', '#59a14f',
           '#edc948', '#b07aa1', '#ff9da7', '#9c755f', '#bab0ac']
type_color = {t: palette[i % len(palette)] for i, t in enumerate(unique_types)}

x = np.arange(len(low))
bar_colors = [type_color[t] for t in low['campaign_type']]
bars = ax.bar(x, low['ad_spend'], color=bar_colors, edgecolor='white')

# Labels above bars
for bar, val, roas in zip(bars, low['ad_spend'], low['ROAS']):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f'${val:,.0f}\nROAS {roas:.2f}',
            ha='center', va='bottom', fontsize=8.5, color='#333333')

ax.set_xticks(x)
# Use rank labels so bars stay distinguishable when types repeat
ax.set_xticklabels([f'#{i+1}\n{t}' for i, t in enumerate(low['campaign_type'])],
                   fontsize=10)

ax.set_title('Top 10 High-Spend Low-ROAS Campaigns', pad=15)
ax.set_xlabel('Campaign (ranked by spend)')
ax.set_ylabel('Ad Spend')
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', linestyle=':', alpha=0.5)
ax.set_axisbelow(True)
ax.margins(y=0.18)

# Legend by campaign_type
from matplotlib.patches import Patch
handles = [Patch(facecolor=c, label=t) for t, c in type_color.items()]
ax.legend(handles=handles, title='Campaign Type', loc='upper right',
          frameon=True, framealpha=0.95, edgecolor='#cccccc')

plt.tight_layout(rect=[0, 0.03, 1, 1])
add_footer(fig)
fig.savefig('/home/user/workspace/p1_chart3_top10.png', dpi=DPI,
            facecolor='white', bbox_inches=None)
plt.close(fig)

print("Done")
print("Avg ROAS by type:")
print(avg_roas)
print("\nTop 10 low-ROAS high-spend:")
print(low[['campaign_type', 'ad_spend', 'ROAS', 'CPA', 'conversions']])

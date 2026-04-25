# google-ads-audit

## 1. Overview

I built this project as a portfolio-grade Google Ads Search Campaign Audit, using a synthetic but realistic multi-platform ads dataset to demonstrate how I diagnose paid media performance end to end. It is written for e-commerce and performance marketing hiring managers who want to see how I move from raw campaign data to clear findings, recommendations, and a 30-day action plan. My goal is to show practical judgment, not just a dashboard — every flag and recommendation is grounded in the underlying numbers.

## 2. Dataset

I work from a multi-platform ads performance dataset that includes daily campaign rows for Google Ads, Meta Ads, and TikTok Ads, with impressions, clicks, spend, conversions, and revenue across industries and countries. The dataset is based on the public Kaggle release [Global Ads Performance — Google, Meta, TikTok](https://www.kaggle.com/datasets/nudratabbas/global-ads-performance-google-meta-tiktok), which I treat as a synthetic but realistic benchmarking source.

For this audit I filter the dataset to the Google Ads subset only, save it as `google_ads_analysis.csv`, and use it as the single source of truth for every chart, table, and finding in the report.

## 3. Methodology

- I filter the raw dataset to Google Ads rows only and segment by `campaign_type` across Search, Shopping, Display, and Video.
- I recompute the core performance metrics row by row: CTR (clicks ÷ impressions), CPC (spend ÷ clicks), CPA (spend ÷ conversions), ROAS (revenue ÷ spend), and Conversion Rate (conversions ÷ clicks).
- I apply three diagnostic flags:
  - **Underperforming** — ROAS < 2.0
  - **High Cost** — CPA greater than 1.3× the Google Ads platform mean
  - **Low Relevance** — CTR < 1%
  - When a row matches multiple rules, I combine the flags in a single `Flags` column.
- I build three charts directly from `google_ads_analysis.csv`:
  - Average ROAS by campaign type (horizontal bar, threshold-coloured)
  - CPA vs conversions bubble scatter, sized by spend and coloured by flag
  - Top 10 high-spend, low-ROAS campaigns
- I summarise everything into a 2-page audit report, `google_ads_audit.pdf`, covering executive summary, performance overview, key findings, visual evidence, fix recommendations, and a 30-day action plan.

## 4. Key Findings

1. **Overall ROAS sits at 4.11x against a 2026 e-commerce benchmark of 4.50x**, so the account is broadly healthy on revenue return but trails benchmark by roughly 9%, leaving a meaningful efficiency gap to close.
2. **About 38.7% of total Google Ads spend (≈ $2.46M of $6.35M) sits inside underperforming campaigns** that returned only 1.12x ROAS, which is the single largest pool of budget I would reallocate first.
3. **Search is the most scalable campaign type** at 4.79x average ROAS and the lowest average CPA across the four types, so my recommendation is to consolidate budget into top-quartile Search campaigns while restructuring the weakest Display and Shopping rows.

## 5. Tools

- **Python (Pandas, NumPy)** — data filtering, metric recomputation, flagging logic, and aggregation.
- **Matplotlib** — all three portfolio charts (bar, bubble scatter, ranked bar) at 1200×700 PNG.
- **ReportLab** — the 2-page audit PDF with embedded fonts, KPI cards, and structured tables.
- **Google Looker Studio** — optional interactive dashboard layer for stakeholders who prefer a live view over a static PDF.
- **GitHub** — version control and public hosting of the repository.

## 6. How to Reproduce

1. Clone the repo: `git clone https://github.com/ashwinkumarglbimr18-cmd/google-ads-audit.git` and `cd google-ads-audit`.
2. Install dependencies: `pip install pandas numpy matplotlib reportlab` (Pandas, NumPy, Matplotlib, ReportLab).
3. Open the analysis script (or notebook) and point the input path to `google_ads_analysis.csv` in the repo root.
4. Run the analysis script to regenerate the three charts (`p1_chart1_roas.png`, `p1_chart2_cpa_vs_conv.png`, `p1_chart3_top10.png`) and the final report (`google_ads_audit.pdf`).

## 7. Contact

I'm happy to discuss the methodology, findings, or extensions — reach me at **ashwin.kumar.glbimr18@gmail.com** or on LinkedIn at **https://www.linkedin.com/in/ashwin-kumar-180816174/>**.

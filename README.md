# 📱 PhonePe Pulse · India UPI Transaction Analytics

> **Where should PhonePe focus merchant acquisition efforts in 2025?**
> This project answers that question using 6 years of real transaction data, SQL analysis, and ML forecasting.

🔗 **[Live Dashboard →](https://phonepe-pulse-analysis.onrender.com)** *([https://phonepe-pulse-analysis.onrender.com](https://phonepe-pulse-analysis.onrender.com))*
📁 **[Dataset](https://github.com/PhonePe/pulse)** · PhonePe Pulse GitHub (official, open-source)

---

## Key Findings

| Finding | Insight |
|---|---|
| 🚀 **40× growth** | India UPI transaction value grew 40× from 2018 to 2024 |
| 📍 **Manipur leads** | Fastest YoY growth state — signals Northeast India opportunity |
| ⚠️ **Churn risk** | Several states have high users but <5 transactions/user |
| 🎉 **Festive spike** | Q4 (Oct–Dec) consistently drives the highest transaction volumes |
| 🏆 **Top 3 states** | Maharashtra, Karnataka, Telangana account for ~55% of all value |

---

## Tech Stack

| Layer | Tools |
|---|---|
| Data processing | Python · Pandas · NumPy |
| SQL analysis | SQLite · 7 business queries with CTEs & window functions |
| Visualisation | Plotly · Seaborn · Matplotlib |
| Dashboard | Streamlit (3-page interactive app) |
| ML forecasting | Facebook Prophet (multiplicative seasonality) |
| Deployment | Streamlit Cloud |

---

## Project Structure

```
phonepe-pulse-analysis/
├── data/
│   ├── agg_transactions.csv      ← cleaned transaction data
│   ├── agg_users.csv             ← cleaned user data
│   ├── phonepe.db                ← SQLite database
│   ├── national_forecast.csv     ← Prophet forecast output
│   └── forecast_combined.csv     ← actual + forecast merged
├── notebooks/
│   ├── 01_data_loading.ipynb     ← JSON → CSV pipeline
│   ├── 02_eda.ipynb              ← exploratory analysis
│   ├── 03_sql_analysis.ipynb     ← 7 business SQL queries
│   └── 04_forecasting.ipynb      ← Prophet ML model
├── dashboard/
│   └── app.py                    ← 3-page Streamlit app
├── sql/
│   └── business_queries.sql      ← all SQL queries
└── README.md
```

---

## SQL Highlights

The project includes 7 business-focused SQL queries demonstrating:

- `LAG()` window function for YoY growth calculation
- `RANK() OVER (PARTITION BY state)` for per-state rankings
- Nested CTEs for multi-step aggregations
- `JOIN` across transactions and users tables for churn analysis
- `CASE WHEN` for engagement labelling

Example — YoY growth using window functions:
```sql
SELECT year,
       ROUND(SUM(amount_cr), 0) AS total_amount_cr,
       ROUND(
           (SUM(amount_cr) - LAG(SUM(amount_cr)) OVER (ORDER BY year))
           * 100.0 / LAG(SUM(amount_cr)) OVER (ORDER BY year),
       2) AS yoy_growth_pct
FROM transactions
GROUP BY year ORDER BY year
```

---

## ML Forecasting

Used **Facebook Prophet** with:
- Multiplicative seasonality (because UPI growth compounds)
- Quarterly frequency (no weekly/daily patterns)
- `changepoint_prior_scale=0.3` for flexible trend capture

Model forecasts the next 4 quarters of national UPI transaction volume and Manipur state-level volume specifically, with confidence intervals shown on the dashboard.

---

## Business Recommendation

Based on this analysis, PhonePe should prioritise **merchant acquisition in 3 tiers**:

1. **Tier 1 — Double down:** Manipur, Meghalaya, Nagaland (high growth, low base — maximum ROI)
2. **Tier 2 — Re-engage:** States with registered users but <5 txns/user (churn risk states)
3. **Tier 3 — Defend:** Maharashtra, Karnataka, Telangana (maintain dominance)

---

## How to Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/phonepe-pulse-analysis.git
cd phonepe-pulse-analysis
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

# Run notebooks in order: 01 → 02 → 03 → 04
# Then launch dashboard:
cd dashboard
streamlit run app.py
```

---

## Author

Built by **Palash Halder** · [LinkedIn](https://www.linkedin.com/in/palashhalder07/) · [GitHub](https://github.com/Palash1249)

*Data sourced from the official [PhonePe Pulse GitHub repository](https://github.com/PhonePe/pulse) under CDLA-Permissive-2.0 license.*
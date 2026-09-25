# ☕ Philippine Coffee Shop Market Intelligence Dashboard

An interactive market intelligence dashboard analyzing the Philippine coffee shop industry. Built with Python (pandas, plotly, Streamlit) as part of the agenticPH Labs portfolio.

## 📊 Dashboard Features

| Page | Description |
|------|-------------|
| **Market Overview** | Macro trends: market size, café sales, consumer behavior KPIs |
| **Competitor Analysis** | Store counts, growth rates, competitive landscape maps |
| **Geographic Distribution** | Regional presence, city density, supply-side analysis |
| **Pricing Analysis** | Menu price comparison, price ladders, value gap analysis |
| **Key Insights** | 13 data-driven business observations + methodology |

## 📁 Project Structure

```
p2-ph-market-intel/
├── data/
│   ├── raw/              # Raw data generation script
│   │   └── coffee_shop_data.py
│   └── processed/        # Cleaned CSVs, summaries, insights
│       ├── market_overview_clean.csv
│       ├── competitors_clean.csv
│       ├── pricing_data_clean.csv
│       ├── geographic_distribution_clean.csv
│       ├── pricing_summary.csv
│       ├── competitor_summary.json
│       └── business_insights.md
├── viz/                  # 13 interactive Plotly HTML charts
├── pipeline.py           # Data pipeline (clean → transform → analyze → export)
├── dashboard.py          # Streamlit dashboard application
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip or uv

### Installation

```bash
# Clone the repository
git clone https://github.com/agenticph-labs/p2-ph-market-intelligence.git
cd p2-ph-market-intelligence

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run the data pipeline
python3 pipeline.py

# Launch the dashboard
streamlit run dashboard.py
```

## 📈 Key Findings

| Finding | Detail |
|---------|--------|
| **Market Size** | PH coffee market: **$1.82B (2025)**, projected **$2.30B (2028)** — **7.3% CAGR** |
| **Market Leader** | **Starbucks** leads premium with **520 stores**; **Pickup Coffee** leads value with **500+** |
| **Fastest Growth** | **Zus Coffee**: **100% YoY** store growth (120 stores, targeting 200) |
| **Price Gap** | Starbucks (avg ₱183) is **2.6x** Zus Coffee (avg ₱70); a Grande Latte costs **2.5x** a Pickup Latte |
| **Import Dependency** | **94.3%** of coffee is imported — only 22,000 tons produced vs 365,000 tons imported |
| **Regional Concentration** | **Luzon (incl. NCR)** captures **63%** of revenue; Visayas (21%) and Mindanao (16%) underserved |
| **Consumer Habits** | **80%** of Filipino adults drink **2.5 cups/day**; **90%** of households stock coffee |
| **Franchising Boom** | **6 of 8** major chains offer franchising, driving rapid geographic expansion |

## 🛠️ Methodology

1. **Data Collection** — Public data from Euromonitor, USDA, Statista, company filings, news reports, and store locator websites (2024–2026)
2. **Data Pipeline** — pandas-based cleaning, transformation, derived metrics (YoY growth, CAGR, import dependency)
3. **Analysis** — Competitive positioning, price ladders, geographic density, market sizing
4. **Visualization** — 13 interactive Plotly charts
5. **Dashboard** — Multi-page Streamlit dashboard

## 🎯 Industry: Coffee Shops

Selected the **Philippine coffee shop industry** for its dynamic growth, clear market segmentation (premium vs. value), strong franchising tailwinds, and publicly available competitive data. The sector reflects broader PH consumer trends: urbanization, digital adoption, and value-conscious premiumization.

## 📝 License

MIT — See [LICENSE](LICENSE)

## 👤 Author

**agenticPH Labs** — Portfolio Project 2

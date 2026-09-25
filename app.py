#!/usr/bin/env python3
"""
PH Coffee Shop Market Intelligence — Interactive Streamlit Dashboard
Run: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json
import base64

st.set_page_config(
    page_title="PH Coffee Market Intelligence",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

PROC = Path("data/processed")
VIZ = Path("viz")


# ── HELPERS ───────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df_market = pd.read_csv(PROC / "market_overview_clean.csv")
    df_comp = pd.read_csv(PROC / "competitors_clean.csv")
    df_geo = pd.read_csv(PROC / "geographic_distribution_clean.csv")
    df_price = pd.read_csv(PROC / "pricing_data_clean.csv")
    df_consumer = pd.read_csv(PROC / "consumer_behavior_clean.csv")
    df_region = pd.read_csv(PROC / "regional_market_breakdown_clean.csv")
    df_prod = pd.read_csv(PROC / "coffee_production_clean.csv")
    price_summary = pd.read_csv(PROC / "pricing_summary.csv")
    with open(PROC / "competitor_summary.json") as f:
        comp_summary = json.load(f)
    with open(PROC / "business_insights.md") as f:
        insights = f.read()
    return (df_market, df_comp, df_geo, df_price, df_consumer,
            df_region, df_prod, price_summary, comp_summary, insights)


def read_html(path):
    with open(path) as f:
        return f.read()


def render_svg(text, size=60):
    """Render a large emoji-style header."""
    return f"<span style='font-size:{size}px;'>{text}</span>"


df_market, df_comp, df_geo, df_price, df_consumer, df_region, df_prod, price_summary, comp_summary, insights_md = load_data()

# ── SIDEBAR ───────────────────────────────────────────────────────────
st.sidebar.markdown("## ☕ PH Coffee Intelligence")
st.sidebar.markdown("***Philippines Coffee Shop Market — Data-Driven Dashboard***")
st.sidebar.markdown("---")
st.sidebar.markdown("### Navigate")
pages = [
    "📊 Market Overview",
    "🏪 Competitor Analysis",
    "🗺️ Geographic Distribution",
    "💰 Pricing Analysis",
    "📈 Key Insights & Methodology",
]
choice = st.sidebar.radio("Go to", pages)
st.sidebar.markdown("---")
st.sidebar.markdown("**Data Sources**")
st.sidebar.markdown("Euromonitor, USDA, Statista, World Coffee Portal, company filings, news reports (2024–2026)")
st.sidebar.markdown("---")
st.sidebar.markdown("**Industry: Coffee Shops**")
st.sidebar.markdown(f"**8 major chains** tracked")
st.sidebar.markdown(f"**{df_price['drink'].nunique()} menu items** priced")
st.sidebar.markdown(f"**{len(df_geo)} city/province areas** mapped")


# ── PAGE 1: MARKET OVERVIEW ──────────────────────────────────────────
if choice == "📊 Market Overview":
    st.markdown("# 📊 Philippine Coffee Market — Overview")
    st.markdown("Macro-level market trends, growth trajectory, and key indicators.")

    # KPI row
    col1, col2, col3, col4 = st.columns(4)
    latest = df_market.iloc[-1]
    col1.metric("Market Size (2028E)", f"${latest['market_size_billion_usd']:.2f}B",
                f"{latest['yoy_growth_pct']:.1f}% YoY")
    col2.metric("Café/Bar Sales (2026E)", f"$1.86B",
                "7.1% YoY")
    col3.metric("Total Outlets (2028E)", f"{latest['total_coffee_outlets_estimate']:,.0f}",
                f"+{latest['specialist_coffee_shops_outlets'] - df_market.iloc[-2]['specialist_coffee_shops_outlets']} specialist")
    col4.metric("CAGR (2019–2028)", "7.3%", "Projected")

    st.markdown("---")

    # Market size & cafe sales side by side
    col1, col2 = st.columns(2)
    with col1:
        fig = px.line(df_market, x="year", y="market_size_billion_usd",
                      title="Market Size (Billion USD)",
                      markers=True, template="plotly_white")
        fig.update_traces(line=dict(width=3, color="#4A2C2A"))
        fig.update_layout(yaxis_title="Billion USD", xaxis=dict(dtick=1))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.line(df_market, x="year", y="cafes_bars_sales_billion_usd",
                       title="Café & Bar Sales (Billion USD)",
                       markers=True, template="plotly_white")
        fig2.update_traces(line=dict(width=3, color="#8B4513"))
        fig2.update_layout(yaxis_title="Billion USD", xaxis=dict(dtick=1))
        st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(read_html(VIZ / "v11_outlets_forecast.html"), use_container_width=True)

    with col2:
        st.plotly_chart(read_html(VIZ / "v9_regional_revenue.html"), use_container_width=True)

    st.markdown("### Consumer Behavior Snapshot")
    cons_display = df_consumer[df_consumer["metric"].isin([
        "Filipinos who drink coffee daily (%)",
        "Average cups per day",
        "Per capita consumption (kg/year)",
        "Coffee shop visit frequency (times/week)",
        "Avg spend per café visit (PHP)",
        "Premium coffee willing to pay more (%)",
    ])]
    cols = st.columns(3)
    for i, (_, row) in enumerate(cons_display.iterrows()):
        with cols[i % 3]:
            st.metric(row["metric"], str(row["value"]), row["source"])


# ── PAGE 2: COMPETITOR ANALYSIS ──────────────────────────────────────
elif choice == "🏪 Competitor Analysis":
    st.markdown("# 🏪 Competitor Analysis")
    st.markdown("Head-to-head comparison of major coffee chains operating in the Philippines.")

    # Competitive landscape
    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(read_html(VIZ / "v13_competitive_landscape.html"), use_container_width=True)
    with col2:
        st.plotly_chart(read_html(VIZ / "v3_store_comparison.html"), use_container_width=True)

    # Growth and comparison
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(read_html(VIZ / "v8_growth_rate.html"), use_container_width=True)
    with col2:
        # Consumer vs chain table
        st.markdown("### Chain Details")
        comp_display = df_comp[["chain", "type", "stores_2025", "avg_cup_price_php",
                                 "app_ordering", "franchise_available", "price_tier"]]
        comp_display.columns = ["Chain", "Type", "Stores (2025)", "Avg Cup (₱)",
                                 "App Ordering", "Franchise", "Tier"]
        st.dataframe(comp_display, hide_index=True, use_container_width=True)

    # Detailed cards
    st.markdown("### Chain Profiles")
    for c in comp_summary:
        with st.expander(f"**{c['chain']}** — {c['type']} ({c['stores_2025']} stores, ₱{c['avg_cup_price_php']}/cup avg)"):
            st.markdown(f"*{c['key_notes']}*")
            cols = st.columns(4)
            cols[0].metric("Stores", c['stores_2025'])
            cols[1].metric("Avg Cup ₱", c['avg_cup_price_php'])
            cols[2].metric("App Ordering", "✅" if c['app_ordering'] else "❌")
            cols[3].metric("Franchise", "✅" if c['franchise_available'] else "❌")


# ── PAGE 3: GEOGRAPHIC DISTRIBUTION ──────────────────────────────────
elif choice == "🗺️ Geographic Distribution":
    st.markdown("# 🗺️ Geographic Distribution")
    st.markdown("Chain store presence across Philippine regions and key cities.")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(read_html(VIZ / "v4_geo_distribution.html"), use_container_width=True)
    with col2:
        st.plotly_chart(read_html(VIZ / "v12_city_density.html"), use_container_width=True)

    st.markdown("### Regional Market Breakdown")
    col1, col2 = st.columns(2)
    with col1:
        st.dataframe(df_region, hide_index=True, use_container_width=True)
    with col2:
        st.plotly_chart(read_html(VIZ / "v9_regional_revenue.html"), use_container_width=True)

    # Filter by region
    st.markdown("### Store Distribution by Region & Chain")
    region_choice = st.selectbox("Select region", ["All"] + sorted(df_geo["region"].unique()))
    if region_choice != "All":
        filtered = df_geo[df_geo["region"] == region_choice]
    else:
        filtered = df_geo

    chain_cols_geo = ["starbucks", "pickup", "zus", "bos", "cb_tl", "tim_hortons", "jco"]
    display_cols = ["city_province", "region"] + chain_cols_geo + ["independents_est"]
    st.dataframe(
        filtered[display_cols].rename(columns={
            "city_province": "City", "independents_est": "Independents (est)"
        }),
        hide_index=True, use_container_width=True
    )

    st.markdown("### Production vs Imports (Supply Side)")
    st.plotly_chart(read_html(VIZ / "v10_production_imports.html"), use_container_width=True)
    st.caption("The Philippines imports >90% of its coffee — a massive opportunity for local production.")


# ── PAGE 4: PRICING ANALYSIS ─────────────────────────────────────────
elif choice == "💰 Pricing Analysis":
    st.markdown("# 💰 Pricing Analysis")
    st.markdown("Comparative pricing across chains, drink categories, and value analysis.")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(read_html(VIZ / "v5_price_comparison.html"), use_container_width=True)
    with col2:
        st.plotly_chart(read_html(VIZ / "v6_americano_ladder.html"), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(read_html(VIZ / "v7_latte_ladder.html"), use_container_width=True)
    with col2:
        st.markdown("### Price Summary by Chain")
        st.dataframe(price_summary.round(1), hide_index=True, use_container_width=True)

    # Interactive price explorer
    st.markdown("### Interactive Price Explorer")
    col1, col2 = st.columns(2)
    with col1:
        selected_chain = st.selectbox("Select chain", sorted(df_price["chain"].unique()))
    with col2:
        selected_drink = st.selectbox("Select drink type", ["All"] + sorted(df_price["drink"].unique()))
    q = df_price[df_price["chain"] == selected_chain]
    if selected_drink != "All":
        q = q[q["drink"] == selected_drink]
    st.dataframe(q, hide_index=True, use_container_width=True)

    st.markdown("### Price Gap Analysis")
    col1, col2, col3 = st.columns(3)
    sb_avg = price_summary[price_summary["chain"] == "Starbucks"]["avg_price"].values[0]
    pu_avg = price_summary[price_summary["chain"] == "Pickup Coffee"]["avg_price"].values[0]
    zus_avg = price_summary[price_summary["chain"] == "Zus Coffee"]["avg_price"].values[0]
    col1.metric("Starbucks Avg", f"₱{sb_avg:.0f}", f"{sb_avg/pu_avg:.1f}x Pickup")
    col2.metric("Pickup Coffee Avg", f"₱{pu_avg:.0f}", f"{(pu_avg/sb_avg-1)*100:.0f}% vs SB")
    col3.metric("Zus Coffee Avg", f"₱{zus_avg:.0f}", f"{(zus_avg/sb_avg-1)*100:.0f}% vs SB")


# ── PAGE 5: INSIGHTS ─────────────────────────────────────────────────
elif choice == "📈 Key Insights & Methodology":
    st.markdown("# 📈 Key Business Insights & Methodology")

    # Insights
    st.markdown("## Key Business Observations")
    st.markdown(insights_md)

    st.markdown("---")
    st.markdown("## Methodology")

    st.markdown("""
    ### Data Collection
    - **Public market reports** from Euromonitor, USDA (Foreign Agricultural Service), and Statista
    - **Company filings** and press releases for store counts and expansion plans
    - **Menu pricing** sourced from official GrabFood / official chain websites (2025–2026)
    - **News reports** from Philstar, BusinessWorld, Bloomberg, Inquirer, World Coffee Portal, Verdict Food Service
    - **Geographic data** estimated from store locator pages of each chain's website

    ### Pipeline
    1. **Raw data** → curated CSV files in `data/raw/`
    2. **Cleaning** → pandas cleanup, type coercion, derived metrics (YoY growth, import dependency)
    3. **Analysis** → market sizing, CAGR calculation, competitive positioning, price ladders
    4. **Visualization** → 13 interactive Plotly charts covering market trends, competition, geography, pricing
    5. **Dashboard** → Streamlit with 5 tabbed pages for exploration
    6. **Insights** → 13 actionable business observations derived from the data

    ### Repository Structure
    ```
    p2-ph-market-intel/
    ├── data/
    │   ├── raw/        # Raw CSV generation script
    │   └── processed/  # Cleaned CSVs, summary JSON, insights markdown
    ├── viz/            # 13 interactive Plotly HTML charts
    ├── pipeline.py     # Data pipeline (clean → transform → analyze → visualize)
    ├── dashboard.py    # Streamlit dashboard
    ├── requirements.txt
    └── README.md
    ```

    ### Key Data Quality Notes
    - Store counts are approximate as of mid-2025 to early 2026, sourced from company announcements
    - Menu prices are as listed on GrabFood / official sites and may vary by location
    - Independent coffee shop counts are estimates based on market research reports
    - Outlet totals are projected based on announced growth targets
    """)

st.sidebar.markdown("---")
st.sidebar.markdown("**Built with** Streamlit • Pandas • Plotly")
st.sidebar.markdown("**2026**")

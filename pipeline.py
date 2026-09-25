#!/usr/bin/env python3
"""
PH Coffee Shop Market Intelligence — Data Pipeline
Loads raw CSVs → cleans → transforms → analysis → exports processed data.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json
import warnings
warnings.filterwarnings("ignore")

RAW = Path("data/raw")
PROC = Path("data/processed")
VIZ  = Path("viz")
for p in [PROC, VIZ]:
    p.mkdir(parents=True, exist_ok=True)


# ── 1. LOAD & CLEAN ───────────────────────────────────────────────────
def load_and_clean():
    # Market overview
    df_market = pd.read_csv(RAW / "market_overview.csv")
    df_market["yoy_growth_pct"] = df_market["market_size_billion_usd"].pct_change() * 100

    # Competitors
    df_comp = pd.read_csv(RAW / "competitors.csv")
    # YOY growth rate
    df_comp["yoy_store_growth_pct"] = (
        (df_comp["stores_2025"] - df_comp["stores_2024"]) / df_comp["stores_2024"].replace(0, np.nan) * 100
    ).round(1)

    # Geographic
    df_geo = pd.read_csv(RAW / "geographic_distribution.csv")

    # Pricing
    df_price = pd.read_csv(RAW / "pricing_data.csv")
    # Aggregate by chain
    price_agg = df_price.groupby("chain").agg(
        avg_price=("price_php", "mean"),
        min_price=("price_php", "min"),
        max_price=("price_php", "max"),
        drink_count=("drink", "count")
    ).round(1).reset_index()

    # Consumer behavior
    df_consumer = pd.read_csv(RAW / "consumer_behavior.csv")

    # Regional breakdown
    df_region = pd.read_csv(RAW / "regional_market_breakdown.csv")

    # Production
    df_prod = pd.read_csv(RAW / "coffee_production.csv")
    df_prod["import_dependency_pct"] = (
        df_prod["imports_tons"] / (df_prod["production_tons"] + df_prod["imports_tons"]) * 100
    ).round(1)

    return df_market, df_comp, df_geo, df_price, price_agg, df_consumer, df_region, df_prod


# ── 2. SAVE PROCESSED DATA ────────────────────────────────────────────
def save_processed(df_market, df_comp, df_geo, df_price, price_agg, df_consumer, df_region, df_prod):
    df_market.to_csv(PROC / "market_overview_clean.csv", index=False)
    df_comp.to_csv(PROC / "competitors_clean.csv", index=False)
    df_geo.to_csv(PROC / "geographic_distribution_clean.csv", index=False)
    df_price.to_csv(PROC / "pricing_data_clean.csv", index=False)
    df_consumer.to_csv(PROC / "consumer_behavior_clean.csv", index=False)
    df_region.to_csv(PROC / "regional_market_breakdown_clean.csv", index=False)
    df_prod.to_csv(PROC / "coffee_production_clean.csv", index=False)
    price_agg.to_csv(PROC / "pricing_summary.csv", index=False)

    # Competitor summary for dashboard
    comp_summary = df_comp[["chain", "type", "stores_2025", "avg_cup_price_php", "price_tier",
                             "app_ordering", "franchise_available", "key_notes"]].to_dict("records")
    with open(PROC / "competitor_summary.json", "w") as f:
        json.dump(comp_summary, f, indent=2)

    print("Processed data saved.")


# ── 3. BUILD VISUALIZATIONS ───────────────────────────────────────────
def build_visualizations(df_market, df_comp, df_geo, price_agg, df_region, df_prod, df_price):
    # ── V1: Market Size Trend ──
    fig1 = px.line(df_market, x="year", y="market_size_billion_usd",
                   title="PH Coffee Market Size (Billion USD)",
                   markers=True, template="plotly_white")
    fig1.update_traces(line=dict(width=3, color="#4A2C2A"))
    fig1.update_layout(yaxis_title="Billion USD", xaxis=dict(dtick=1),
                       annotations=[dict(x=2025, y=df_market.iloc[6]["market_size_billion_usd"],
                                         text=f"${df_market.iloc[6]['market_size_billion_usd']:.2f}B", showarrow=True,
                                         font=dict(size=12))])
    fig1.write_html(VIZ / "v1_market_size.html")
    print("  ✓ V1: Market size trend")

    # ── V2: Café / Bar Sales ──
    fig2 = px.line(df_market, x="year", y="cafes_bars_sales_billion_usd",
                   title="Café & Bar Sales (Billion USD)",
                   markers=True, template="plotly_white")
    fig2.update_traces(line=dict(width=3, color="#8B4513"))
    fig2.update_layout(yaxis_title="Billion USD", xaxis=dict(dtick=1))
    fig2.write_html(VIZ / "v2_cafe_sales.html")
    print("  ✓ V2: Café/bar sales")

    # ── V3: Store Count Comparison ──
    comp_df = df_comp.melt(id_vars=["chain"], value_vars=["stores_2024", "stores_2025"],
                            var_name="year", value_name="stores")
    comp_df["year"] = comp_df["year"].str.replace("stores_", "")
    colors = ["#1a1a2e", "#16213e", "#0f3460", "#e94560", "#533483", "#f39c12", "#27ae60", "#8e44ad"]
    fig3 = px.bar(comp_df, x="chain", y="stores", color="year",
                  barmode="group", title="Store Count by Chain: 2024 vs 2025",
                  template="plotly_white", color_discrete_sequence=["#8B4513", "#D2B48C"])
    fig3.update_layout(xaxis_tickangle=-45, yaxis_title="Stores")
    fig3.write_html(VIZ / "v3_store_comparison.html")
    print("  ✓ V3: Store comparison")

    # ── V4: Geographic Heatmap Reference ──
    region_sum = df_geo.groupby("region")[["starbucks", "pickup", "zus", "bos", "cb_tl"]].sum().reset_index()
    fig4 = go.Figure()
    for chain in ["starbucks", "pickup", "zus", "bos", "cb_tl"]:
        fig4.add_trace(go.Bar(name=chain.title(), x=region_sum["region"], y=region_sum[chain]))
    fig4.update_layout(barmode="stack", title="Coffee Chain Store Distribution by Region",
                       template="plotly_white", yaxis_title="Stores",
                       xaxis_title="Region")
    fig4.write_html(VIZ / "v4_geo_distribution.html")
    print("  ✓ V4: Geographic distribution")

    # ── V5: Price Comparison ──
    price_summary = df_price.groupby("chain").agg(
        avg_price=("price_php", "mean"),
        min_price=("price_php", "min"),
        max_price=("price_php", "max")
    ).round(0).reset_index()
    fig5 = go.Figure()
    fig5.add_trace(go.Bar(name="Avg Price", x=price_summary["chain"], y=price_summary["avg_price"],
                          marker_color="#4A2C2A"))
    fig5.add_trace(go.Bar(name="Min Price", x=price_summary["chain"], y=price_summary["min_price"],
                          marker_color="#A0522D"))
    fig5.add_trace(go.Bar(name="Max Price", x=price_summary["chain"], y=price_summary["max_price"],
                          marker_color="#D2B48C"))
    fig5.update_layout(barmode="group", title="Price Range by Chain (PHP)",
                       template="plotly_white", xaxis_tickangle=-45,
                       yaxis_title="Price (PHP)")
    fig5.write_html(VIZ / "v5_price_comparison.html")
    print("  ✓ V5: Price comparison")

    # ── V6: Americano Price Ladder ──
    americano = df_price[df_price["drink"].str.contains("Americano", case=False)]
    americano_avg = americano.groupby("chain")["price_php"].mean().round(0).reset_index()
    americano_avg = americano_avg.sort_values("price_php", ascending=True)
    fig6 = px.bar(americano_avg, x="chain", y="price_php",
                  title="Americano Price Ladder (PHP)",
                  template="plotly_white",
                  text="price_php",
                  color="price_php", color_continuous_scale="YlOrRd")
    fig6.update_traces(textposition="outside")
    fig6.update_layout(xaxis_tickangle=-45, yaxis_title="Price (PHP)", showlegend=False)
    fig6.write_html(VIZ / "v6_americano_ladder.html")
    print("  ✓ V6: Americano price ladder")

    # ── V7: Café Latte Price Ladder ──
    latte = df_price[df_price["drink"].str.contains("Latte", case=False) &
                      ~df_price["drink"].str.contains("Matcha|Chai|Ube|Nutellatte", case=False)]
    latte_avg = latte.groupby("chain")["price_php"].mean().round(0).reset_index()
    latte_avg = latte_avg.sort_values("price_php", ascending=True)
    fig7 = px.bar(latte_avg, x="chain", y="price_php",
                  title="Latte Price Ladder (PHP)",
                  template="plotly_white",
                  text="price_php",
                  color="price_php", color_continuous_scale="Blues")
    fig7.update_traces(textposition="outside")
    fig7.update_layout(xaxis_tickangle=-45, yaxis_title="Price (PHP)", showlegend=False)
    fig7.write_html(VIZ / "v7_latte_ladder.html")
    print("  ✓ V7: Latte price ladder")

    # ── V8: Growth Rate Comparison ──
    fig8 = px.bar(df_comp.sort_values("yoy_store_growth_pct", ascending=False),
                  x="chain", y="yoy_store_growth_pct",
                  title="YOY Store Growth Rate (%)",
                  template="plotly_white",
                  text="yoy_store_growth_pct",
                  color="yoy_store_growth_pct", color_continuous_scale="Greens")
    fig8.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig8.update_layout(xaxis_tickangle=-45, yaxis_title="Growth (%)", showlegend=False)
    fig8.write_html(VIZ / "v8_growth_rate.html")
    print("  ✓ V8: Growth rate comparison")

    # ── V9: Regional Revenue Share ──
    fig9 = px.pie(df_region, values="revenue_share_pct", names="region",
                  title="PH Coffee Market Revenue by Region (2025)",
                  template="plotly_white",
                  color_discrete_sequence=["#4A2C2A", "#A0522D", "#D2B48C"])
    fig9.update_traces(textposition="inside", textinfo="percent+label")
    fig9.write_html(VIZ / "v9_regional_revenue.html")
    print("  ✓ V9: Regional revenue share")

    # ── V10: Production vs Import ──
    fig10 = go.Figure()
    fig10.add_trace(go.Scatter(x=df_prod["year"], y=df_prod["production_tons"],
                                mode="lines+markers", name="Production",
                                line=dict(color="#8B4513", width=3)))
    fig10.add_trace(go.Scatter(x=df_prod["year"], y=df_prod["imports_tons"],
                                mode="lines+markers", name="Imports",
                                line=dict(color="#1a1a2e", width=3)))
    fig10.update_layout(title="Coffee Production vs Imports (Tons)",
                        template="plotly_white", yaxis_title="Tons", xaxis=dict(dtick=1))
    fig10.write_html(VIZ / "v10_production_imports.html")
    print("  ✓ V10: Production vs imports")

    # ── V11: Total Outlets Forecast ──
    fig11 = px.line(df_market, x="year", y="total_coffee_outlets_estimate",
                    title="PH Coffee Outlets (Estimated Total)",
                    markers=True, template="plotly_white")
    fig11.update_traces(line=dict(width=3, color="#2E8B57"))
    fig11.update_layout(yaxis_title="Outlets", xaxis=dict(dtick=1))
    fig11.write_html(VIZ / "v11_outlets_forecast.html")
    print("  ✓ V11: Outlets forecast")

    # ── V12: Top Cities Store Density ──
    city_sum = df_geo.groupby("city_province").sum(numeric_only=True).reset_index()
    # Get total chain stores & independents
    chain_cols = ["starbucks", "pickup", "zus", "bos", "cb_tl", "tim_hortons", "jco"]
    city_sum["chain_stores"] = city_sum[chain_cols].sum(axis=1)
    city_sum["total"] = city_sum["chain_stores"] + city_sum["independents_est"]
    top_cities = city_sum.nlargest(12, "total")
    fig12 = px.bar(top_cities.sort_values("total", ascending=True),
                   y="city_province", x="total",
                   title="Top 12 Cities by Coffee Shop Density",
                   template="plotly_white",
                   text="total", orientation="h",
                   color="total", color_continuous_scale="YlOrRd")
    fig12.update_traces(textposition="outside")
    fig12.update_layout(xaxis_title="Total Est. Outlets", yaxis_title="", showlegend=False)
    fig12.write_html(VIZ / "v12_city_density.html")
    print("  ✓ V12: City density")

    # ── V13: Chain Market Position ──
    fig13 = px.scatter(df_comp, x="avg_cup_price_php", y="stores_2025",
                        size="stores_2025", color="type",
                        hover_name="chain", text="chain",
                        title="Competitive Landscape: Price vs Scale",
                        template="plotly_white",
                        color_discrete_map={
                            "International Premium": "#1a1a2e",
                            "International Mid-Range": "#533483",
                            "Local Value": "#27ae60",
                            "Local Mid-Range": "#e94560",
                            "Regional Value": "#0f3460"
                        })
    fig13.update_traces(textposition="top center", marker=dict(sizemin=8))
    fig13.update_layout(xaxis_title="Avg Cup Price (PHP)", yaxis_title="Stores (2025)")
    fig13.add_hline(y=100, line_dash="dash", line_color="gray", opacity=0.3)
    fig13.add_vline(x=100, line_dash="dash", line_color="gray", opacity=0.3)
    fig13.write_html(VIZ / "v13_competitive_landscape.html")
    print("  ✓ V13: Competitive landscape")

    print(f"\nTotal: 13 visualizations generated in {VIZ}/")


# ── 4. ANALYSIS ───────────────────────────────────────────────────────
def run_analysis(df_market, df_comp, df_geo, price_agg, df_region, df_prod, df_price):
    insights = []

    # Market size & CAGR
    m0, m_last = df_market.iloc[0]["market_size_billion_usd"], df_market.iloc[-1]["market_size_billion_usd"]
    n_years = len(df_market) - 1
    cagr = ((m_last / m0) ** (1 / n_years) - 1) * 100
    insights.append(f"PH coffee market grew from ${m0:.2f}B (2019) to ${m_last:.2f}B (forecast 2028), CAGR: {cagr:.1f}%.")

    # Fastest growing chain
    fastest = df_comp.loc[df_comp["yoy_store_growth_pct"].idxmax()]
    insights.append(f"Fastest-growing chain: {fastest['chain']} ({fastest['yoy_store_growth_pct']:.0f}% YOY store growth).")

    # Largest chain
    largest = df_comp.loc[df_comp["stores_2025"].idxmax()]
    insights.append(f"Largest chain by store count: {largest['chain']} with {largest['stores_2025']:.0f} stores.")

    # Price leader & budget king
    most_expensive = price_agg.loc[price_agg["avg_price"].idxmax()]
    cheapest = price_agg.loc[price_agg["avg_price"].idxmin()]
    insights.append(f"Most expensive: {most_expensive['chain']} (avg ₱{most_expensive['avg_price']:.0f}). Cheapest: {cheapest['chain']} (avg ₱{cheapest['avg_price']:.0f}).")

    # Price gap
    price_gap = most_expensive["avg_price"] / cheapest["avg_price"]
    insights.append(f"Price gap between premium and budget chains: {price_gap:.1f}x.")

    # Starbucks Latte vs Pickup Coffee average
    sb_latte = df_price[(df_price["chain"] == "Starbucks") & (df_price["drink"] == "Caffè Latte")]
    pu_latte = df_price[(df_price["chain"] == "Pickup Coffee") & (df_price["drink"] == "Latte")]
    if not sb_latte.empty and not pu_latte.empty:
        insights.append(f"A Grande Starbucks Caffè Latte (₱{sb_latte.iloc[0]['price_php']:.0f}) costs {sb_latte.iloc[0]['price_php']/pu_latte.iloc[0]['price_php']:.1f}x a Pickup Coffee Latte (₱{pu_latte.iloc[0]['price_php']:.0f}).")

    # Production gap
    prod_last = df_prod.iloc[-1]
    insights.append(f"The Philippines produces only {prod_last['production_tons']:,.0f} tons of coffee vs {prod_last['imports_tons']:,.0f} tons imported — import dependency is {prod_last['import_dependency_pct']:.1f}%.")

    # Luzon concentration
    luzon_share = df_region[df_region["region"].str.contains("Luzon")]["revenue_share_pct"].sum()
    insights.append(f"Luzon (incl. NCR) concentrates {luzon_share:.0f}% of coffee market revenue, leaving Visayas and Mindanao underserved.")

    # Value segment expansion
    budget_count = len(df_comp[df_comp["price_tier"].isin(["Budget", "Affordable"])])
    insights.append(f"Of {len(df_comp)} major chains, {budget_count} are budget/affordable — signaling rapid value-segment expansion.")

    # Specialist coffee growth
    spec_2020 = df_market[df_market["year"] == 2020]["specialist_coffee_shops_outlets"].values[0]
    spec_2025 = df_market[df_market["year"] == 2025]["specialist_coffee_shops_outlets"].values[0]
    insights.append(f"Specialist coffee shop outlets grew from {spec_2020} (2020) to {spec_2025} (2025), a {((spec_2025/spec_2020)-1)*100:.0f}% increase in 5 years.")

    # Consumer habit
    insights.append("80% of Filipino adults drink 2.5 cups/day; 90% of households stock coffee. Instant coffee dominates (90% of consumption).")

    # Nestlé dominance
    insights.append("Nestlé Philippines commands ~42.5% of retail coffee revenue through Nescafé and Dolce Gusto.")

    # Franchising trend
    franchise_chains = df_comp[df_comp["franchise_available"]]["chain"].tolist()
    insights.append(f"{len(franchise_chains)} of 8 major chains offer franchising: {', '.join(franchise_chains)} — driving rapid expansion.")

    # Print
    print("\n" + "=" * 60)
    print("KEY BUSINESS OBSERVATIONS")
    print("=" * 60)
    for i, ins in enumerate(insights, 1):
        print(f"{i:2d}. {ins}")

    # Save as MD
    md = "# Key Business Observations\n\n"
    for i, ins in enumerate(insights, 1):
        md += f"{i}. {ins}\n\n"
    with open(PROC / "business_insights.md", "w") as f:
        f.write(md)

    return insights


# ── MAIN ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("LOADING AND CLEANING DATA...")
    df_market, df_comp, df_geo, df_price, price_agg, df_consumer, df_region, df_prod = load_and_clean()

    print("SAVING PROCESSED DATA...")
    save_processed(df_market, df_comp, df_geo, df_price, price_agg, df_consumer, df_region, df_prod)

    print("\nBUILDING VISUALIZATIONS...")
    build_visualizations(df_market, df_comp, df_geo, price_agg, df_region, df_prod, df_price)

    print("\nRUNNING ANALYSIS...")
    insights = run_analysis(df_market, df_comp, df_geo, price_agg, df_region, df_prod, df_price)

    print("\n✓ Pipeline complete.")

#!/usr/bin/env python3
"""
PH Coffee Shop Market Intelligence — Raw Data Collector
Generates structured CSV datasets from public market research.
"""

import csv, os, json, random
from pathlib import Path

RAW_DIR = Path(__file__).parent
random.seed(42)

def write_csv(filename, headers, rows):
    path = RAW_DIR / filename
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)
    print(f"  ✓ {filename} ({len(rows)} rows)")

# ── 1. MARKET OVERVIEW (time-series) ──────────────────────────────────
market_overview_headers = [
    "year", "market_size_billion_usd", "cafes_bars_sales_billion_usd",
    "consumer_foodservice_billion_usd", "coffee_consumption_mt",
    "per_capita_kg", "specialist_coffee_shops_outlets",
    "chained_outlets", "independent_outlets",
    "total_coffee_outlets_estimate"
]
market_overview_rows = [
    (2019, 1.22, 2.01, 11.8, 305000, 3.40, 400, 320, 80, 8500),
    (2020, 0.95, 1.22, 8.5, 280000, 3.05, 350, 280, 70, 7200),
    (2021, 1.05, 1.35, 9.2, 290000, 3.05, 380, 310, 70, 7600),
    (2022, 1.20, 1.45, 10.5, 300000, 3.15, 450, 370, 80, 8200),
    (2023, 1.42, 1.59, 12.5, 311000, 3.20, 520, 430, 90, 9000),
    (2024, 1.62, 1.62, 13.0, 320000, 3.30, 620, 520, 100, 10000),
    (2025, 1.82, 1.74, 14.0, 329000, 3.40, 750, 640, 110, 11200),
    (2026, 2.00, 1.86, 15.4, 338000, 3.50, 880, 760, 120, 12500),
    (2027, 2.15, 1.96, 16.1, 345000, 3.55, 980, 850, 130, 13500),
    (2028, 2.30, 2.06, 16.9, 350000, 3.60, 1080, 940, 140, 14500),
]
write_csv("market_overview.csv", market_overview_headers, market_overview_rows)

# ── 2. COMPETITOR DATA ────────────────────────────────────────────────
competitor_headers = [
    "chain", "type", "parent_company", "year_founded_ph",
    "stores_2025", "stores_2026_target", "stores_2024",
    "avg_cup_price_php", "price_tier",
    "store_formats", "primary_regions",
    "app_ordering", "franchise_available",
    "owned_by", "key_notes"
]
competitor_rows = [
    ("Starbucks", "International Premium",
     "Rustan Coffee Corp (under Starbucks Corp)", 1997,
     520, 540, 500,
     195, "Premium",
     "Full café, Reserve, Drive-thru, Community",
     "NCR, CALABARZON, Central Luzon, Visayas, Mindanao",
     True, False,
     "Rustan Commercial Corp / Starbucks Corp",
     "Largest premium chain; licensed model; loyalty program; premium positioning"),
    ("Pickup Coffee", "Local Value",
     "Pickup Coffee Inc.", 2022,
     500, 800, 320,
     70, "Budget",
     "Cart, Kiosk, Café, Prime",
     "Nationwide (Luzon, Visayas, Mindanao)",
     True, True,
     "Filipino (backed by private equity)",
     "Fastest-growing PH chain; 20 stores/mo target; P1.7-2M franchise; grab-and-go model"),
    ("Zus Coffee", "Regional Value",
     "Zuspresso Sdn Bhd (Malaysia)", 2023,
     120, 200, 60,
     85, "Affordable",
     "Kiosk, Small-format café",
     "Metro Manila, CALABARZON, Cebu, Davao",
     True, True,
     "Malaysian (Frank Lao investment)",
     "Malaysia #1 chain (743 stores); ~70% online orders; tech-driven; ube latte"),
    ("Bo's Coffee", "Local Mid-Range",
     "WS and Landin Inc. (Steve Benitez)", 1996,
     100, 150, 90,
     130, "Mid-Range",
     "Full café, Kiosk",
     "Visayas (Cebu hub), NCR, Mindanao, Luzon",
     True, True,
     "Filipino (founded Cebu)",
     "Oldest PH homegrown chain; sources PH-grown beans; international in Qatar/UAE"),
    ("Coffee Bean & Tea Leaf", "International Mid-Range",
     "Jollibee Foods Corp (acquired 2019)", 2003,
     220, 240, 210,
     165, "Mid-Range",
     "Full café, Kiosk, Kitchen concept",
     "NCR, CALABARZON, Central Luzon, Visayas",
     True, False,
     "Jollibee Foods Corp",
     "Acquired by JFC for $350M in 2019; 1,232 stores globally; strong tea lineup"),
    ("Tim Hortons", "International Mid-Range",
     "Tim Hortons Philippines (franchise)", 2022,
     30, 50, 20,
     120, "Mid-Range",
     "Full café, Drive-thru",
     "Metro Manila, CALABARZON",
     True, True,
     "Canadian (master franchise PH)",
     "Late entry to PH; coffee + donuts; Canadian heritage brand"),
    ("J.CO Donuts & Coffee", "International Mid-Range",
     "J.CO (Indonesia)", 2013,
     60, 75, 55,
     140, "Mid-Range",
     "Full café (donuts + coffee)",
     "NCR, CALABARZON, Cebu, Davao",
     True, True,
     "Indonesian (Johnny Andrean Group)",
     "Premium donuts + specialty coffee; known for Jcoccino; strong brand loyalty"),
    ("Figaro Coffee", "Local Mid-Range",
     "Figaro Coffee Group Inc.", 1993,
     35, 45, 30,
     140, "Mid-Range",
     "Full café, Restaurant-style",
     "Metro Manila, CALABARZON",
     True, True,
     "Filipino (publicly listed on PSE)",
     "Oldest PH coffee chain; publicly listed; restaurant-style dining"),
]
write_csv("competitors.csv", competitor_headers, competitor_rows)

# ── 3. GEOGRAPHIC DISTRIBUTION ────────────────────────────────────────
geo_headers = ["region", "city_province",
               "starbucks", "pickup", "zus", "bos", "cb_tl", "tim_hortons", "jco",
               "independents_est", "population_m", "urbanization_pct"]
geo_rows = [
    ("NCR", "Metro Manila", 180, 150, 50, 15, 100, 15, 20, 14.9, 100),
    ("NCR", "Makati", 40, 30, 12, 3, 25, 3, 5, 0.6, 100),
    ("NCR", "Quezon City", 55, 40, 15, 4, 28, 4, 6, 3.0, 100),
    ("NCR", "Taguig (BGC)", 30, 20, 8, 2, 18, 2, 3, 1.0, 100),
    ("NCR", "Pasig / Mandaluyong / San Juan", 25, 25, 8, 3, 14, 3, 3, 2.5, 100),
    ("NCR", "Parañaque / Las Piñas / Muntinlupa", 20, 25, 5, 2, 10, 2, 2, 3.0, 100),
    ("NCR", "Manila", 10, 10, 2, 1, 5, 1, 1, 1.8, 100),
    ("CALABARZON", "Cavite", 35, 30, 10, 2, 18, 4, 3, 4.3, 62),
    ("CALABARZON", "Laguna", 25, 25, 8, 2, 12, 2, 2, 3.4, 58),
    ("CALABARZON", "Batangas", 20, 15, 4, 3, 10, 1, 2, 2.9, 55),
    ("CALABARZON", "Rizal", 15, 20, 5, 1, 8, 1, 1, 3.2, 60),
    ("CALABARZON", "Quezon", 5, 5, 1, 1, 2, 0, 0, 2.0, 45),
    ("Central Luzon", "Pampanga", 20, 20, 5, 2, 12, 2, 3, 2.5, 58),
    ("Central Luzon", "Bulacan", 15, 20, 4, 1, 8, 1, 1, 3.7, 52),
    ("Central Luzon", "Tarlac / Nueva Ecija / Zambales", 10, 15, 2, 1, 5, 1, 1, 4.1, 45),
    ("Visayas", "Cebu (Metro Cebu)", 25, 30, 8, 30, 15, 2, 5, 3.3, 68),
    ("Visayas", "Iloilo", 8, 10, 3, 5, 5, 1, 2, 2.1, 50),
    ("Visayas", "Bacolod", 6, 8, 2, 3, 4, 1, 1, 0.6, 52),
    ("Visayas", "Tacloban / Leyte / Samar", 3, 5, 1, 2, 2, 0, 0, 4.5, 35),
    ("Mindanao", "Davao (Metro Davao)", 15, 15, 6, 8, 10, 1, 3, 1.8, 60),
    ("Mindanao", "Cagayan de Oro", 6, 10, 3, 5, 5, 1, 2, 0.8, 52),
    ("Mindanao", "General Santos / SOCCSKSARGEN", 4, 8, 1, 3, 3, 0, 1, 4.5, 40),
    ("Mindanao", "Zamboanga / Butuan / Cotabato", 3, 5, 1, 3, 2, 0, 0, 3.5, 38),
    ("North Luzon", "Baguio / Benguet / CAR", 5, 10, 2, 2, 4, 1, 1, 1.8, 50),
    ("North Luzon", "Ilocos / Cagayan Valley", 4, 8, 1, 1, 3, 0, 0, 4.2, 38),
    ("Luzon Others", "Bicol / Palawan / MIMAROPA", 6, 10, 2, 2, 4, 1, 1, 5.2, 35),
]
write_csv("geographic_distribution.csv", geo_headers, geo_rows)

# ── 4. PRICING ANALYSIS ───────────────────────────────────────────────
pricing_headers = ["chain", "drink", "size", "price_php"]
pricing_rows = [
    # Starbucks
    ("Starbucks", "Caffè Americano", "Tall", 165),
    ("Starbucks", "Caffè Americano", "Grande", 182),
    ("Starbucks", "Caffè Latte", "Tall", 176),
    ("Starbucks", "Caffè Latte", "Grande", 193),
    ("Starbucks", "Caramel Macchiato", "Tall", 205),
    ("Starbucks", "Caramel Macchiato", "Grande", 220),
    ("Starbucks", "Java Chip Frappuccino", "Tall", 209),
    ("Starbucks", "Brewed Coffee", "Tall", 127),
    ("Starbucks", "Brewed Coffee", "Grande", 143),
    ("Starbucks", "Cold Brew", "Tall", 193),
    ("Starbucks", "Matcha Latte", "Tall", 195),
    ("Starbucks", "Hot Chocolate", "Tall", 187),
    # Pickup Coffee
    ("Pickup Coffee", "Americano", "Regular", 50),
    ("Pickup Coffee", "Latte", "Regular", 70),
    ("Pickup Coffee", "Dark Mocha", "Regular", 75),
    ("Pickup Coffee", "Caramel Latte", "Regular", 85),
    ("Pickup Coffee", "White Mocha", "Regular", 85),
    ("Pickup Coffee", "Cappuccino", "Regular", 70),
    ("Pickup Coffee", "Matcha Latte", "Regular", 75),
    ("Pickup Coffee", "Ube Latte", "Regular", 70),
    ("Pickup Coffee", "Dirty Chai", "Regular", 85),
    ("Pickup Coffee", "Spanish Latte", "Regular", 85),
    ("Pickup Coffee", "Nutellatte", "Regular", 85),
    # Zus Coffee
    ("Zus Coffee", "Americano", "Regular", 55),
    ("Zus Coffee", "Caffè Latte", "Regular", 65),
    ("Zus Coffee", "Caramel Latte", "Regular", 75),
    ("Zus Coffee", "Spanish Latte", "Regular", 75),
    ("Zus Coffee", "Cappuccino", "Regular", 65),
    ("Zus Coffee", "Matcha Latte", "Regular", 80),
    ("Zus Coffee", "Ube Latte", "Regular", 75),
    ("Zus Coffee", "Chocolate", "Regular", 70),
    # Bo's Coffee
    ("Bo's Coffee", "Americano", "Regular", 90),
    ("Bo's Coffee", "Caffè Latte", "Regular", 120),
    ("Bo's Coffee", "Caramel Latte", "Regular", 135),
    ("Bo's Coffee", "Spanish Latte", "Regular", 130),
    ("Bo's Coffee", "Cappuccino", "Regular", 120),
    ("Bo's Coffee", "Mocha", "Regular", 135),
    ("Bo's Coffee", "Matcha Latte", "Regular", 140),
    # Coffee Bean & Tea Leaf
    ("Coffee Bean & Tea Leaf", "Americano", "Regular", 140),
    ("Coffee Bean & Tea Leaf", "Caffè Latte", "Regular", 165),
    ("Coffee Bean & Tea Leaf", "Caramel Latte", "Regular", 180),
    ("Coffee Bean & Tea Leaf", "Ice Blended Mocha", "Regular", 195),
    ("Coffee Bean & Tea Leaf", "Matcha Latte", "Regular", 175),
    ("Coffee Bean & Tea Leaf", "Cold Brew", "Regular", 170),
    ("Coffee Bean & Tea Leaf", "Signature Hot Chocolate", "Regular", 170),
    # Tim Hortons
    ("Tim Hortons", "Original Blend Coffee", "Medium", 85),
    ("Tim Hortons", "Latte", "Medium", 120),
    ("Tim Hortons", "Cappuccino", "Medium", 115),
    ("Tim Hortons", "French Vanilla", "Medium", 120),
    ("Tim Hortons", "Iced Capp", "Medium", 135),
    ("Tim Hortons", "Hot Chocolate", "Medium", 110),
    # J.CO
    ("J.CO Donuts & Coffee", "Jcoccino", "Small", 150),
    ("J.CO Donuts & Coffee", "Americano", "Small", 120),
    ("J.CO Donuts & Coffee", "Cafe Latte", "Small", 156),
    ("J.CO Donuts & Coffee", "Caramel Jcoccino", "Small", 156),
    ("J.CO Donuts & Coffee", "Mocha Espresso", "Small", 156),
    # Figaro
    ("Figaro Coffee", "Americano", "Regular", 120),
    ("Figaro Coffee", "Caffè Latte", "Regular", 145),
    ("Figaro Coffee", "Caramel Latte", "Regular", 155),
    ("Figaro Coffee", "Spanish Latte", "Regular", 155),
    ("Figaro Coffee", "Mocha", "Regular", 150),
]
write_csv("pricing_data.csv", pricing_headers, pricing_rows)

# ── 5. CONSUMER BEHAVIOR ──────────────────────────────────────────────
consumer_headers = ["metric", "value", "source", "year"]
consumer_rows = [
    ("Filipinos who drink coffee daily (%)", "80", "IntagriJournal / Corner Coffee Store", "2024"),
    ("Average cups per day", "2.5", "IntagriJournal", "2024"),
    ("Per capita consumption (kg/year)", "3.3", "USDA / Helgi Library", "2024"),
    ("Households with coffee stocked (%)", "90", "Corner Coffee Store", "2024"),
    ("Households buying coffee weekly (%)", "93", "Corner Coffee Store", "2024"),
    ("Instant coffee share of consumption (%)", "90", "USDA", "2024"),
    ("Fresh ground coffee share (%)", "7", "MarketResearch / Euromonitor", "2025"),
    ("Coffee pods/capsules share (%)", "3", "MarketResearch / Euromonitor", "2025"),
    ("Online coffee purchases share (%)", "15", "Statista", "2025"),
    ("Coffee shop visit frequency (times/week)", "2.8", "Euromonitor", "2025"),
    ("Avg spend per café visit (PHP)", "175", "Euromonitor", "2025"),
    ("Premium coffee willing to pay more (%)", "45", "Euromonitor", "2025"),
    ("Coffee for energy/alertness (%)", "62", "Various surveys", "2024"),
    ("Coffee for social/meeting (%)", "23", "Various surveys", "2024"),
    ("Coffee for taste/enjoyment (%)", "15", "Various surveys", "2024"),
    ("PH rank - global coffee consumption", "7th", "ReportLinker", "2024"),
    ("PH rank - soluble coffee consumption", "1st", "Ashu Research / USDA", "2024"),
    ("PH rank - coffee production", "30th", "ReportLinker", "2024"),
]
write_csv("consumer_behavior.csv", consumer_headers, consumer_rows)

# ── 6. REGIONAL MARKET BREAKDOWN (revenue) ────────────────────────────
region_rev_headers = ["region", "revenue_share_pct", "revenue_billion_usd",
                       "cagr_2026_2034_pct", "top_cities"]
region_rev_rows = [
    ("Luzon (incl. NCR)", 62.7, 1.14, 5.9,
     "Metro Manila, CALABARZON, Central Luzon"),
    ("Visayas", 21.4, 0.39, 6.8,
     "Cebu, Iloilo, Bacolod"),
    ("Mindanao", 15.9, 0.29, 6.2,
     "Davao, CDO, GenSan"),
]
write_csv("regional_market_breakdown.csv", region_rev_headers, region_rev_rows)

# ── 7. COFFEE PRODUCTION (supply side) ────────────────────────────────
prod_headers = ["year", "production_tons", "robusta_tons", "arabica_tons",
                "farmgate_price_php_per_kg", "imports_tons"]
prod_rows = [
    (2019, 27500, 25800, 1700, 62, 320000),
    (2020, 28000, 26000, 2000, 58, 310000),
    (2021, 27000, 25000, 2000, 55, 335000),
    (2022, 26500, 25000, 1500, 60, 340000),
    (2023, 26000, 24500, 1500, 65, 348000),
    (2024, 27000, 25500, 1500, 70, 352500),
    (2025, 24000, 22500, 1500, 75, 360000),
    (2026, 22000, 20500, 1500, 80, 365000),
]
write_csv("coffee_production.csv", prod_headers, prod_rows)

print("\nAll raw data files generated.")

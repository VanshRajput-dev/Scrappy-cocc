# Bike Data Collector for Route Suitability Scoring

## 📌 Overview

This project builds a **clean, physics-safe dataset of motorcycle specifications**
that can be used for **route suitability analysis and scoring**.

Instead of asking users to manually enter bike specifications, the system allows
them to **select a bike model**, after which all required technical parameters are
automatically available for downstream algorithms.

The primary use case is:
> **Selecting the right bike for a given route** based on terrain, traffic,
distance, and riding conditions.

---

## 🎯 Key Design Principles

- **Detail pages are authoritative** — listing pages are not trusted for specs
- **No guessing** — ambiguous values are discarded, not repaired
- **Unit-aware parsing** — bhp/ps, Nm/kgm handled safely
- **Physics validation** — impossible values are rejected
- **Completeness over quantity** — missing data is better than wrong data

---

## 🏍️ What Data Is Collected

For each bike:

- brand
- model
- engine_cc
- power_bhp
- torque_nm
- kerb_weight_kg
- mileage_kmpl
- abs (if available)
- detail_url

⚠️ **Price is intentionally excluded** because it is volatile,
location-dependent, and irrelevant for route suitability.

---

## 🗂️ Project Structure

bike-data-collector/
│
├── src/
│ ├── main.py # Pipeline entry point
│ ├── brands.py # Brand discovery
│ ├── scraper.py # Bike URL extraction
│ ├── parser.py # Listing-page parsing
│ ├── detail_parser.py # Detail-page spec discovery
│ ├── spec_parser.py # Unit-safe spec parsing & validation
│ ├── save.py # Output writer
│ ├── filter_complete_bikes.py # Filters fully-usable bikes
│ ├── config.py # Headers & config
│ ├── enrich_data.py # (optional / experimental)
│ └── normalize_data.py # (optional / experimental)
│
├── output/ # Generated datasets (gitignored)
├── requirements.txt
├── README.md
└── .gitignore

---

## 🚀 How to Run (Production-Grade)

### 1️⃣ Install dependencies
```bash
pip install -r requirements.txt
python src/main.py
This will:

scrape all brands and bikes

extract authoritative specs

save results to output/bikes.json
🛠️ Manual Bike Entry (Future Use)

The system is designed to support manual bike entry as an optional path.
Manual input is validated using the same physics rules as scraped data.

⚠️ Disclaimer

This project is intended for analysis and research purposes.
Specifications may vary by region, variant, and year.
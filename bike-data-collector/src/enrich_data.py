import json
import time
from pathlib import Path
from src.scraper import fetch_html
from src.detail_parser import parse_detail_page

INPUT = Path("data/bikes_ml_ready.json")
OUTPUT = Path("data/bikes_enriched.json")

DELAY = 2.0  # seconds

def enrich():
    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    bikes = data["bikes"]

    # Create output file early
    enriched = []
    if OUTPUT.exists():
        with open(OUTPUT, "r", encoding="utf-8") as f:
            enriched = json.load(f).get("bikes", [])

    enriched_index = {
        (b.get("brand"), b.get("model")): b
        for b in enriched
    }

    for i, bike in enumerate(bikes, 1):
        key = (bike.get("brand"), bike.get("model"))

        # Skip already enriched bikes
        if key in enriched_index and enriched_index[key].get("engine_cc"):
            continue

        url = bike.get("detail_url")
        if not url:
            continue

        try:
            print(f"[{i}/{len(bikes)}] Enriching {bike['brand']} {bike['model']}")
            html = fetch_html(url)
            specs = parse_detail_page(html)
            bike.update(specs)
        except Exception as e:
            print("Failed:", e)

        enriched_index[key] = bike

        # 🔥 WRITE CHECKPOINT EVERY BIKE
        with open(OUTPUT, "w", encoding="utf-8") as f:
            json.dump({
                "schema_version": "3.0",
                "count": len(enriched_index),
                "bikes": list(enriched_index.values())
            }, f, indent=2, ensure_ascii=False)

        time.sleep(DELAY)

    print("Enrichment complete.")

if __name__ == "__main__":
    enrich()

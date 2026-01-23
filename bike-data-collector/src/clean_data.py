import json
from pathlib import Path

INPUT = Path("data/bikes_enriched.json")
OUTPUT = Path("data/bikes_final_clean.json")

ALLOWED_CATEGORIES = {
    "motorcycle",
    "electric_motorcycle"
}

JUNK_KEYWORDS = {
    "more reviews",
    "reviews",
    "compare",
    "expert",
    "user review"
}

def clean_number(val):
    if isinstance(val, (int, float)):
        return val
    return None

def clean():
    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = []
    seen = set()

    for b in data["bikes"]:
        brand = b.get("brand")
        model = b.get("model")

        if not brand or not model or len(model) < 3:
            continue

        model_lower = model.lower()

        # 🚫 remove UI junk
        if any(k in model_lower for k in JUNK_KEYWORDS):
            continue

        # 🚫 keep only bikes (no scooters)
        if b.get("vehicle_category") not in ALLOWED_CATEGORIES:
            continue

        key = (brand.strip(), model.strip())
        if key in seen:
            continue
        seen.add(key)

        cleaned.append({
            "brand": brand,
            "model": model,
            "price_inr": b.get("price_inr_numeric"),
            "price_bucket": b.get("price_bucket"),
            "fuel_type": b.get("fuel_type"),
            "vehicle_category": b.get("vehicle_category"),
            "status": b.get("status"),

            # enriched specs
            "engine_cc": clean_number(b.get("engine_cc")),
            "power_bhp": clean_number(b.get("power")),
            "torque_nm": clean_number(b.get("torque")),
            "mileage_kmpl": clean_number(b.get("mileage")),
            "kerb_weight_kg": clean_number(b.get("kerb_weight")),
            "fuel_tank_l": clean_number(b.get("fuel_tank_capacity")),
            "abs": b.get("abs"),

            "detail_url": b.get("detail_url")
        })

    output = {
        "schema_version": "final-1.0",
        "original_count": len(data["bikes"]),
        "final_count": len(cleaned),
        "bikes": cleaned
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("Original enriched bikes:", len(data["bikes"]))
    print("Final cleaned motorcycles:", len(cleaned))

if __name__ == "__main__":
    clean()

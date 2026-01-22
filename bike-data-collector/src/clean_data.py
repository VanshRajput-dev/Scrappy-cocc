import json
import re
from pathlib import Path

INPUT = Path("data/bikes.json")
OUTPUT = Path("data/bikes_clean.json")

EV_BRANDS = {
    "Ather", "Ola", "Revolt", "Bounce", "Ampere",
    "Hero Electric", "PUREEV", "Simple Energy",
    "Ultraviolette", "Tork", "Okinawa"
}

def parse_price(price):
    if not price:
        return None
    digits = re.sub(r"[^\d]", "", price)
    return int(digits) if digits else None

def detect_fuel_type(brand, model):
    text = f"{brand} {model}".lower()
    if brand in EV_BRANDS:
        return "electric"
    if any(k in text for k in ["electric", "ev", "e-bike"]):
        return "electric"
    return "petrol"

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

        key = (brand.strip(), model.strip())
        if key in seen:
            continue
        seen.add(key)

        price_num = parse_price(b.get("price_inr"))
        fuel = detect_fuel_type(brand, model)

        cleaned.append({
            **b,
            "price_inr_numeric": price_num,
            "fuel_type": fuel
        })

    output = {
        "schema_version": "1.1",
        "original_count": len(data["bikes"]),
        "cleaned_count": len(cleaned),
        "bikes": cleaned
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("Original:", len(data["bikes"]))
    print("Cleaned:", len(cleaned))

if __name__ == "__main__":
    clean()

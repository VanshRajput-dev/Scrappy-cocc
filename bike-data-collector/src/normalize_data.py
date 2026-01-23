import json
from pathlib import Path

INPUT = Path("data/bikes.json")
OUTPUT = Path("data/bikes_ml_ready.json")

EV_BRANDS = {
    "Ather", "Ola", "Okinawa", "Revolt", "Ultraviolette",
    "Simple Energy", "Hop Electric", "Ampere", "PURE EV",
    "Hero Electric", "Bounce", "Odysse", "Quantum Energy",
    "Lectrix", "Joy e-bike", "iVOOMi", "Matter"
}

SCOOTER_KEYWORDS = {
    "activa", "jupiter", "access", "dio", "ntorq",
    "vespa", "chetak", "aerox", "burgman", "rizta"
}

def price_bucket(price):
    if price is None:
        return "unknown"
    if price < 100000:
        return "budget"
    if price < 200000:
        return "mid_low"
    if price < 400000:
        return "mid_high"
    if price < 800000:
        return "premium"
    return "luxury"

def normalize_category(brand, model, fuel):
    text = f"{brand} {model}".lower()

    if fuel == "electric":
        if any(k in text for k in SCOOTER_KEYWORDS):
            return "electric_scooter"
        return "electric_motorcycle"

    if any(k in text for k in SCOOTER_KEYWORDS):
        return "scooter"

    return "motorcycle"

def normalize():
    with open(INPUT, "r", encoding="utf-8") as f:
        data = json.load(f)

    normalized = []

    for b in data["bikes"]:
        brand = b.get("brand")
        model = b.get("model")
        price = b.get("price_inr_numeric")
        fuel = b.get("fuel_type", "unknown")
        status = b.get("status", "unknown")

        fuel_norm = fuel if fuel in {"petrol", "electric"} else "unknown"

        normalized.append({
            **b,
            "price_bucket": price_bucket(price),
            "fuel_type": fuel_norm,
            "vehicle_category": normalize_category(brand, model, fuel_norm),
            "status": status if status in {"launched", "upcoming"} else "unknown"
        })

    output = {
        "schema_version": "2.0",
        "count": len(normalized),
        "bikes": normalized
    }

    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("Normalized bikes:", len(normalized))

if __name__ == "__main__":
    normalize()

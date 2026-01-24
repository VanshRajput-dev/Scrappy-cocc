import json
import csv
from pathlib import Path

# --------------------------------------------------
# PATHS (MATCH YOUR PROJECT STRUCTURE)
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

INPUT_JSON = OUTPUT_DIR / "bikes.json"              # ✅ INPUT
OUTPUT_JSON = OUTPUT_DIR / "bikes_complete.json"    # ✅ OUTPUT
OUTPUT_CSV = OUTPUT_DIR / "bikes_complete.csv"      # ✅

REQUIRED_FIELDS = [
    "brand",
    "model",
    "engine_cc",
    "power_bhp",
    "torque_nm",
    "kerb_weight_kg",
    "mileage_kmpl"
]


def is_complete_bike(bike: dict) -> bool:
    for field in REQUIRED_FIELDS:
        if field not in bike or bike[field] is None:
            return False
    return True


def main():
    if not INPUT_JSON.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_JSON}")

    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list of bike objects")

    kept = []
    dropped = 0

    for bike in data:
        if is_complete_bike(bike):
            kept.append(bike)
        else:
            dropped += 1

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(kept, f, indent=2, ensure_ascii=False)

    if kept:
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=kept[0].keys())
            writer.writeheader()
            writer.writerows(kept)

    print("✅ Filtering complete\n")
    print(f"Input bikes      : {len(data)}")
    print(f"Usable bikes     : {len(kept)}")
    print(f"Dropped bikes    : {dropped}")
    print("\nSaved to:")
    print(f" - {OUTPUT_JSON}")
    print(f" - {OUTPUT_CSV}")


if __name__ == "__main__":
    main()

import json
import csv
from pathlib import Path

FIELDS = [
    "brand", "model",
    "price_inr", "price_bucket", "status",
    "engine_cc", "power_bhp", "torque_nm",
    "kerb_weight_kg", "mileage_kmpl",
    "fuel_type", "vehicle_category", "abs",
    "fuel_tank_l", "detail_url"
]

OUT = Path("output")
JSON_PATH = OUT / "bikes.json"
CSV_PATH = OUT / "bikes.csv"

def init_output():
    OUT.mkdir(exist_ok=True)
    JSON_PATH.write_text("[]", encoding="utf-8")
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writeheader()

def save(record):
    clean = {k: record.get(k) for k in FIELDS}

    data = json.loads(JSON_PATH.read_text())
    data.append(clean)
    JSON_PATH.write_text(json.dumps(data, indent=2))

    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=FIELDS).writerow(clean)

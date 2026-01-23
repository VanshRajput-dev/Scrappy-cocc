import json
from datetime import datetime
from pathlib import Path
from src.config import SOURCE

DATA_PATH = Path("data/bikes_enriched.json")

def save_json(new_bikes):
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
            existing_bikes = existing_data.get("bikes", [])
    else:
        existing_bikes = []

    index = {
        (b.get("brand"), b.get("model")): b
        for b in existing_bikes
    }

    for bike in new_bikes:
        key = (bike.get("brand"), bike.get("model"))
        if key in index:
            # UPDATE existing entry
            index[key].update(bike)
        else:
            # INSERT new entry
            existing_bikes.append(bike)
            index[key] = bike

    payload = {
        "schema_version": "1.2",
        "scraped_at": datetime.utcnow().isoformat(),
        "source": SOURCE,
        "count": len(existing_bikes),
        "bikes": existing_bikes
    }

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

        print("Writing to:", DATA_PATH.resolve())


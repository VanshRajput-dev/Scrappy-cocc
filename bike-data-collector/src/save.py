import json
from datetime import datetime
from pathlib import Path
from src.config import SOURCE

DATA_PATH = Path("data/bikes.json")

def save_json(new_bikes):
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            existing = json.load(f)
            all_bikes = existing.get("bikes", [])
    else:
        all_bikes = []

    seen = {
        (b.get("brand"), b.get("model"))
        for b in all_bikes
    }

    for bike in new_bikes:
        key = (bike.get("brand"), bike.get("model"))
        if key not in seen:
            all_bikes.append(bike)
            seen.add(key)

    payload = {
        "schema_version": "1.0",
        "scraped_at": datetime.utcnow().isoformat(),
        "source": SOURCE,
        "count": len(all_bikes),
        "bikes": all_bikes
    }

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

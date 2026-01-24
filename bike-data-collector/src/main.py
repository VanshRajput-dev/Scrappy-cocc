import time
import requests
from pathlib import Path

from src.brands import get_all_brands
from src.scraper import get_all_bikes_for_brand
from src.detail_parser import parse_bike_page
from src.save import init_output, save
from src.config import HEADERS, TIMEOUT


BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"


def safe_get(url, retries=3, delay=1.0):
    last_error = None

    for attempt in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            r.raise_for_status()
            return r
        except requests.exceptions.RequestException as e:
            last_error = e
            time.sleep(delay * (attempt + 1))

    raise RuntimeError(f"Failed to fetch: {url}") from last_error


def run():
    OUTPUT_DIR.mkdir(exist_ok=True)
    init_output()

    brands = get_all_brands()
    print(f"Found {len(brands)} brands\n")

    for brand, url in brands.items():
        print(f"Scraping brand: {brand}")
        bikes = get_all_bikes_for_brand(brand, url)

        for bike in bikes:
            try:
                r = safe_get(bike["detail_url"])
                specs = parse_bike_page(r.text)

                record = {
                    **bike,
                    **specs,
                    "fuel_tank_l": None
                }

                save(record)
                time.sleep(0.5)

            except RuntimeError as e:
                print(f"[FETCH FAILED] {bike['detail_url']}")
                continue

            except Exception as e:
                print(f"[PARSE ERROR] {bike['detail_url']} → {type(e).__name__}")
                continue

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    run()

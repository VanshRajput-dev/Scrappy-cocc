import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from src.config import HEADERS, TIMEOUT

def get_all_bikes_for_brand(brand, brand_url):
    r = requests.get(brand_url, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    bikes = {}

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if not href.startswith("/") or brand_url.split("/")[-2] not in href:
            continue

        parts = href.strip("/").split("/")
        if len(parts) != 2:
            continue

        model = a.get_text(strip=True)
    
        if model.lower().startswith(brand.lower()):
         model = model[len(brand):].strip()


        bikes[href] = {
            "brand": brand,
            "model": model,
            "detail_url": urljoin(brand_url, href),
            "price_inr": None,
            "price_bucket": None,
            "status": "launched",
            "fuel_type": "unknown",
            "vehicle_category": "motorcycle",
            "abs": None
        }

    return list(bikes.values())

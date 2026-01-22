from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.bikewale.com"

def parse_bikes(html):
    soup = BeautifulSoup(html, "html.parser")
    bikes = []

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if not href.startswith("/hero-bikes/"):
            continue

        name = a.get_text(strip=True)
        if not name or len(name) < 3:
            continue

        bikes.append({
            "brand": "Hero",
            "model": name,
            "price_inr": None,
            "detail_url": urljoin(BASE, href),
            "engine_cc": None,
            "power": None,
            "torque": None,
            "mileage": None,
            "category": "Bike"
        })

    return bikes

from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.bikewale.com"

def parse_bikes(html):
    soup = BeautifulSoup(html, "html.parser")
    bikes = []

    cards = soup.select("li")

    for card in cards:
        name_tag = card.select_one("a[href^='/royalenfield-bikes/']")
        price_tag = card.select_one("span")

        if not name_tag:
            continue

        name = name_tag.get_text(strip=True)

        if len(name) < 3:
            continue

        bikes.append({
            "brand": "Royal Enfield",
            "model": name,
            "price_inr": price_tag.get_text(strip=True) if price_tag else None,
            "detail_url": urljoin(BASE, name_tag["href"]),
            "engine_cc": None,
            "power": None,
            "torque": None,
            "mileage": None,
            "category": "Bike"
        })

    return bikes

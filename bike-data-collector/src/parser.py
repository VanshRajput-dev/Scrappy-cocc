import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://www.bikewale.com"

PRICE_RE = re.compile(r"₹\s?[\d,]+")
RATING_RE = re.compile(r"(\d(?:\.\d)?)\s*/\s*5")
LAUNCH_RE = re.compile(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'?\s?\d{2}")

JUNK_KEYWORDS = {
    "more reviews",
    "reviews",
    "compare",
    "rating",
    "expert review",
    "user review"
}

def parse_bikes(html, brand, prefix):
    """
    Listing-page parser.

    IMPORTANT:
    - Extracts ONLY metadata available on listing cards
    - Does NOT extract or infer technical specifications
    - All specs MUST be populated from detail pages later
    """

    soup = BeautifulSoup(html, "html.parser")
    bikes = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if prefix not in href:
            continue

        model_name = a.get_text(strip=True)
        if not model_name or len(model_name) < 3:
            continue

        model_lower = model_name.lower()

        if any(j in model_lower for j in JUNK_KEYWORDS):
            continue

        if re.search(r"\d{3,}$", model_name):
            continue

        if model_lower.startswith(brand.lower()):
            model_name = model_name[len(brand):].strip()

        card = a.parent
        text = card.get_text(" ", strip=True)

        price_text = None
        price_numeric = None
        rating = None
        launch_date = None
        status = "launched"

        price_match = PRICE_RE.search(text)
        if price_match:
            price_text = price_match.group()
            price_numeric = int(re.sub(r"[^\d]", "", price_text))

        rating_match = RATING_RE.search(text)
        if rating_match:
            rating = float(rating_match.group(1))

        launch_match = LAUNCH_RE.search(text)
        if launch_match and not price_text:
            launch_date = launch_match.group()
            status = "upcoming"

        key = (brand, model_name)
        if key in seen:
            continue
        seen.add(key)

        bikes.append({
            "brand": brand,
            "model": model_name,
            "price_text": price_text,
            "price_inr_numeric": price_numeric,
            "rating": rating,
            "launch_date": launch_date,
            "status": status,
            "detail_url": urljoin(BASE, href),

            # Technical specs – MUST be filled from detail pages
            "engine_cc": None,
            "power_bhp": None,
            "torque_nm": None,
            "kerb_weight_kg": None,
            "mileage_kmpl": None,

            "category": "Bike"
        })

    return bikes

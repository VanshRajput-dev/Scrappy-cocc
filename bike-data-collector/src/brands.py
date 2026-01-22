import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from src.config import HEADERS, TIMEOUT

BASE = "https://www.bikewale.com"
BRAND_PAGE = "https://www.bikewale.com/new-bikes-in-india/"

EXCLUDE_KEYWORDS = {
    "compare",
    "best",
    "upcoming",
    "search",
    "mileage",
    "100cc",
    "110cc",
    "125cc",
    "150cc",
    "200cc",
    "250cc",
    "500cc"
}

def get_all_brands():
    r = requests.get(BRAND_PAGE, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    brands = {}

    for a in soup.find_all("a", href=True):
        href = a["href"]

        if not href.endswith("-bikes/"):
            continue

        if any(x in href for x in EXCLUDE_KEYWORDS):
            continue

        name = a.get_text(strip=True)
        if not name:
            continue

        brands[name] = urljoin(BASE, href)

    return brands

import re
from bs4 import BeautifulSoup

import re

def extract_number(text):
    if not text:
        return None

    match = re.search(r"\d+(\.\d+)?", text)
    if not match:
        return None

    try:
        return float(match.group())
    except ValueError:
        return None


def parse_detail_page(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True).lower()

    specs = {
        "engine_cc": None,
        "power": None,
        "torque": None,
        "mileage": None,
        "abs": None,
        "kerb_weight": None
    }

    def find_after(keyword):
        idx = text.find(keyword)
        if idx == -1:
            return None
        return text[idx:idx+80]

    specs["engine_cc"] = extract_number(find_after("engine"))
    specs["power"] = extract_number(find_after("bhp"))
    specs["torque"] = extract_number(find_after("nm"))
    specs["mileage"] = extract_number(find_after("kmpl"))
    specs["kerb_weight"] = extract_number(find_after("kg"))

    if "dual channel abs" in text:
        specs["abs"] = "dual"
    elif "single channel abs" in text:
        specs["abs"] = "single"
    elif "abs" in text:
        specs["abs"] = "yes"

    return specs

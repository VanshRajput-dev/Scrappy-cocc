from bs4 import BeautifulSoup
from src.spec_parser import extract_specs

# Only labels we CARE about (hard gate)
VALID_LABEL_KEYWORDS = {
    "engine",
    "displacement",
    "power",
    "torque",
    "weight",
    "mileage"
}

def parse_bike_page(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = []

    # 1️⃣ Table-based specs (most reliable)
    for tr in soup.select("table tr"):
        tds = tr.find_all("td")
        if len(tds) == 2:
            label = tds[0].get_text(strip=True)
            value = tds[1].get_text(strip=True)
            rows.append((label, value))

    # 2️⃣ Definition lists (dt / dd)
    for dl in soup.find_all("dl"):
        dts = dl.find_all("dt")
        dds = dl.find_all("dd")
        for dt, dd in zip(dts, dds):
            rows.append((
                dt.get_text(strip=True),
                dd.get_text(strip=True)
            ))

    # 3️⃣ BikeWale spec blocks (div-based, but guarded)
    divs = soup.find_all("div")
    for i in range(len(divs) - 1):
        label = divs[i].get_text(strip=True)
        value = divs[i + 1].get_text(strip=True)

        if not label or not value:
            continue

        l = label.lower()

        # 🔒 HARD FILTER — only spec-like labels
        if not any(k in l for k in VALID_LABEL_KEYWORDS):
            continue

        # 🔒 Avoid obvious junk
        if len(label) > 40:
            continue

        rows.append((label, value))

    # 🔥 SINGLE source of truth for interpretation
    return extract_specs(rows)

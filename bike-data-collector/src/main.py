from src.scraper import fetch_html
from src.brands import get_all_brands
from src.parser import parse_bikes
from src.save import save_json

def run():
    brands = get_all_brands()
    print("Brands found:", len(brands))

    total = 0

    for brand, url in brands.items():
        prefix = "/" + url.rstrip("/").split("/")[-1] + "/"
        print(f"\nScraping {brand} -> {url}")

        html = fetch_html(url)
        bikes = parse_bikes(html, brand, prefix)

        print("Bikes parsed:", len(bikes))

        total += len(bikes)
        save_json(bikes)

    print("\nTOTAL BIKES PARSED THIS RUN:", total)

if __name__ == "__main__":
    run()

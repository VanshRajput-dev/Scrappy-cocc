from src.scraper import fetch_html
from src.parser import parse_bikes
from src.save import save_json
from src.config import BASE_URL

def run():
    html = fetch_html(BASE_URL)
    bikes = parse_bikes(html)
    save_json(bikes)
    print(len(bikes))

if __name__ == "__main__":
    run()

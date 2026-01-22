import requests
from src.config import HEADERS, TIMEOUT

def fetch_html(url):
    r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    r.raise_for_status()
    return r.text

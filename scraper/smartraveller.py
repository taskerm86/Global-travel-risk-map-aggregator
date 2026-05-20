import requests
from bs4 import BeautifulSoup

LEVEL_MAP = {
    "do not travel": 4,
    "reconsider your need to travel": 3,
    "exercise a high degree of caution": 2,
    "exercise normal safety precautions": 1,
}

def scrape_smartraveller():
    url = "https://www.smartraveller.gov.au/destinations"
    headers = {"User-Agent": "Mozilla/5.0"}
    print("Fetching Smartraveller advisories...")
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    countries = []
    cards = soup.select("a.destination-card")[:10]
    for card in cards:
        name = card.select_one(".destination-card__title")
        advice = card.select_one(".destination-card__advice-level")
        if not name or not advice:
            continue
        advice_text = advice.text.strip().lower()
        level = LEVEL_MAP.get(advice_text, 1)
        country = {
            "name": name.text.strip(),
            "advice": advice.text.strip(),
            "level": level,
            "source": "smartraveller",
            "url": "https://www.smartraveller.gov.au" + card.get("href", "")
        }
        countries.append(country)
        print(f"{country['name']} -> Level {level} ({country['advice']})")
    return countries

scrape_smartraveller()

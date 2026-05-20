import requests

LEVEL_MAP = {
    1: 1,
    2: 2,
    3: 3,
    4: 4,
}

def scrape_us_state():
    url = "https://travel.state.gov/content/dam/NEWTravelAssets/TSGlobalAssetsJSON/en_US/travel-advisories.json"
    headers = {"User-Agent": "Mozilla/5.0"}
    print("Fetching US State Dept advisories...")
    response = requests.get(url, headers=headers, timeout=15)
    data = response.json()

    countries = []
    for item in list(data["advisories"].values())[:10]:
        country = {
            "name": item.get("name", ""),
            "level": item.get("level", 1),
            "source": "us_state",
            "url": "https://travel.state.gov" + item.get("url", "")
        }
        countries.append(country)
        print(f"{country['name']} -> Level {country['level']}")

    return countries

scrape_us_state()

import requests
import json

ALERT_TO_LEVEL = {
    "normal": 1,
    "avoid_non_essential_travel": 2,
    "avoid_all_but_essential_travel_to_parts": 3,
    "avoid_all_travel": 4,
}

def scrape_fcdo():
    url = "https://www.gov.uk/api/content/foreign-travel-advice"
    print("Fetching FCDO country list...")
    response = requests.get(url)
    data = response.json()

    countries = []
    children = data["links"]["children"]
    print(f"Found {len(children)} countries, fetching risk levels...")

    for i, link in enumerate(children[:10]):  # first 10 to start
        slug = link["base_path"].replace("/foreign-travel-advice/", "")
        detail = requests.get(f"https://www.gov.uk/api/content/foreign-travel-advice/{slug}").json()
        alert = detail.get("details", {}).get("alert_status", [])
        alert_str = alert[0] if alert else "normal"
        level = ALERT_TO_LEVEL.get(alert_str, 1)

        country = {
            "name": link["title"].replace(" travel advice", ""),
            "slug": slug,
            "alert": alert_str,
            "level": level,
            "url": "https://www.gov.uk" + link["base_path"]
        }
        countries.append(country)
        print(f"{i+1}. {country['name']} → Level {level} ({alert_str})")

    return countries

scrape_fcdo()
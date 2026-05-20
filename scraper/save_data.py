import requests
import json
import time

ALERT_TO_LEVEL = {
    "normal": 1,
    "avoid_non_essential_travel": 2,
    "avoid_all_but_essential_travel_to_parts": 3,
    "avoid_all_travel_to_parts": 3,
    "avoid_all_but_essential_travel": 3,
    "avoid_all_travel": 4,
    "avoid_all_travel_to_whole_country": 4,
}

def scrape_fcdo():
    url = "https://www.gov.uk/api/content/foreign-travel-advice"
    print("Fetching FCDO country list...")
    response = requests.get(url)
    data = response.json()
    countries = []
    children = data["links"]["children"]
    print(f"Found {len(children)} countries...")
    for i, link in enumerate(children):
        try:
            slug = link["base_path"].replace("/foreign-travel-advice/", "")
            detail = requests.get(f"https://www.gov.uk/api/content/foreign-travel-advice/{slug}").json()
            alerts = detail.get("details", {}).get("alert_status", [])
            
            # Get highest risk level from ALL alerts
            level = 1
            top_alert = "normal"
            for alert in alerts:
                mapped = ALERT_TO_LEVEL.get(alert, 1)
                if mapped > level:
                    level = mapped
                    top_alert = alert
            
            # Flag if multiple risk zones exist
            has_mixed = len(alerts) > 1

            country = {
                "name": link["title"].replace(" travel advice", ""),
                "slug": slug,
                "alert": top_alert,
                "all_alerts": alerts,
                "level": level,
                "has_mixed_risk": has_mixed,
                "source": "fcdo",
                "url": "https://www.gov.uk" + link["base_path"]
            }
            countries.append(country)
            mixed = " ⚠️ mixed" if has_mixed else ""
            print(f"{i+1}. {country['name']} -> Level {level}{mixed}")
            time.sleep(0.2)
        except Exception as e:
            print(f"Error on {link}: {e}")
            continue
    return countries

data = scrape_fcdo()
with open("advisories.json", "w") as f:
    json.dump(data, f, indent=2)
print(f"\nSaved {len(data)} countries to advisories.json")
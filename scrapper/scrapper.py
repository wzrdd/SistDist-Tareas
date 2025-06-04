import requests
import json
import pymongo
from pymongo import MongoClient

# waze url and queryparams
base_url = "https://www.waze.com/live-map/api/georss"
env = "row"
types = "alerts,traffic"

with open('coordinates.json', 'r') as file:
    data = json.load(file)

coordinates = data["coordinates"]

client = MongoClient("mongodb://dumbuser:dumbpassword@mongo:27017")
db = client["admin"]
alerts_collection = db["alerts"]

def fetch_alerts(top, bottom, left, right, env, types, region_name):
    url = f"{base_url}?top={top}&bottom={bottom}&left={left}&right={right}&env={env}&types={types}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        if "alerts" in data:
            return data["alerts"]
        else:
            print(f"No alerts found in {region_name} (Coordinates: Top={top}, Bottom={bottom}, Left={left}, Right={right})")
            return []
    else:
        print(f"Failed to fetch data for coordinates: top={top}, bottom={bottom}, left={left}, right={right}")
        return []

inserted_total = 0

for coord in coordinates:
    name = coord["name"]
    top = coord["top"]
    bottom = coord["bottom"]
    left = coord["left"]
    right = coord["right"]

    alerts = fetch_alerts(top, bottom, left, right, env, types, name)

    for alert in alerts:
        alert_data = {
            "region_name": name,
            "comuna": alert.get("city", "N/A"),
            "alert_id": alert.get("id", "N/A"),
            "report_by": alert.get("reportBy", "N/A"),
            "type": alert.get("type", "N/A"),
            "report_rating": alert.get("reportRating", "N/A"),
            "location_x": alert.get("location", {}).get("x", "N/A"),
            "location_y": alert.get("location", {}).get("y", "N/A")
        }

        alerts_collection.insert_one(alert_data)
        inserted_total += 1

        if inserted_total % 100 == 0:
            print(f"[PROGRESS] Insertados {inserted_total} alertas...")

print(f"[DONE] Insertados {inserted_total} alertas en total.")

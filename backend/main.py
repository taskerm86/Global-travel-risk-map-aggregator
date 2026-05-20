import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = os.path.join(os.path.dirname(__file__), "../scraper/advisories.json")

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

@app.get("/")
def root():
    return {"message": "Travel Risk Map API is running"}

@app.get("/advisories")
def get_advisories():
    return load_data()

@app.get("/advisory/{slug}")
def get_advisory(slug: str):
    data = load_data()
    for country in data:
        if country["slug"] == slug:
            return country
    return {"error": "Country not found"}
# collects data from the cornell course api

import os
import httpx

from cornell_db_updater.api_types import Roster

CORNELL_HOST = os.getenv("CORNELL_API_HOST")
CORNELL_VERSION = os.getenv("CORNELL_API_VERSION")

if CORNELL_HOST is None:
    raise ValueError("CORNELL_API_HOST must be set")

if CORNELL_VERSION is None:
    raise ValueError("CORNELL_API_VERSION must be set")


def create_cornell_path(route: str) -> str:
    return f"https://{CORNELL_HOST}/api/{CORNELL_VERSION}/{route}.json"


def fetch_cornell_data(route: str) -> dict:
    path = create_cornell_path(route)
    response = httpx.get(path)

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch data from {path}")

    data = response.json()

    if "data" not in data:
        raise ValueError(f"Invalid data returned from {path}")

    return data["data"]


data = fetch_cornell_data("config/rosters")["rosters"]

for datum in data:
    typed_datum = Roster(**datum)
    print(typed_datum)
    break

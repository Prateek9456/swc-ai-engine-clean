import os
import requests
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = os.getenv("GEOCODING_USER_AGENT")

NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse"


def reverse_geocode(lat, lon):
    """
    Convert GPS coordinates to administrative location.
    Returns state and district.
    """
    params = {
        "lat": lat,
        "lon": lon,
        "format": "json",
        "addressdetails": 1
    }

    headers = {
        "User-Agent": USER_AGENT
    }

    response = requests.get(NOMINATIM_URL, params=params, headers=headers)

    if response.status_code != 200:
        raise RuntimeError("Geocoding API failed")

    data = response.json()
    address = data.get("address", {})

    state = address.get("state")
    district = (
        address.get("district")
        or address.get("county")
        or address.get("state_district")
    )

    if not state:
        raise ValueError("State not found from GPS")

    return {
        "state": state,
        "district": district
    }

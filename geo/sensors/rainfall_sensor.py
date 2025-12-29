import requests


def fetch_rainfall_mm(lat, lon):
    """
    Fetch long-term mean ANNUAL rainfall (mm)
    using NASA POWER climatology (PRECTOTCORR).

    Units from API: mm/day (annual mean)
    Converted to: mm/year
    """

    url = "https://power.larc.nasa.gov/api/temporal/climatology/point"

    params = {
        "latitude": lat,
        "longitude": lon,
        "parameters": "PRECTOTCORR",
        "community": "AG",
        "format": "JSON"
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()

        # NASA POWER climatology gives annual mean in mm/day
        mm_per_day = data["properties"]["parameter"]["PRECTOTCORR"]["ANN"]

        annual_mm = mm_per_day * 365.0

        return round(float(annual_mm), 2)

    except Exception as e:
        print("NASA POWER rainfall API failed:", e)

        # Conservative India-wide climatological fallback
        return 1200.0

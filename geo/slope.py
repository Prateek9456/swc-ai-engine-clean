# geo/slope.py
# Terrain-averaged slope computation (ICAR-safe)

import requests
import math
import statistics

# =========================
# CONFIGURATION (TUNABLE)
# =========================

MAPBOX_TOKEN = "<pk.eyJ1IjoicHJhdGVlazk0NTYiLCJhIjoiY21qaTkwZjd0MDNtNzNmcjB1Y2I4NGFqMSJ9.Whh4fHjS_jpVx95gqtGayA>"
MAPBOX_URL = "https://api.mapbox.com/v4/mapbox.mapbox-terrain-v2/tilequery/{lon},{lat}.json"

# Terrain window ~120 m
WINDOW_METERS = 120

# Grid resolution (5x5 = 25 samples)
GRID_SIZE = 5

# Max physically meaningful terrain slope for agriculture
MAX_VALID_SLOPE = 60.0  # percent

# =========================
# INTERNAL UTILITIES
# =========================

def _meters_to_deg_lat(m):
    return m / 111_320


def _meters_to_deg_lon(m, lat):
    return m / (111_320 * math.cos(math.radians(lat)))


def _get_elevation(lat, lon):
    """
    Fetch nearest terrain elevation from Mapbox contours
    """
    url = MAPBOX_URL.format(lat=lat, lon=lon)
    params = {
        "layers": "contour",
        "access_token": MAPBOX_TOKEN
    }

    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()

    data = resp.json()
    features = data.get("features", [])

    if not features:
        raise RuntimeError("No elevation data from Mapbox")

    return features[0]["properties"]["ele"]


def _compute_local_slope(z_center, z_north, z_east, dx, dy):
    dz_dx = (z_east - z_center) / dx
    dz_dy = (z_north - z_center) / dy
    return math.sqrt(dz_dx**2 + dz_dy**2) * 100


# =========================
# PUBLIC API
# =========================

def get_slope(lat, lon):
    """
    Compute terrain-averaged slope (%) using median aggregation
    """

    # Convert window to degrees
    half = WINDOW_METERS / 2
    dlat = _meters_to_deg_lat(half)
    dlon = _meters_to_deg_lon(half, lat)

    # Step size between grid points
    lat_step = (2 * dlat) / (GRID_SIZE - 1)
    lon_step = (2 * dlon) / (GRID_SIZE - 1)

    elevations = {}

    # 1️⃣ Sample elevations
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            sample_lat = lat - dlat + i * lat_step
            sample_lon = lon - dlon + j * lon_step
            elevations[(i, j)] = _get_elevation(sample_lat, sample_lon)

    # Convert degree step to meters
    dx = lon_step * 111_320 * math.cos(math.radians(lat))
    dy = lat_step * 111_320

    slopes = []

    # 2️⃣ Compute local slopes (central difference)
    for i in range(1, GRID_SIZE - 1):
        for j in range(1, GRID_SIZE - 1):
            zc = elevations[(i, j)]
            zn = elevations[(i + 1, j)]
            ze = elevations[(i, j + 1)]

            s = _compute_local_slope(zc, zn, ze, dx, dy)
            slopes.append(s)

    if not slopes:
        return 0.0

    # 3️⃣ Median slope (robust)
    median_slope = statistics.median(slopes)

    # 4️⃣ Sanity clamp (terrain artifact filter)
    if median_slope > MAX_VALID_SLOPE:
        return round(MAX_VALID_SLOPE, 2)

    return round(median_slope, 2)

# geo/arable_classifier.py
# FINAL PRODUCTION VERSION
# ESRI Global Land Cover based arable classification (ICAR-safe)

import os
import rasterio
from rasterio.warp import transform
from collections import Counter

LANDCOVER_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "landcover"
)

# ESRI Global Land Cover (Impact Observatory) — OFFICIAL CLASSES
ESRI_CLASS_LABELS = {
    1: "WATER",
    2: "TREES",
    3: "GRASS",
    4: "FLOODED_VEGETATION",
    5: "CROPLAND",
    6: "SHRUB_SCRUB",
    7: "BUILT_UP",
    8: "BARE_GROUND",
    9: "SNOW_ICE",
    10: "CLOUDS",
    11: "RANGELAND"
}

ARABLE_CLASSES = {5}  # CROPLAND ONLY
NON_ARABLE_CLASSES = set(ESRI_CLASS_LABELS.keys()) - ARABLE_CLASSES


def _landcover_files():
    files = [
        os.path.join(LANDCOVER_DIR, f)
        for f in os.listdir(LANDCOVER_DIR)
        if f.lower().endswith(".tif")
    ]
    if not files:
        raise RuntimeError("No ESRI land cover GeoTIFFs found")
    return files


def is_arable_land(lat: float, lon: float, slope_percent: float):
    """
    Returns:
        (is_arable: bool, reason: str)
    """

    # 1️⃣ ICAR hard constraint: slope
    if slope_percent > 33:
        return False, "Slope > 33% (ICAR non-arable)"

    # 2️⃣ Land cover check
    for tif in _landcover_files():
        with rasterio.open(tif) as src:
            # Reproject point to raster CRS
            try:
                x, y = transform(
                    "EPSG:4326",
                    src.crs,
                    [lon],
                    [lat]
                )
                x, y = x[0], y[0]
            except Exception:
                continue

            # Bounds check
            if not (
                src.bounds.left <= x <= src.bounds.right and
                src.bounds.bottom <= y <= src.bounds.top
            ):
                continue

            # Sample 3×3 window
            row, col = src.index(x, y)
            window = src.read(
                1,
                window=((row - 1, row + 2), (col - 1, col + 2)),
                boundless=True
            )

            values = [int(v) for v in window.flatten() if v > 0]
            if not values:
                return False, "Invalid land cover data"

            majority = Counter(values).most_common(1)[0][0]
            label = ESRI_CLASS_LABELS.get(majority, "UNKNOWN")

            if majority in ARABLE_CLASSES:
                return True, "Cropland (ESRI Land Cover)"

            return False, f"Non-arable land cover ({label})"

    return False, "Location outside land cover coverage"

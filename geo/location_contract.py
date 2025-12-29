from dataclasses import dataclass


@dataclass
class LocationFactors:
    latitude: float
    longitude: float

    land_use: str

    rainfall_mm: float
    slope_percent: float

    soil_depth: str      # SHALLOW | MEDIUM | DEEP
    drainage: str        # POOR | MODERATE | GOOD

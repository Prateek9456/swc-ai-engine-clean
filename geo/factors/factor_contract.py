from dataclasses import dataclass
from geo.factors.enums import SoilDepth, Drainage, LandUse

@dataclass
class Factors:
    rainfall_mm: float
    slope_percent: float
    soil_depth: SoilDepth
    drainage: Drainage
    land_use: LandUse

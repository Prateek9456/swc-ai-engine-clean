from enum import Enum

class Rainfall(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"

class Slope(Enum):
    GENTLE = "gentle"
    MODERATE = "moderate"
    STEEP = "steep"
    VERY_STEEP = "very_steep"

class SoilDepth(Enum):
    SHALLOW = "shallow"
    MEDIUM = "medium"
    DEEP = "deep"

class Drainage(Enum):
    POOR = "poor"
    MODERATE = "moderate"
    GOOD = "good"

class LandUse(Enum):
    PADDY = "paddy"
    SMALL_MILLETS = "small_millets"
    PLANTATION = "plantation"
    VEGETABLES = "vegetables"
    ROOT_CROPS = "root_crops"
    FOREST = "forest"

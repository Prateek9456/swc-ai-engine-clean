from geo.sensors.rainfall_sensor import fetch_rainfall_mm
from geo.sensors.slope_sensor import fetch_slope_percent
from geo.sensors.soil_depth_sensor import fetch_soil_depth_class
from geo.sensors.soil_drainage_sensor import fetch_soil_drainage
from geo.location_contract import LocationFactors




def build_factors(lat, lon, land_use, overrides=None):
    overrides = overrides or {}

    rainfall = overrides.get("rainfall_mm") or fetch_rainfall_mm(lat, lon)
    slope = overrides.get("slope_percent") or fetch_slope_percent(lat, lon)

    soil_depth = overrides.get("soil_depth") or fetch_soil_depth_class(lat, lon)
    drainage = overrides.get("drainage") or fetch_soil_drainage(slope, rainfall)

    return LocationFactors(
        latitude=lat,
        longitude=lon,
        land_use=land_use,
        rainfall_mm=rainfall,
        slope_percent=slope,
        soil_depth=soil_depth,
        drainage=drainage
    )

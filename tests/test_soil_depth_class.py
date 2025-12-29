from geo.sensors.soil_depth_sensor import fetch_soil_depth_class

test_cases = [
    ("Flat + good drainage", 2.0, "GOOD"),
    ("Flat + moderate drainage", 4.0, "MODERATE"),
    ("Moderate slope", 10.0, "GOOD"),
    ("Steep slope", 18.0, "GOOD"),
    ("Steep + poor drainage", 20.0, "POOR"),
]

for name, slope, drainage in test_cases:
    depth = fetch_soil_depth_class(slope, drainage)
    print(f"{name}: {depth}")

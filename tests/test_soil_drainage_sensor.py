from geo.sensors.soil_drainage_sensor import fetch_soil_drainage

test_cases = {
    "Delhi": (1.5, 650),
    "Dehradun": (8.0, 2100),
    "Manali": (18.0, 1600),
    "Kerala": (3.0, 3000),
    "Rajasthan": (1.0, 200),
}

for name, (slope, rainfall) in test_cases.items():
    drainage = fetch_soil_drainage(slope, rainfall)
    print(f"{name}: {drainage}")

REQUIRED_FIELDS = ["category", "practice", "conditions"]

REQUIRED_CONDITIONS = [
    "slope_percent",
    "rainfall_mm",
    "land_use"
]

def validate_rule(rule):
    for field in REQUIRED_FIELDS:
        if field not in rule:
            raise ValueError(f"Missing field {field} in rule")

    conditions = rule["conditions"]

    for cond in REQUIRED_CONDITIONS:
        if cond not in conditions:
            raise ValueError(
                f"Missing condition '{cond}' in rule: {rule['practice']}"
            )

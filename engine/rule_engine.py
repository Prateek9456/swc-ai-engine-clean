import json


def load_rules(path):
    with open(path, "r") as f:
        return json.load(f)


def rule_matches(rule, factors, ignore_land_use=False):
    slope = factors.slope_percent
    rainfall = factors.rainfall_mm
    soil_depth = factors.soil_depth
    drainage = factors.drainage

    # ---- slope ----
    if "slope_max" in rule and slope > rule["slope_max"]:
        return False
    if "slope_range" in rule:
        lo, hi = rule["slope_range"]
        if not (lo <= slope <= hi):
            return False

    # ---- rainfall ----
    if "rainfall_min" in rule and rainfall < rule["rainfall_min"]:
        return False
    if "rainfall_max" in rule and rainfall > rule["rainfall_max"]:
        return False

    # ---- soil depth ----
    if soil_depth not in rule["soil_depth"]:
        return False

    # ---- drainage ----
# ---- drainage (optional constraint) ----
    if "drainage" in rule:
        if drainage not in rule["drainage"]:
            return False


    # ---- land use (optional) ----
    if not ignore_land_use:
        if factors.land_use not in rule["land_use"]:
            return False

    return True


def evaluate_rules(factors, rule_file):
    rules = load_rules(rule_file)

    # STAGE 1 — strict (with land use)
    strict = [
        r["measure"]
        for r in rules
        if rule_matches(r, factors, ignore_land_use=False)
    ]

    if strict:
        return {
            "mode": "STRICT",
            "measures": strict
        }

    # STAGE 2 — relaxed (ignore land use)
    relaxed = [
        r["measure"]
        for r in rules
        if rule_matches(r, factors, ignore_land_use=True)
    ]

    return {
        "mode": "RELAXED",
        "measures": relaxed
    }

def compute_erosion_risk(factors):

    if factors.slope == "STEEP" and factors.rainfall == "HIGH":
        return {"risk_level": "HIGH"}

    if factors.slope == "MODERATE" or factors.rainfall == "MODERATE":
        return {"risk_level": "MODERATE"}

    return {"risk_level": "LOW"}

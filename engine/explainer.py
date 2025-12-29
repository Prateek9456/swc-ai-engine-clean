def explain(factors, measures, risk):
    return (
        f"Based on a {factors.slope.name.lower()} slope and "
        f"{factors.rainfall.name.lower()} rainfall conditions, "
        f"the erosion risk is assessed as {risk}. "
        f"ICAR recommends {', '.join(measures)}."
    )

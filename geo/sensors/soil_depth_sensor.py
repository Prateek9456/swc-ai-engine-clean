def fetch_soil_depth_class(slope_percent, drainage):
    """
    Returns ICAR soil depth class:
    SHALLOW / MEDIUM / DEEP

    Derived using ICAR-consistent terrain interpretation.
    """

    # ICAR: deep soils on gentle slopes with good drainage
    if slope_percent < 6 and drainage in ["GOOD", "MODERATE"]:
        return "DEEP"

    # ICAR: medium soils on moderate slopes
    if slope_percent < 15:
        return "MEDIUM"

    # ICAR: shallow soils on steep slopes
    return "SHALLOW"

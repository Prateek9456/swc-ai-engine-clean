import numpy as np
import math


def compute_slope_percent(dem_array, transform):
    """
    Compute average slope (%) from a DEM array
    using Horn's method (standard GIS approach).
    """

    # Pixel resolution
    x_res = transform.a
    y_res = -transform.e

    dzdx = np.gradient(dem_array, axis=1) / x_res
    dzdy = np.gradient(dem_array, axis=0) / y_res

    slope_rad = np.arctan(np.sqrt(dzdx**2 + dzdy**2))
    slope_percent = np.tan(slope_rad) * 100

    return float(np.nanmean(slope_percent))

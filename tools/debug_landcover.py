#!/usr/bin/env python3
"""
tools/debug_landcover.py

Usage:
  # single point
  python tools/debug_landcover.py --lat 34.0837 --lon 74.8204

  # multiple points (space-separated pairs)
  python tools/debug_landcover.py --points "30.9,75.85" "34.0837,74.8204"

This script:
 - lists landcover .tif files in data/landcover
 - for each file prints CRS, bounds, meta
 - transforms the input WGS84 point to raster CRS
 - checks whether point is inside that raster
 - prints row/col, 3x3 window values and majority
 - prints a histogram (unique values and counts) for the tile (or a clipped window)
 - prints any colormap/tags available
"""
import os
import argparse
from collections import Counter

import numpy as np
import rasterio
from rasterio.warp import transform

BASE = os.path.dirname(os.path.dirname(__file__))
LANDCOVER_DIR = os.path.join(BASE, "data", "landcover")


def find_tifs():
    if not os.path.isdir(LANDCOVER_DIR):
        raise SystemExit(f"Landcover directory not found: {LANDCOVER_DIR}")
    tifs = [os.path.join(LANDCOVER_DIR, f) for f in sorted(os.listdir(LANDCOVER_DIR)) if f.lower().endswith(".tif")]
    return tifs


def analyze_file(tif, lat, lon, sample_hist_window_size=5000):
    print("\n--- Checking file ---")
    print("File:", tif)
    with rasterio.open(tif) as src:
        print("Driver:", src.driver)
        print("Width x Height:", src.width, "x", src.height)
        print("Count (bands):", src.count)
        print("Dtype:", src.dtypes)
        print("CRS:", src.crs)
        print("Transform:", src.transform)
        print("Bounds:", src.bounds)
        tags = src.tags()
        if tags:
            print("Tags:", tags)
        # any colormap?
        try:
            cmap = src.colormap(1)
            if cmap:
                print("Colormap (sample entries):", dict(list(cmap.items())[:10]))
        except Exception:
            pass

        # transform point to raster CRS
        try:
            x, y = transform("EPSG:4326", src.crs, [lon], [lat])
            x, y = float(x[0]), float(y[0])
            print("Transformed (x,y):", x, y)
        except Exception as e:
            print("Transform failed:", e)
            return None

        inside = (src.bounds.left <= x <= src.bounds.right and src.bounds.bottom <= y <= src.bounds.top)
        print("Inside bounds:", inside)
        if not inside:
            return {"file": tif, "inside": False}

        # compute row, col and sample window
        try:
            row, col = src.index(x, y)
            print("Raster row, col:", row, col)
        except Exception as e:
            print("Indexing failed:", e)
            return {"file": tif, "inside": True, "index_error": str(e)}

        # 3x3 window
        window = src.read(1, window=((row - 1, row + 2), (col - 1, col + 2)), boundless=True)
        flat = window.flatten().tolist()
        print("Window 3x3 values:", flat)
        values = [int(v) for v in flat if v is not None and not (isinstance(v, float) and np.isnan(v))]
        if not values:
            print("Window contained no valid values (all nodata?)")
        else:
            majority = Counter(values).most_common(1)[0]
            print("Majority value (value, count):", majority)

        # quick histogram of the tile: to avoid loading huge arrays, sample a decimated grid
        try:
            # sample a window around point with radius sample_hist_window_size meters using pixel size
            px_width = src.transform.a
            if px_width == 0:
                # fallback: compute histogram on entire band (may be large)
                arr = src.read(1)
                unique, counts = np.unique(arr, return_counts=True)
            else:
                # determine pixel radius
                radius_px = int(max(5, sample_hist_window_size / abs(px_width)))
                r0 = max(0, row - radius_px)
                r1 = min(src.height, row + radius_px)
                c0 = max(0, col - radius_px)
                c1 = min(src.width, col + radius_px)
                print(f"Histogram window rows {r0}:{r1}, cols {c0}:{c1} (radius_px={radius_px})")
                arr = src.read(1, window=((r0, r1), (c0, c1)), boundless=True)
                # decimate if too large
                max_pixels = 5_000_000
                if arr.size > max_pixels:
                    step = int(np.ceil(np.sqrt(arr.size / max_pixels)))
                    arr = arr[::step, ::step]
                unique, counts = np.unique(arr, return_counts=True)
            hist = dict(zip([int(u) for u in unique], [int(c) for c in counts]))
            # show top classes
            sorted_hist = sorted(hist.items(), key=lambda it: it[1], reverse=True)
            print("Tile histogram (top 20 classes):")
            for v, cnt in sorted_hist[:20]:
                print("  value:", v, "count:", cnt)
        except Exception as e:
            print("Histogram computation failed:", e)

        return {"file": tif, "inside": True, "row": row, "col": col, "window": flat}

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--lat", type=float, help="Latitude (WGS84)")
    p.add_argument("--lon", type=float, help="Longitude (WGS84)")
    p.add_argument("--points", nargs="*", help='Points as "lat,lon" strings', default=[])
    p.add_argument("--hist-window-m", type=int, default=5000, help="Histogram window approx meters (default 5000)")
    return p.parse_args()

def main():
    args = parse_args()
    pts = []
    if args.lat is not None and args.lon is not None:
        pts.append((args.lat, args.lon))
    for s in args.points:
        try:
            lat, lon = s.split(",")
            pts.append((float(lat.strip()), float(lon.strip())))
        except Exception:
            print("Invalid point format:", s)
    if not pts:
        print("No points provided. Use --lat --lon or --points")
        return
    tifs = find_tifs()
    print("Found tif count:", len(tifs))
    for lat, lon in pts:
        print("\n\n================== POINT ==================")
        print("Point (lat,lon):", lat, lon)
        any_inside = False
        for tif in tifs:
            res = analyze_file(tif, lat, lon, sample_hist_window_size=args.hist_window_m)
            if res and res.get("inside"):
                any_inside = True
        if not any_inside:
            print("No tile contained this point.")

if __name__ == "__main__":
    main()

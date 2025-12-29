CACHE = {}

def get_cached(lat, lon):
    return CACHE.get((lat, lon))

def set_cache(lat, lon, value):
    CACHE[(lat, lon)] = value

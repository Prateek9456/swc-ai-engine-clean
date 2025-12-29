from geo.geocoder import reverse_geocode

def resolve_location(lat, lon):
    """
    Resolves administrative context from GPS.
    Subdivision logic intentionally removed.
    """
    location = reverse_geocode(lat, lon)

    return {
        "latitude": lat,
        "longitude": lon,
        "state": location.get("state"),
        "district": location.get("district")
    }

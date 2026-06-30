from models.location import Location

def normalize_location(location: Location) -> Location:
    if location.city:
        location.city = location.city.strip().title()
    if location.region:
        location.region = location.region.strip().title()
    if location.country:
        location.country = location.country.strip().title()
    return location
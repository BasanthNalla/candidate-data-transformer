import pycountry
from models.location import Location

def normalize_location(location: Location) -> Location:
    if location.city:
        location.city = location.city.strip().title()
    if location.region:
        location.region = location.region.strip().title()
    if location.country:
        location.country = _country_to_alpha2(location.country.strip())
    return location

def _country_to_alpha2(country_str: str) -> str:
    if not country_str:
        return country_str
    
    if len(country_str) == 2:
        result = pycountry.countries.get(alpha_2=country_str.upper())
        if result: return result.alpha_2
        
    try:
        results = pycountry.countries.search_fuzzy(country_str)
        if results: return results[0].alpha_2
    except LookupError:
        pass
        
    return country_str
import re

def split_date_range(date_range: str) -> tuple[str | None, str | None]:
    if not date_range:
        return None, None
    date_range = date_range.strip()
    
    pattern = re.compile(r'\s*(?:[-–—]|\bto\b)\s*', re.IGNORECASE)
    parts = pattern.split(date_range, maxsplit=1)
    
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return date_range, None
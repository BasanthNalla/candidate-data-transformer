import re

def split_date_range(date_range: str) -> tuple[str | None, str | None]:
    if not date_range:
        return None, None
    date_range = date_range.strip()
    separators = ["-", "to"]
    for sep in separators:
        if sep in date_range:
            start, end = date_range.split(sep, 1)
            return start.strip(), end.strip()
    return date_range, None
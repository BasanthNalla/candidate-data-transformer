import dateparser

def normalize_date(date_str: str) -> str | None:
    if not date_str:
        return None
    date_str = date_str.strip()
    if date_str.lower() in ["present", "current", "ongoing"]:
        return "Present"
    dt = dateparser.parse(date_str)
    if dt is None:
        return date_str
    if len(date_str)==4 and date_str.isdigit():
        return dt.strftime("%Y")
    return dt.strftime("%Y-%m")
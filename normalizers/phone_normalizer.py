import phonenumbers

def normalize_phone(phone: str) -> str:
    if not phone:
        return ""
    try:
        parsed = phonenumbers.parse(phone, "IN")
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except Exception:
        pass
    return phone.strip()
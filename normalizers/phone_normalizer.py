import phonenumbers

def normalize_phone(phone: str) -> str | None:
    if not phone:
        return None
    phone = phone.strip()
    if phone.endswith(".0"):
        phone = phone[:-2]
    
    for region in [None, "IN", "US"]:
        try:
            parsed = phonenumbers.parse(phone, region)
            if phonenumbers.is_valid_number(parsed):
                return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        except Exception:
            continue
            
    return phone.strip()
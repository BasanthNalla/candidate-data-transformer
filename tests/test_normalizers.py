import pytest
from normalizers.phone_normalizer import normalize_phone
from normalizers.location_normalizer import _country_to_alpha2
from normalizers.skill_normalizer import normalize_skill
from normalizers.email_normalizer import normalize_email

def test_phone_e164_indian():
    assert normalize_phone("+919876543210") == "+919876543210"
    assert normalize_phone("09876543210") == "+919876543210"

def test_phone_e164_us():
    assert normalize_phone("+12025551234") == "+12025551234"

def test_phone_invalid():
    assert normalize_phone("not-a-phone") == "not-a-phone"

def test_country_iso3166():
    assert _country_to_alpha2("India") == "IN"
    assert _country_to_alpha2("United States") == "US"
    assert _country_to_alpha2("US") == "US"

def test_country_unknown():
    assert _country_to_alpha2("Narnia") == "Narnia"

def test_email_lowercase():
    assert normalize_email("John@Gmail.COM") == "john@gmail.com"

def test_skill_canonical():
    assert normalize_skill("js") == "JavaScript"
    assert normalize_skill("ML") == "Machine Learning"
    assert normalize_skill("unknown_skill") == "Unknown_Skill"

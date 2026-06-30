import pytest
from validator.candidate_validator import CandidateValidator
from models.candidate import Candidate
from models.provenance import Provenance
from models.skill import Skill
from models.location import Location
from models.link import Link

def test_validator_valid():
    cand = Candidate(
        candidate_id="1", full_name="Test User", emails=["test@example.com"], phones=[], location=Location(), links=Link(),
        overall_confidence=0.9
    )
    cand.provenance = [
        Provenance(field="email", value="test@example.com", source="Resume", method="Parsed")
    ]
    validator = CandidateValidator()
    assert validator.validate(cand) is True

def test_validator_missing_name():
    cand = Candidate(
        candidate_id="1", full_name="", emails=["test@example.com"], phones=[], location=Location(), links=Link()
    )
    validator = CandidateValidator()
    with pytest.raises(ValueError, match="empty"):
        validator.validate(cand)

def test_validator_duplicate_skill():
    cand = Candidate(
        candidate_id="1", full_name="Test User", emails=["test@example.com"], phones=[], location=Location(), links=Link()
    )
    cand.skills = [
        Skill(name="Python", confidence=1.0, sources=[]),
        Skill(name="python", confidence=1.0, sources=[])
    ]
    validator = CandidateValidator()
    with pytest.raises(ValueError, match="Duplicate skill"):
        validator.validate(cand)

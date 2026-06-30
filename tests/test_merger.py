from models.candidate import Candidate, Skill, Location, Experience, Education
from models.link import Link
from merger.candidate_merger import CandidateMerger
from merger.confidence import ConfidenceCalculator

def make_candidate(**kwargs):
    default = {
        "candidate_id": "test",
        "full_name": "Test",
        "emails": [],
        "phones": [],
        "location": Location(city=None, region=None, country=None),
        "links": Link(linkedin=None, github=None, portfolio=None, other=[])
    }
    default.update(kwargs)
    return Candidate(**default)

def test_merge_emails_dedup():
    c1 = make_candidate(emails=["john@example.com"])
    c2 = make_candidate(emails=["john@example.com", "john2@example.com"])
    merger = CandidateMerger([("Source1", c1), ("Source2", c2)])
    merged = merger.merge()
    assert len(merged.emails) == 2
    assert "john@example.com" in merged.emails

def test_merge_skills_single_source():
    c1 = make_candidate(skills=[Skill(name="Python", confidence=0.9, sources=["Source1"])])
    merger = CandidateMerger([("Source1", c1)])
    merged = merger.merge()
    assert len(merged.skills) == 1
    assert merged.skills[0].name == "Python"
    assert merged.skills[0].sources == ["Source1"]

def test_merge_skills_multi_source():
    c1 = make_candidate(skills=[Skill(name="Python", confidence=0.9, sources=["Source1"])])
    c2 = make_candidate(skills=[Skill(name="Python", confidence=0.9, sources=["Source2"])])
    merger = CandidateMerger([("Source1", c1), ("Source2", c2)])
    merged = merger.merge()
    assert len(merged.skills) == 1
    assert sorted(merged.skills[0].sources) == sorted(["Source1", "Source2"])

def test_merge_location_fill():
    c1 = make_candidate(location=Location(city="San Francisco", region=None, country=None))
    c2 = make_candidate(location=Location(city=None, region=None, country="US"))
    merger = CandidateMerger([("Source1", c1), ("Source2", c2)])
    merged = merger.merge()
    assert merged.location.city == "San Francisco"
    assert merged.location.country == "US"

def test_pick_prefers_first_non_null():
    c1 = make_candidate(full_name="")
    c2 = make_candidate(full_name="John")
    merger = CandidateMerger([("Source1", c1), ("Source2", c2)])
    merged = merger.merge()
    assert merged.full_name == "John"

def test_merge_returns_none_on_empty_sources():
    merger = CandidateMerger([])
    assert merger.merge() is None

def test_confidence_with_email():
    c = make_candidate(emails=["test@example.com"], skills=[Skill(name="Python", confidence=0.9, sources=["s"])])
    calc = ConfidenceCalculator()
    c = calc.calculate(c)
    assert c.overall_confidence > 0

def test_confidence_no_skills_no_links():
    c = make_candidate(full_name="John")
    calc = ConfidenceCalculator()
    c = calc.calculate(c)
    assert c.overall_confidence == 0.0

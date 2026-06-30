import os
from parsers.csv_parser import CSVParser
from parsers.resume_parser import ResumeParser
from models.candidate import Candidate, Skill
from models.location import Location
from models.link import Link

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

def get_csv_candidates():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "input", "recruiter.csv")
    return CSVParser(csv_path).parse()

def test_alice_walker_no_email():
    candidates = get_csv_candidates()
    alice = [c for c in candidates if c.full_name == "Alice Walker"][0]
    assert len(alice.emails) == 0

def test_resume_no_skills_section():
    parser = ResumeParser("dummy.pdf")
    skills = parser._extract_skills("")
    assert len(skills) == 0

def test_csv_only_no_resume():
    candidates = get_csv_candidates()
    assert len(candidates) == 7

def test_resume_only_no_csv():
    resume_path = os.path.join(os.path.dirname(__file__), "..", "input", "resume.pdf")
    parser = ResumeParser(resume_path)
    c = parser.parse()
    assert c.full_name == "BASANTH NALLA"

def test_duplicate_skill_in_csv():
    c = make_candidate(skills=[Skill(name="Python", confidence=0.9, sources=["CSV"]), 
                               Skill(name="Python", confidence=0.9, sources=["CSV"]), 
                               Skill(name="Java", confidence=0.9, sources=["CSV"])])
    from merger.candidate_merger import CandidateMerger
    m = CandidateMerger([("CSV", c)])
    merged = m.merge()
    assert len(merged.skills) == 2

def test_corrupt_years_field():
    parser = CSVParser("dummy.csv")
    assert parser._parse_years("three years") is None

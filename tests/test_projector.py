import pytest
from projector.config_loader import ConfigLoader
from projector.field_resolver import FieldResolver
from projector.projector import Projector
from models.candidate import Candidate
from models.skill import Skill
from models.location import Location
from models.link import Link

def test_field_resolver():
    cand = Candidate(
        candidate_id="1", full_name="Test User", emails=["test@example.com"], phones=[], location=Location(), links=Link()
    )
    cand.skills = [Skill(name="Python", confidence=1.0, sources=["Resume"])]
    
    resolver = FieldResolver()
    
    val, found = resolver.resolve(cand, "full_name")
    assert found and val == "Test User"
    
    val, found = resolver.resolve(cand, "emails[0]")
    assert found and val == "test@example.com"
    
    val, found = resolver.resolve(cand, "skills[].name")
    assert found and val == ["Python"]
    
    val, found = resolver.resolve(cand, "missing_field")
    assert not found

def test_projector():
    config = {
        "fields": [
            {"path": "name", "from": "full_name", "type": "string"},
            {"path": "email", "from": "emails[0]", "type": "string"},
            {"path": "missing_field", "type": "string"}
        ],
        "on_missing": "null"
    }
    
    cand = Candidate(
        candidate_id="1", full_name="Test User", emails=["test@example.com"], phones=[], location=Location(), links=Link()
    )
    
    proj = Projector(config)
    output = proj.project(cand)
    
    assert output["name"] == "Test User"
    assert output["email"] == "test@example.com"
    assert output["missing_field"] is None

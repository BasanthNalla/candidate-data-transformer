from pydantic import BaseModel, Field
from typing import Optional
from models.skill import Skill
from models.location import Location
from models.link import Link
from models.experience import Experience
from models.education import Education
from models.provenance import Provenance

class Candidate(BaseModel):
    candidate_id: str
    full_name: str
    emails: list[str]
    phones: list[str]
    location: Location
    links: Link
    headline: Optional[str] = None
    years_experience: Optional[float] = None
    skills: list[Skill] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    provenance: list[Provenance] = Field(default_factory=list)
    overall_confidence: float = 0.0
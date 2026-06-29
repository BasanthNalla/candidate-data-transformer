from pydantic import BaseModel

class Skill(BaseModel):
    name: str
    confidence: float
    sources: list[str]
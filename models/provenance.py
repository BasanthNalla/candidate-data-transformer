from pydantic import BaseModel

class Provenance(BaseModel):
    field: str
    source: str
    method: str
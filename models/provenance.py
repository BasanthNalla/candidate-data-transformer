from pydantic import BaseModel

class Provenance(BaseModel):
    field: str
    value: str
    source: str
    method: str
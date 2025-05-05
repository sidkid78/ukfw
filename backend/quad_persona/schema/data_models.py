from typing import List, Dict, Optional
from pydantic import BaseModel

class PersonaMetadata(BaseModel):
    persona_type: str                  # e.g. "Knowledge Expert"
    name: str
    job_roles: List[str]
    skills: List[str]
    certifications: List[str]
    training: List[str]
    education: List[str]
    research_base: List[str]

class PersonaTrace(BaseModel):
    persona: PersonaMetadata
    step: int
    title: str
    summary: str
    details: Optional[str]

class QuadPersonaResponse(BaseModel):
    query: str
    trace: List[PersonaTrace]          # Each persona's stepwise contribution
    final_response: str

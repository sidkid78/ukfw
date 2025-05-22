from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

class EducationRequirement(BaseModel):
    degree: str
    field_of_study: str
    institution: Optional[str] = None

class CertificationLicense(BaseModel):
    name: str
    issuing_authority: Optional[str] = None
    license_number: Optional[str] = None

class Publication(BaseModel):
    title: str
    authors: List[str] = Field(default_factory=list)
    journal_or_conference: Optional[str] = None
    year: Optional[int] = None
    url_or_doi: Optional[str] = None

class PersonaProfile(BaseModel):
    profile_id: str 
    persona_archetype: str 
    name: str 
    description: Optional[str] = Field(None, description="A brief description of this persona and its typical focus.")
    job_title_exemplar: Optional[str] = Field(None, description="A typical job title this persona might hold, e.g., 'Chief Compliance Officer'.")
    ukg_axes: List[str] = Field(default_factory=list, description="List of UKG Axis IDs this persona is primarily associated with.")
    domain_expertise: List[str] = Field(default_factory=list, description="Broad areas of expertise, e.g., 'Aerospace Engineering', 'Contract Law'.")
    industry_sectors: List[str] = Field(default_factory=list, description="Specific industry sectors of focus, e.g., 'Commercial Aviation', 'Pharmaceuticals'.")
    education: List[EducationRequirement] = Field(default_factory=list)
    certifications_licenses: List[CertificationLicense] = Field(default_factory=list)
    professional_training: List[str] = Field(default_factory=list)
    publications_or_research: List[Publication] = Field(default_factory=list)
    experience_level: Optional[str] = Field(None, description="e.g., 'Senior', 'Lead', 'Consultant'")
    key_responsibilities_or_tasks: List[str] = Field(default_factory=list)
    behavioral_traits: List[str] = Field(default_factory=list, description="Simulated behavioral characteristics, e.g., 'meticulous', 'pragmatic', 'innovative'.")
    simulation_parameters: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Custom parameters for the simulation logic, e.g., LLM temperature, specific heuristic weights.")
    source_data_references: List[Dict[str, str]] = Field(default_factory=list, description="Structured references (e.g., type, id) to documents or UKG nodes used to define or instantiate this persona.")
    custom_properties: Optional[Dict[str, Any]] = Field(default_factory=dict, description="For additional, dynamic properties not covered by the schema.")

    class Config:
        json_schema_extra = {
            "example": {
                "profile_id": "persona-knowledge-aerospace-001",
                "persona_archetype": "KnowledgeExpert",
                "name": "Dr. Elara Vance",
                "description": "Specializes in advanced aerospace propulsion systems and theoretical physics.",
                "job_title_exemplar": "Principal Research Scientist - Propulsion",
                "ukg_axes": ["AXIS_AERO_PROPULSION", "AXIS_THEORETICAL_PHYSICS"],
                "domain_expertise": ["Ion Drives", "Plasma Physics", "Relativistic Mechanics"],
                "industry_sectors": ["Space Exploration", "Satellite Technology"],
                "education": [{"degree": "PhD", "field_of_study": "Aerospace Engineering", "institution": "MIT"}],
                "certifications_licenses": [{"name": "Fellow", "issuing_authority": "AIAA"}],
                "professional_training": ["Advanced Plasma Dynamics Workshop"],
                "publications_or_research": [{"title": "Next-Gen Ion Thrusters", "authors": ["Dr. Elara Vance"], "journal_or_conference": "Journal of Spacecraft and Rockets", "year": 2023}],
                "experience_level": "Senior Principal",
                "key_responsibilities_or_tasks": ["Fundamental research", "Theoretical model validation", "Mentoring junior scientists"],
                "behavioral_traits": ["analytical", "detail-oriented", "forward-thinking"],
                "simulation_parameters": {"llm_temperature_override": 0.6},
                "source_data_references": [{"type": "ukg_node_definition", "id": "UKG_NODE_PillarAero_Sublevel2_PropulsionExpert"}],
                "custom_properties": {"internal_project_code": "PROJ_X"},
            }
        }

class ReasoningStep(BaseModel):
    step_id: str # Changed from int to str for potentially more complex IDs (e.g., UUIDs or hierarchical like "1.2.1")
    description: Optional[str] = Field(None, description="Human-readable description of what this step accomplishes.")
    model_used: Optional[str] = Field(None, description="Identifier for the reasoning model used (e.g., 'ToT-Branch', 'AoT-Decomposition', 'LLM-GPT4.1').")
    persona_profile_id: str = Field(description="ID of the PersonaProfile that performed or is associated with this step.")
    persona_display_name: str # For easier display on frontend without another lookup
    input_context: Optional[Any] = Field(None, description="The primary input data or context for this reasoning step.")
    output_generated: Optional[Any] = Field(None, description="The primary output or result of this reasoning step.")
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score for the output of this step, if applicable.")
    knowledge_references: List[Dict[str, str]] = Field(default_factory=list, description="List of knowledge base entries or external sources referenced (e.g., {'source_id': 'KB_XYZ', 'type': 'regulation'}).")
    parent_step_id: Optional[str] = Field(None, description="ID of the parent step in a hierarchical reasoning process (e.g., ToT).")
    child_step_ids: List[str] = Field(default_factory=list, description="IDs of child steps, if this step decomposes into sub-steps (e.g., AoT).")
    start_time: Optional[datetime] = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = Field(None)
    self_reflection: Optional[str] = Field(None, description="Internal monologue or self-critique generated by the persona during this step.")
    issues_identified: List[str] = Field(default_factory=list, description="Any issues, gaps, or uncertainties identified during this step.")
    associated_axes: List[str] = Field(default_factory=list, description="UKG Axes relevant to or processed in this step.")
    status: Optional[str] = Field(None, description="Status of this step, e.g., 'completed', 'failed', 'pending_refinement'.")
    custom_step_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="For any additional model-specific or step-specific data.")

class ReasoningTrace(BaseModel):
    task_id: str
    request_timestamp: datetime = Field(default_factory=datetime.utcnow)
    original_query: Optional[Any] = Field(None, description="The initial query or input that triggered the reasoning task.")
    final_response_summary: Optional[str] = Field(None, description="A consolidated summary of the final outcome.")
    overall_confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    total_refinement_iterations: int = Field(0, description="Number of recursive refinement loops performed.")
    steps: List[ReasoningStep] = Field(default_factory=list)
    personas_involved_ids: List[str] = Field(default_factory=list, description="List of unique PersonaProfile IDs involved in the trace.")
    reasoning_models_used: List[str] = Field(default_factory=list, description="List of unique reasoning model identifiers used.")
    ukg_axes_queried: List[str] = Field(default_factory=list, description="List of unique UKG axes touched upon or queried during reasoning.")
    audit_trail_notes: List[str] = Field(default_factory=list, description="High-level notes on the reasoning process, refinement decisions, etc.")
    errors_encountered: List[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "task_id": "task-xyz-123",
                "request_timestamp": "2023-10-26T10:00:00Z",
                "original_query": "Analyze the impact of Regulation X on small businesses.",
                "final_response_summary": "Regulation X is likely to have a significant impact...",
                "overall_confidence_score": 0.85,
                "total_refinement_iterations": 1,
                "steps": [
                    {
                        "step_id": "step-001",
                        "description": "Initial analysis by Regulatory Expert.",
                        "model_used": "LLM-GPT4.1",
                        "persona_profile_id": "persona-regulatory-001",
                        "persona_display_name": "Dr. Lex",
                        "input_context": "Regulation X text",
                        "output_generated": "Identified key clauses A, B, C.",
                        "confidence_score": 0.9,
                        "knowledge_references": [{"source_id": "REG_X_DOC", "type": "document"}],
                        "start_time": "2023-10-26T10:00:05Z",
                        "end_time": "2023-10-26T10:00:15Z",
                        "associated_axes": ["AXIS_REGULATION_IMPACT"],
                        "status": "completed"
                    }
                    # ... more steps
                ],
                "personas_involved_ids": ["persona-regulatory-001", "persona-sector-smallbiz-002"],
                "reasoning_models_used": ["LLM-GPT4.1", "AoT-Decomposer"],
                "ukg_axes_queried": ["AXIS_REGULATION_IMPACT", "AXIS_SMALL_BUSINESS_OPS"],
                "audit_trail_notes": ["Initial pass completed. Identified need for sector expert input."],
                "errors_encountered": []
            }
        }

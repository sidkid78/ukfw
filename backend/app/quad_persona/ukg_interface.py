from typing import List, Dict
import random # For simulating dynamic elements

# Import the necessary data models
from .schema.data_models import (
    PersonaProfile, 
    EducationRequirement, 
    CertificationLicense, 
    Publication
)

# --- Placeholder Functions ---

def get_dynamic_persona_profile(query: str, archetype: str) -> PersonaProfile:
    """
    Placeholder function to simulate fetching a dynamic PersonaProfile.
    In a real implementation, this would query a UKG or database based on 
    the query context and the requested archetype.
    """
    print(f"[UKG Interface Placeholder] Fetching profile for archetype: {archetype} based on query: '{query[:50]}...'" )

    # --- Basic Mock Logic ---
    # Simulate finding slightly different profiles based on query keywords or archetype
    # This is highly simplified for demonstration.
    
    profile_id = f"dyn-{archetype.lower()}-{random.randint(100, 999)}"
    name = f"Dynamic {archetype}"
    job_title = f"Lead {archetype} Analyst"
    ukg_axes = [f"AXIS_{archetype.upper()}_DYN"]
    domains = [f"{archetype} Domain {random.randint(1, 5)} elicited by query"]
    education_details = [{"degree": "PhD", "field_of_study": f"{archetype} Studies"}]
    cert_names = [f"{archetype} Certified Pro"]
    tasks = [f"Dynamic Task for {archetype} based on query context"]
    
    # Add slight variations based on archetype
    if archetype == "KnowledgeExpert":
        name = "Dr. Dynamic Knowledge"
        job_title = "Principal Theoretical Researcher"
        ukg_axes = ["AXIS_THEORY_DYN", "AXIS_FUNDAMENTALS_DYN"]
        education_details = [{"degree": "PhD", "field_of_study": "Advanced Theory"}]
        cert_names = ["Advanced Theoretical Methods Cert"]
    elif archetype == "SectorExpert":
        name = "Ms. Dynamic Sector Lead"
        job_title = "Senior Industry Consultant"
        ukg_axes = ["AXIS_INDUSTRY_APP_DYN", "AXIS_PRACTICE_DYN"]
        education_details = [{"degree": "MBA", "field_of_study": "Sector Management"}]
        cert_names = ["Industry Leadership Fellow"]
    elif archetype == "RegulatoryExpert":
         name = "Mr. Dynamic Regulator"
         job_title = "Chief Policy Advisor"
         ukg_axes = ["AXIS_REGULATION_DYN", "AXIS_POLICY_DYN"]
         education_details = [{"degree": "LLM", "field_of_study": "Regulatory Law"}]
         cert_names = ["Certified Regulator"]
    elif archetype == "ComplianceExpert":
         name = "Mrs. Dynamic Compliance"
         job_title = "Head of Standards Assurance"
         ukg_axes = ["AXIS_COMPLIANCE_DYN", "AXIS_STANDARDS_DYN"]
         education_details = [{"degree": "MSc", "field_of_study": "Compliance & Risk Mgmt"}]
         cert_names = ["Lead Compliance Auditor"]


    # Construct the PersonaProfile object
    profile = PersonaProfile(
        profile_id=profile_id,
        persona_archetype=archetype,
        name=name,
        description=f"Dynamically generated profile for {archetype} based on query context.",
        job_title_exemplar=job_title,
        ukg_axes=ukg_axes,
        domain_expertise=domains,
        education=[EducationRequirement(**edu) for edu in education_details],
        certifications_licenses=[CertificationLicense(name=cert) for cert in cert_names],
        key_responsibilities_or_tasks=tasks,
        behavioral_traits=random.sample(["analytical", "pragmatic", "meticulous", "collaborative"], 2), # Simulate dynamic traits
        professional_training=["Dynamic Training Module Based on Query"],
        publications_or_research=[Publication(title=f"Dynamic Paper on {archetype}", authors=[name])],
        source_data_references=[
            {
                "type": "simulated_ukg_node", 
                "id": f"ukg_node_{archetype.lower()}_{random.randint(1000,9999)}",
                "description": f"Simulated UKG Node for {archetype} related to query: {query[:30]}..."
            }
        ] 
        # Add other fields with default/sample values if necessary
    )
    
    return profile

# --- New Planner Persona Profile Function ---
def get_planner_persona_profile() -> PersonaProfile:
    """
    Returns a pre-defined PersonaProfile for the Planner/Orchestrator.
    """
    archetype = "PlannerExpert"
    profile_id = f"static-planner-001"
    name = "Orchestrator Prime"
    job_title = "Chief Strategy & Reasoning Officer"
    
    profile = PersonaProfile(
        profile_id=profile_id,
        persona_archetype=archetype,
        name=name,
        description="Responsible for analyzing complex queries, decomposing them into manageable sub-tasks, and determining the optimal sequence of expert personas to involve for comprehensive reasoning.",
        job_title_exemplar=job_title,
        ukg_axes=["AXIS_STRATEGY_PLANNING", "AXIS_REASONING_ORCHESTRATION"],
        domain_expertise=["Query Analysis", "Problem Decomposition", "Workflow Optimization", "Multi-Agent Coordination"],
        education=[
            EducationRequirement(degree="PhD", field_of_study="Cognitive Science & AI Planning"),
            EducationRequirement(degree="MBA", field_of_study="Strategic Management")
        ],
        certifications_licenses=[
            CertificationLicense(name="Certified AI Planning Specialist"),
            CertificationLicense(name="Master Orchestrator Certification")
        ],
        key_responsibilities_or_tasks=[
            "Analyze initial query to understand core objectives.",
            "Identify key sub-questions or facets of the query.",
            "Determine the most relevant expert personas for each sub-question.",
            "Define the optimal sequence or parallel workflow for persona engagement.",
            "Specify the expected output or focus for each persona step.",
            "Ensure logical flow and coherence of the overall reasoning plan."
        ],
        behavioral_traits=["strategic", "analytical", "holistic-thinker", "decisive", "systems-oriented"],
        professional_training=["Advanced AI Orchestration Techniques", "Complex Systems Modelling"],
        publications_or_research=[
            Publication(title="Dynamic Orchestration of Multi-Persona Reasoning Systems", authors=[name], journal_or_conference="Journal of Advanced AI", year=2024)
        ],
        source_data_references=[
            {"type": "internal_model_config", "id": "planner_persona_v1_definition"}
        ]
        # Other fields can use defaults or be None
    )
    return profile

# --- New Synthesizer Persona Profile Function ---
def get_synthesizer_persona_profile() -> PersonaProfile:
    """
    Returns a pre-defined PersonaProfile for the Synthesizer.
    """
    archetype = "SynthesizerExpert"
    profile_id = f"static-synthesizer-001"
    name = "Consolidator Unit"
    job_title = "Chief Integration Officer"
    
    profile = PersonaProfile(
        profile_id=profile_id,
        persona_archetype=archetype,
        name=name,
        description="Responsible for reviewing the outputs of all preceding expert personas, consolidating findings, resolving minor discrepancies, and generating a final, coherent summary response to the original query.",
        job_title_exemplar=job_title,
        ukg_axes=["AXIS_SYNTHESIS", "AXIS_INTEGRATION"],
        domain_expertise=["Information Synthesis", "Multi-perspective Analysis", "Report Generation", "Clarity Enhancement"],
        education=[
            EducationRequirement(degree="MSc", field_of_study="Information Management & Synthesis")
        ],
        certifications_licenses=[
            CertificationLicense(name="Certified Knowledge Integrator")
        ],
        key_responsibilities_or_tasks=[
            "Review planner rationale and sequence.",
            "Analyze outputs from all executed expert steps.",
            "Identify key takeaways and consensus points.",
            "Note any unresolved conflicts or major uncertainties.",
            "Structure and synthesize a comprehensive final answer.",
            "Ensure the final answer directly addresses the original user query."
        ],
        behavioral_traits=["integrative", "concise", "objective", "structured", "clarity-focused"],
        professional_training=["Advanced Summarization Techniques", "Multi-source Data Fusion"],
        publications_or_research=[], # Synthesizers usually compile, not publish primary research
        source_data_references=[
            {"type": "internal_model_config", "id": "synthesizer_persona_v1_definition"}
        ]
    )
    return profile

# Example of how this might be used (will be called from main.py)
# if __name__ == '__main__':
#     test_query = "Analyze the safety protocols for nuclear reactor maintenance."
#     knowledge_prof = get_dynamic_persona_profile(test_query, "KnowledgeExpert")
#     compliance_prof = get_dynamic_persona_profile(test_query, "ComplianceExpert")
#     print("--- Knowledge Expert Profile ---")
#     print(knowledge_prof.model_dump_json(indent=2))
#     print("--- Compliance Expert Profile ---")
#     print(compliance_prof.model_dump_json(indent=2)) 
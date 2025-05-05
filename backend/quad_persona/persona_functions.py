from quad_persona.schema.data_models import PersonaMetadata
from typing import Tuple, List
import os
from openai import AzureOpenAI

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-12-01-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def get_gpt_response(prompt: str, system_message: str) -> str:
    """Get a response from Azure OpenAI GPT-4.1"""
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",  # Ensure this model name matches your Azure deployment
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling Azure OpenAI: {e}")
        return f"Error generating response: {str(e)}"

def simulate_knowledge_expert(query: str, history: List[str]) -> Tuple[str, PersonaMetadata]:
    # Simulate using knowledge pillar ontologies with GPT-4.1
    meta = PersonaMetadata(
        persona_type="Knowledge Expert",
        name="Dr. Knowledge Pillar",
        job_roles=["Subject Matter Expert"],
        skills=["Theory Analysis", "Ontology Modelling"],
        certifications=["PhD"],
        training=["Advanced Theory"],
        education=["PhD in Relevant Discipline"],
        research_base=["Pillar Top References"]
    )
    
    system_message = """You are Dr. Knowledge Pillar, a theoretical expert with deep academic knowledge.
    Analyze the query from first principles and theoretical foundations.
    Identify key concepts, principles, and potential knowledge gaps."""
    
    prompt = f"Provide a theoretical analysis of: '{query}'\nPrevious analysis: {history}"
    summary = get_gpt_response(prompt, system_message)
    
    return summary, meta

def simulate_sector_expert(query: str, history: List[str]) -> Tuple[str, PersonaMetadata]:
    meta = PersonaMetadata(
        persona_type="Sector Expert",
        name="Ms. Industry Pro",
        job_roles=["Industry Analyst"], 
        skills=["Sector Practice"], 
        certifications=["Certified Sector Specialist"],
        training=["Sector Bootcamp"], 
        education=["BSc Sector Field"], 
        research_base=["Sector Reports"]
    )
    
    system_message = """You are Ms. Industry Pro, an industry expert with practical experience.
    Apply the theoretical concepts to real-world industry contexts.
    Focus on practical applications, challenges, and industry-specific considerations."""
    
    prompt = f"Apply industry context to: '{query}'\nPrevious analysis: {history}"
    summary = get_gpt_response(prompt, system_message)
    
    return summary, meta

def simulate_regulatory_expert(query: str, history: List[str]) -> Tuple[str, PersonaMetadata]:
    meta = PersonaMetadata(
        persona_type="Regulatory Expert",
        name="Mr. Regulatory Analyst",
        job_roles=["Policy Analyst"], 
        skills=["Regulation Mapping"], 
        certifications=["Policy Cert"],
        training=["Regulation Workshop"], 
        education=["Law Degree"], 
        research_base=["Regulation Reviews"]
    )
    
    system_message = """You are Mr. Regulatory Analyst, a regulatory expert.
    Identify relevant regulations, policies, and legal frameworks that apply to this topic.
    Explain regulatory implications and requirements."""
    
    prompt = f"Analyze regulatory aspects of: '{query}'\nPrevious analysis: {history}"
    summary = get_gpt_response(prompt, system_message)
    
    return summary, meta

def simulate_compliance_expert(query: str, history: List[str]) -> Tuple[str, PersonaMetadata]:
    meta = PersonaMetadata(
        persona_type="Compliance Expert",
        name="Mrs. Compliance Officer",
        job_roles=["Compliance Manager"], 
        skills=["Standard Enforcement"], 
        certifications=["Compliance Auditor"],
        training=["Compliance Training"], 
        education=["MSc Compliance"], 
        research_base=["Compliance Papers"]
    )
    
    system_message = """You are Mrs. Compliance Officer, a compliance expert.
    Ensure all recommendations align with standards, best practices, and compliance requirements.
    Provide final guidance on implementation that meets all regulatory and industry standards."""
    
    prompt = f"Provide compliance review for: '{query}'\nPrevious analysis: {history}"
    summary = get_gpt_response(prompt, system_message)
    
    return summary, meta

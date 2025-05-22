from .schema.data_models import PersonaProfile, ReasoningStep
from typing import Tuple, List, Dict, Optional
import os
from openai import AzureOpenAI
from datetime import datetime
import uuid
import random
import json # For parsing the planner's output
from ..models import Provision # Adjusted import for Provision

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2025-03-01-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def get_gpt_response(prompt: str, system_message: str) -> str:
    """Get a response from Azure OpenAI GPT-4.1"""
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2048,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content.strip() if response.choices and response.choices[0].message else "No response from API."
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return f"Error: Could not get response from LLM. Details: {str(e)}"

def simulate_knowledge_expert(query: str, history: List[str], profile: PersonaProfile) -> ReasoningStep:
    """Simulate a Knowledge Expert analyzing the query, using a provided PersonaProfile."""
    start_time = datetime.utcnow()

    system_message = f"""You are {profile.name}, a {profile.persona_archetype} and {profile.job_title_exemplar}.
    Your expertise lies in {', '.join(profile.domain_expertise)}.
    Your key responsibilities include: {', '.join(profile.key_responsibilities_or_tasks)}.
    Your behavioral traits are: {', '.join(profile.behavioral_traits)}.
    Analyze the query from first principles and theoretical foundations.
    Previous analysis steps for context (if any):
    {''.join(history)}
    Focus on identifying key concepts, core principles, and theoretical underpinnings related to the query: '{query}'"""

    response_text = get_gpt_response(query, system_message)

    end_time = datetime.utcnow()
    step_id = f"ks_{uuid.uuid4()}"

    # Use the passed-in profile information
    return ReasoningStep(
        step_id=step_id,
        description=f"{profile.name} ({profile.persona_archetype}) providing foundational knowledge analysis.",
        model_used="gpt-4.1",
        persona_profile_id=profile.profile_id,
        persona_display_name=profile.name,
        input_context={"query": query, "history": history, "persona_config": profile.model_dump(exclude_none=True)},
        output_generated=response_text,
        confidence_score=random.uniform(0.7, 0.95), # Placeholder
        knowledge_references=profile.source_data_references, # Use from profile
        start_time=start_time,
        end_time=end_time,
        issues_identified=[], # Placeholder
        associated_axes=profile.ukg_axes,
        status="completed"
    )

def simulate_sector_expert(query: str, history: List[str], profile: PersonaProfile) -> ReasoningStep:
    """Simulate a Sector Expert analyzing the query, using a provided PersonaProfile."""
    start_time = datetime.utcnow()
    
    system_message = f"""You are {profile.name}, a {profile.persona_archetype} and {profile.job_title_exemplar}.
    Your expertise lies in {', '.join(profile.domain_expertise)} within industry sectors like {', '.join(profile.industry_sectors if profile.industry_sectors else ['various'])}.
    Your key responsibilities include: {', '.join(profile.key_responsibilities_or_tasks)}.
    Your behavioral traits are: {', '.join(profile.behavioral_traits)}.
    Analyze the query considering its practical application in relevant industry sectors.
    Previous analysis steps for context:
    {''.join(history)}
    Focus on real-world implications, industry best practices, and sector-specific challenges for the query: '{query}'"""

    response_text = get_gpt_response(query, system_message)

    end_time = datetime.utcnow()
    step_id = f"se_{uuid.uuid4()}"

    return ReasoningStep(
        step_id=step_id,
        description=f"{profile.name} ({profile.persona_archetype}) providing sector-specific application analysis.",
        model_used="gpt-4.1",
        persona_profile_id=profile.profile_id,
        persona_display_name=profile.name,
        input_context={"query": query, "history": history, "persona_config": profile.model_dump(exclude_none=True)},
        output_generated=response_text,
        confidence_score=random.uniform(0.65, 0.9), # Placeholder
        knowledge_references=profile.source_data_references,
        start_time=start_time,
        end_time=end_time,
        issues_identified=[],
        associated_axes=profile.ukg_axes,
        status="completed"
    )

def simulate_regulatory_expert(query: str, history: List[str], profile: PersonaProfile) -> ReasoningStep:
    """Simulate a Regulatory Expert analyzing the query, using a provided PersonaProfile."""
    start_time = datetime.utcnow()
    
    system_message = f"""You are {profile.name}, a {profile.persona_archetype} and {profile.job_title_exemplar}.
    Your expertise lies in {', '.join(profile.domain_expertise)} related to regulations and policies.
    Your key responsibilities include: {', '.join(profile.key_responsibilities_or_tasks)}.
    Your behavioral traits are: {', '.join(profile.behavioral_traits)}.
    Analyze the query from a regulatory and policy perspective.
    Previous analysis steps for context:
    {''.join(history)}
    Focus on applicable laws, regulations, standards, and potential policy implications for the query: '{query}'"""
    
    response_text = get_gpt_response(query, system_message)

    end_time = datetime.utcnow()
    step_id = f"re_{uuid.uuid4()}"

    return ReasoningStep(
        step_id=step_id,
        description=f"{profile.name} ({profile.persona_archetype}) providing regulatory and policy analysis.",
        model_used="gpt-4.1",
        persona_profile_id=profile.profile_id,
        persona_display_name=profile.name,
        input_context={"query": query, "history": history, "persona_config": profile.model_dump(exclude_none=True)},
        output_generated=response_text,
        confidence_score=random.uniform(0.7, 0.95),
        knowledge_references=profile.source_data_references,
        start_time=start_time,
        end_time=end_time,
        issues_identified=[],
        associated_axes=profile.ukg_axes,
        status="completed"
    )

def simulate_compliance_expert(query: str, history: List[str], profile: PersonaProfile) -> ReasoningStep:
    """Simulate a Compliance Expert analyzing the query, using a provided PersonaProfile."""
    start_time = datetime.utcnow()

    system_message = f"""You are {profile.name}, a {profile.persona_archetype} and {profile.job_title_exemplar}.
    Your expertise lies in {', '.join(profile.domain_expertise)} related to compliance and risk management.
    Your key responsibilities include: {', '.join(profile.key_responsibilities_or_tasks)}.
    Your behavioral traits are: {', '.join(profile.behavioral_traits)}.
    Analyze the query for compliance requirements, potential risks, and mitigation strategies.
    Previous analysis steps for context:
    {''.join(history)}
    Focus on identifying compliance obligations, risks, control gaps, and ensuring adherence to standards for the query: '{query}'"""

    response_text = get_gpt_response(query, system_message)

    end_time = datetime.utcnow()
    step_id = f"ce_{uuid.uuid4()}"

    return ReasoningStep(
        step_id=step_id,
        description=f"{profile.name} ({profile.persona_archetype}) providing compliance and risk analysis.",
        model_used="gpt-4.1",
        persona_profile_id=profile.profile_id,
        persona_display_name=profile.name,
        input_context={"query": query, "history": history, "persona_config": profile.model_dump(exclude_none=True)},
        output_generated=response_text,
        confidence_score=random.uniform(0.75, 0.98),
        knowledge_references=profile.source_data_references,
        start_time=start_time,
        end_time=end_time,
        issues_identified=[],
        associated_axes=profile.ukg_axes,
        status="completed"
    )

def simulate_planner_expert(query: str, profile: PersonaProfile, provision_context: Optional[Provision] = None) -> ReasoningStep:
    """Simulate a Planner Expert analyzing the query and generating a reasoning plan, optionally using specific provision context."""
    start_time = datetime.utcnow()

    provision_details_for_prompt_lines = []
    if provision_context:
        provision_details_for_prompt_lines.append(
            "\nYou are also provided with specific context for a regulatory provision. PRIORITIZE this provision in your analysis and planning:"
        )
        provision_details_for_prompt_lines.append(f"Provision ID: {provision_context.id}")
        provision_details_for_prompt_lines.append(f"Provision Title: \"{provision_context.title}\"")
        
        provision_text_excerpt = provision_context.text
        if len(provision_text_excerpt) > 1000:
            provision_text_excerpt = provision_text_excerpt[:1000] + "..."
        # Correctly escape for inclusion in a Python f-string that becomes an LLM prompt string.
        # The goal is to have literal """ markers in the string passed to the LLM.
        provision_details_for_prompt_lines.append("Provision Text: \"\"\"") # Start of text block marker
        provision_details_for_prompt_lines.append(provision_text_excerpt.replace('\\', '\\\\').replace('"', '\\"')) # Escape backslashes and quotes in the text itself
        provision_details_for_prompt_lines.append("\"\"\"") # End of text block marker

        if provision_context.section:
            provision_details_for_prompt_lines.append(f"Section: {provision_context.section}")
        if provision_context.tags:
            provision_details_for_prompt_lines.append(f"Tags: {', '.join(provision_context.tags)}")
        if provision_context.roles_responsible:
            provision_details_for_prompt_lines.append(f"Responsible Role IDs: {', '.join(provision_context.roles_responsible)}")
        provision_details_for_prompt_lines.append("") # Add a final newline for separation
    
    provision_details_for_prompt_str = "\n".join(provision_details_for_prompt_lines)

    # Doubled curly braces for literal JSON braces in f-string
    system_message = f"""You are {profile.name}, a {profile.persona_archetype} ({profile.job_title_exemplar}).
Your expertise: {', '.join(profile.domain_expertise)}.
Your key responsibilities: {', '.join(profile.key_responsibilities_or_tasks)}.
Your goal is to analyze the user's query and create a strategic reasoning plan.

The user's query is: "{query}"
{provision_details_for_prompt_str}
Based on this query {'AND the detailed provision context provided above, ' if provision_context else ''}determine the optimal sequence of the following expert persona archetypes to involve: 
KnowledgeExpert, SectorExpert, RegulatoryExpert, ComplianceExpert.
You may choose to use all, some, or none, and in any order you deem best.
For each chosen persona, briefly specify a 'focus' or sub-task for them related to the main query (and the specific provision if provided).

Output your plan STRICTLY as a JSON object with the following structure:
{{  // Doubled braces
  "reasoning_sequence": [
    {{ "archetype": "<Archetype_Name>", "focus": "<Specific focus or sub-task for this archetype based on the query (and provision if specified)>" }},
    // ... more steps if needed ...
  ],
  "overall_strategy_rationale": "<Brief rationale for your chosen sequence and focus areas, considering the provision if provided.>"
}}

Example for a query about 'new drone regulations for agriculture' (without specific provision context):
{{ // Doubled braces
  "reasoning_sequence": [
    {{ "archetype": "KnowledgeExpert", "focus": "Define key terms: drone, agriculture, current regulatory landscape overview." }},
    {{ "archetype": "RegulatoryExpert", "focus": "Detail the new drone regulations specifically for agriculture, citing relevant sections." }},
    {{ "archetype": "SectorExpert", "focus": "Analyze the practical impact of these new regulations on agricultural operations and drone usage." }},
    {{ "archetype": "ComplianceExpert", "focus": "Outline compliance steps and potential challenges for agricultural businesses regarding these new drone regulations." }}
  ],
  "overall_strategy_rationale": "Sequential approach: define terms, detail regulations, analyze impact, then outline compliance."
}}
If specific provision context IS provided, your plan and rationale MUST heavily focus on that provision. For instance, if the query is "Impact analysis" and a specific provision about data storage is given, the plan should be about analyzing the impact of THAT data storage provision.
Ensure the output is ONLY the JSON object, with no other text before or after.
"""

    llm_user_prompt = query 
    if provision_context:
        llm_user_prompt = f"{query}\n(Context: Provision '{provision_context.title}')"

    response_text = get_gpt_response(llm_user_prompt, system_message)

    end_time = datetime.utcnow()
    step_id = f"planner_{uuid.uuid4()}"

    parsed_plan = None
    parsing_error = None
    try:
        parsed_plan = json.loads(response_text)
        if not isinstance(parsed_plan, dict) or "reasoning_sequence" not in parsed_plan or not isinstance(parsed_plan["reasoning_sequence"], list):
            raise ValueError("Parsed JSON does not match expected plan structure.")
    except json.JSONDecodeError as e:
        parsing_error = f"Failed to parse planner output as JSON: {e}. Raw output: {response_text}"
        print(parsing_error)
    except ValueError as e:
        parsing_error = f"Planner output JSON structure invalid: {e}. Raw output: {response_text}"
        print(parsing_error)

    input_ctx = {"query": query, "persona_config": profile.model_dump(exclude_none=True)}
    if provision_context:
        input_ctx["provision_context"] = provision_context.model_dump(exclude_none=True)

    return ReasoningStep(
        step_id=step_id,
        description=f"{profile.name} ({profile.persona_archetype}) generating a strategic reasoning plan {('for provision ' + provision_context.id) if provision_context else ''}.",
        model_used="gpt-4.1", 
        persona_profile_id=profile.profile_id,
        persona_display_name=profile.name,
        input_context=input_ctx,
        output_generated=response_text, 
        confidence_score=random.uniform(0.8, 0.98) if parsed_plan and not parsing_error else 0.3,
        knowledge_references=profile.source_data_references,
        start_time=start_time,
        end_time=end_time,
        issues_identified=[parsing_error] if parsing_error else [],
        associated_axes=profile.ukg_axes,
        status="completed" if parsed_plan and not parsing_error else "error_parsing_plan",
        custom_step_data={"parsed_plan": parsed_plan} if parsed_plan else {"parsing_error_detail": parsing_error}
    )

# --- New Synthesizer Expert Simulation ---
def simulate_synthesizer_expert(original_query: str, history: List[str], profile: PersonaProfile) -> ReasoningStep:
    """Simulate a Synthesizer Expert consolidating all prior steps into a final answer."""
    start_time = datetime.utcnow()

    # Construct the full context for the synthesizer
    full_context = f"Original User Query: \"{original_query}\"\n\n"
    full_context += "Reasoning History (Planner + Experts):\n"
    full_context += "========================================\n"
    full_context += '\n---\n'.join(history)
    full_context += "\n========================================\n"

    # Calculate number of expert steps (assuming history[0] is the planner step if it succeeded)
    num_expert_steps = len(history) -1 if history else 0 
    
    system_message = f"""You are {profile.name}, a {profile.persona_archetype} ({profile.job_title_exemplar}).
    Your expertise: {', '.join(profile.domain_expertise)}.
    Your goal is to synthesize the information provided in the Reasoning History to generate a final, comprehensive, and coherent response that directly addresses the Original User Query.

    Review the entire history, including the planner's rationale and the outputs from the subsequent {num_expert_steps} expert steps. Identify key findings, consensus points, and any remaining conflicts or uncertainties noted by the experts.

    Generate a final summary response. Start by directly addressing the user's original query. Then, integrate the key insights from the expert steps in a logical flow. Do NOT simply list the expert outputs; synthesize them. If significant uncertainties or conflicting expert views remain, briefly mention them.
    Focus on clarity, conciseness, and directly answering the original request.
    """

    # The prompt is the full context constructed above
    response_text = get_gpt_response(full_context, system_message)

    end_time = datetime.utcnow()
    step_id = f"synth_{uuid.uuid4()}"

    return ReasoningStep(
        step_id=step_id,
        description=f"{profile.name} ({profile.persona_archetype}) synthesizing final response.",
        model_used="gpt-4.1", # Or configured model
        persona_profile_id=profile.profile_id,
        persona_display_name=profile.name,
        input_context={"original_query": original_query, "full_history": history, "persona_config": profile.model_dump(exclude_none=True)},
        output_generated=response_text,
        confidence_score=random.uniform(0.85, 0.99), # Synthesizer should aim for high confidence in its summary
        knowledge_references=profile.source_data_references,
        start_time=start_time,
        end_time=end_time,
        issues_identified=[], # Issues should ideally be resolved or noted in the summary
        associated_axes=profile.ukg_axes,
        status="completed"
    )

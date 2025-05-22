from fastapi import FastAPI, HTTPException
from typing import List, Dict
import uuid
from datetime import datetime

from .persona_functions import (
    simulate_knowledge_expert,
    simulate_sector_expert,
    simulate_regulatory_expert,
    simulate_compliance_expert
)
# Import the new response models
from quad_persona.schema.data_models import ReasoningStep, ReasoningTrace, PersonaProfile
from .ukg_interface import get_dynamic_persona_profile # Changed to relative import

app = FastAPI(title="Quad Persona Engine - Reasoning Service")

@app.post("/reason/quad", response_model=ReasoningTrace, summary="Run Quad Persona Reasoning")
def run_quad_persona_reasoning(request: Dict[str, str]) -> ReasoningTrace:
    """
    Accepts a query and runs it sequentially through four expert personas, dynamically instantiated.
    Returns a detailed ReasoningTrace object containing the steps taken by each persona.
    """
    query = request.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    task_id = f"task_{uuid.uuid4()}"
    request_timestamp = datetime.utcnow()
    all_steps: List[ReasoningStep] = []
    history: List[str] = []
    overall_confidence_scores: List[float] = []

    # Define persona archetypes in order of execution
    persona_archetypes_order = [
        "KnowledgeExpert", 
        "SectorExpert", 
        "RegulatoryExpert", 
        "ComplianceExpert"
    ]
    
    simulation_functions = {
        "KnowledgeExpert": simulate_knowledge_expert,
        "SectorExpert": simulate_sector_expert,
        "RegulatoryExpert": simulate_regulatory_expert,
        "ComplianceExpert": simulate_compliance_expert
    }

    for archetype in persona_archetypes_order:
        print(f"Processing {archetype}...")
        # 1. Get dynamic persona profile
        try:
            current_profile: PersonaProfile = get_dynamic_persona_profile(query, archetype)
        except Exception as e:
            # Handle cases where profile fetching might fail
            error_step = ReasoningStep(
                step_id=f"error_profile_{archetype.lower()}_{uuid.uuid4()}",
                description=f"Failed to instantiate persona profile for {archetype}. Error: {str(e)}",
                persona_display_name=f"Error Fetching {archetype}",
                status="error",
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow(),
                # Populate other required fields with defaults or N/A
                model_used="N/A",
                persona_profile_id="N/A",
                input_context={"query": query, "archetype": archetype},
                output_generated=f"Error: {str(e)}",
                associated_axes=[],
                issues_identified=[f"Profile instantiation failed for {archetype}"]
            )
            all_steps.append(error_step)
            # Potentially stop processing or continue with a default/dummy profile
            # For now, we'll append error and continue, which means subsequent steps might be affected
            history.append(f"Error Step for {archetype}: Profile instantiation failed. {str(e)}")
            continue # Skip to next archetype if profile fetching failed

        # 2. Run simulation with the dynamic profile
        simulate_func = simulation_functions[archetype]
        step_result = simulate_func(query=query, history=history, profile=current_profile)
        all_steps.append(step_result)

        if step_result.output_generated:
            history.append(f"Summary from {step_result.persona_display_name} ({step_result.persona_profile_id}):\n{step_result.output_generated}\nConfidence: {step_result.confidence_score}\n")
        if step_result.confidence_score is not None:
            overall_confidence_scores.append(step_result.confidence_score)

    final_summary = "Sequential reasoning complete. Review individual steps for details."
    if history:
        final_summary = history[-1] # Take the last expert's summary as the overall for now
    
    avg_confidence = sum(overall_confidence_scores) / len(overall_confidence_scores) if overall_confidence_scores else 0.0

    return ReasoningTrace(
        task_id=task_id,
        request_timestamp=request_timestamp.isoformat(),
        original_query=query,
        steps=all_steps,
        final_response_summary=final_summary,
        overall_confidence_score=avg_confidence,
        reasoning_model_used="Sequential Quad Persona with Dynamic Instantiation",
        audit_trail_notes=["Quad persona reasoning executed sequentially with dynamically fetched profiles."]
    )
    
    
    
    

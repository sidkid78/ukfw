import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
import uuid
from datetime import datetime
import os
import json

# Import the KGM instance from api.py
from .api import kgm 
from .models import Provision # Import Provision model

# Imports for Quad Persona Reasoning
from .quad_persona.persona_functions import (
    simulate_knowledge_expert,
    simulate_sector_expert,
    simulate_regulatory_expert,
    simulate_compliance_expert,
    simulate_planner_expert,
    simulate_synthesizer_expert
)
from .quad_persona.schema.data_models import ReasoningStep, ReasoningTrace, PersonaProfile
from .quad_persona.ukg_interface import (
    get_dynamic_persona_profile,
    get_planner_persona_profile,
    get_synthesizer_persona_profile
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure conversation logging
os.makedirs("logs/conversations", exist_ok=True)
conversation_logger = logging.getLogger("conversation_logger")
conversation_logger.setLevel(logging.INFO)
conversation_file_handler = logging.FileHandler("logs/conversations/reasoning_conversations.log")
conversation_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
conversation_logger.addHandler(conversation_file_handler)

app = FastAPI(
    title="Universal Knowledge Framework (UKFW) API",
    description="API for managing and querying the 13-Axis Knowledge Graph.",
    version="0.1.0",
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the UKFW API"}

# Import the main API router AFTER kgm is potentially used by it or other app setup
# Ensure api.router does not cause circular dependencies if it also imports from main
# For now, assuming this order is fine or that kgm is self-contained enough in api.py
from .api import router as api_router # aliased to avoid conflict if router name is reused
app.include_router(api_router)

@app.post(
    "/reason/quad",
    response_model=ReasoningTrace,
    summary="Run Quad Persona Reasoning with Planner and Synthesizer"
)
def run_quad_persona_reasoning(request: Dict[str, str]) -> ReasoningTrace:
    query = request.get("query")
    provision_id = request.get("provision_id") # Get provision_id
    provision_object: Optional[Provision] = None

    if not query:
        logger.error("Received empty query.")
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    task_id = f"task_{uuid.uuid4()}"
    request_timestamp = datetime.utcnow()
    all_steps: List[ReasoningStep] = []
    history: List[str] = []
    overall_confidence_scores: List[float] = []
    errors_encountered: List[str] = []
    planner_rationale = "Planner did not run or failed critically."
    planned_sequence = []
    final_synth_summary = "Synthesis step did not run or failed."

    logger.info(f"Starting Quad Persona Reasoning for task_id: {task_id}")
    conversation_logger.info(f"TASK_START: {task_id} - Query: {query}{f' - Provision ID: {provision_id}' if provision_id else ''}")

    # Fetch provision if ID is provided
    if provision_id:
        logger.info(f"Provision ID '{provision_id}' provided, attempting to fetch from KGM.")
        try:
            provision_object = kgm.get_provision_by_id(provision_id)
            if provision_object:
                logger.info(f"Successfully fetched provision '{provision_id}': {provision_object.title}")
            else:
                logger.warning(f"Provision ID '{provision_id}' not found in KGM. Proceeding without specific provision context.")
        except Exception as e:
            logger.error(f"Error fetching provision '{provision_id}' from KGM: {e}", exc_info=True)
            errors_encountered.append(f"Error fetching provision {provision_id}: {str(e)}. Proceeding without it.")
            # Non-critical, planner will proceed with query only

    # Planner Step
    logger.info("Executing PlannerExpert...")
    try:
        planner_profile = get_planner_persona_profile()
        # Pass provision_object to simulate_planner_expert
        planner_step = simulate_planner_expert(query=query, profile=planner_profile, provision_context=provision_object)
        all_steps.append(planner_step)

        conversation_logger.info(f"PLANNER_INPUT: {task_id} - Query: {query}{f' - Provision ID: {provision_id}' if provision_id else ''}")
        conversation_logger.info(f"PLANNER_OUTPUT: {task_id} - {planner_step.output_generated}")

        if (
            planner_step.status != "completed"
            or not planner_step.custom_step_data
            or "parsed_plan" not in planner_step.custom_step_data
        ):
            error_msg = f"Planner step failed or produced invalid plan. Status: {planner_step.status}. Issues: {planner_step.issues_identified}"
            logger.error(error_msg)
            errors_encountered.append(error_msg)
            planner_rationale = "Planner failed to generate a valid plan."
            conversation_logger.error(f"PLANNER_ERROR: {task_id} - {error_msg}")
        else:
            parsed_plan = planner_step.custom_step_data["parsed_plan"]
            planned_sequence = parsed_plan.get("reasoning_sequence", [])
            planner_rationale = parsed_plan.get("overall_strategy_rationale", "No rationale provided by planner.")
            history.append(f"Planner ({planner_profile.name}) Rationale: {planner_rationale}\nOutput:\n{planner_step.output_generated}\n")
            if planner_step.confidence_score is not None:
                overall_confidence_scores.append(planner_step.confidence_score)
            conversation_logger.info(f"PLANNER_RATIONALE: {task_id} - {planner_rationale}")

    except Exception as e:
        error_msg = f"Exception during PlannerExpert execution: {str(e)}"
        logger.exception(error_msg)
        errors_encountered.append(error_msg)
        planner_step_input_context = {"query": query}
        if provision_id:
            planner_step_input_context["provision_id"] = provision_id # Add provision_id if available
        
        planner_step = ReasoningStep(
            step_id=f"error_planner_{uuid.uuid4()}",
            description=error_msg,
            persona_display_name="Planner System Error",
            status="error",
            start_time=datetime.utcnow(),
            end_time=datetime.utcnow(),
            model_used="N/A",
            persona_profile_id="N/A",
            input_context=planner_step_input_context, # Updated context
            output_generated=error_msg,
            associated_axes=[],
            issues_identified=[error_msg]
        )
        all_steps.append(planner_step)
        planner_rationale = "Planner critically failed."
        conversation_logger.error(f"PLANNER_EXCEPTION: {task_id} - {error_msg}")

    expert_simulation_functions = {
        "KnowledgeExpert": simulate_knowledge_expert,
        "SectorExpert": simulate_sector_expert,
        "RegulatoryExpert": simulate_regulatory_expert,
        "ComplianceExpert": simulate_compliance_expert
    }

    # Execute planned expert sequence
    for step_info in planned_sequence:
        archetype = step_info.get("archetype")
        focus = step_info.get("focus", "Address the overall query based on your expertise.")

        if archetype not in expert_simulation_functions:
            error_msg = f"Invalid archetype specified by planner: {archetype}. Skipping."
            logger.warning(error_msg)
            errors_encountered.append(error_msg)
            conversation_logger.warning(f"EXPERT_INVALID: {task_id} - {error_msg}")
            continue

        logger.info(f"Executing {archetype} with focus: {focus}")
        # The current_query for experts now includes planner_rationale which might be provision-aware
        current_query_for_expert = f"Original Query: {query}{f' (related to Provision ID: {provision_id})' if provision_id else ''}\nPlanner's Plan & Rationale (consider this primary instructions): {planner_rationale}\nYour Specific Focus: {focus}"
        conversation_logger.info(f"EXPERT_INPUT: {task_id} - Archetype: {archetype} - Query: {current_query_for_expert}")

        try:
            current_profile = get_dynamic_persona_profile(current_query_for_expert, archetype)
            simulate_func = expert_simulation_functions[archetype]
            expert_step = simulate_func(query=current_query_for_expert, history=history, profile=current_profile)
            all_steps.append(expert_step)

            conversation_logger.info(f"EXPERT_OUTPUT: {task_id} - Archetype: {archetype} - Output: {expert_step.output_generated}")

            if expert_step.output_generated:
                history.append(f"{expert_step.persona_display_name} ({expert_step.persona_profile_id}) Output:\n{expert_step.output_generated}\nConfidence: {expert_step.confidence_score}\n")
            if expert_step.confidence_score is not None:
                overall_confidence_scores.append(expert_step.confidence_score)

        except Exception as e:
            error_msg = f"Exception during {archetype} execution: {str(e)}"
            logger.exception(error_msg)
            errors_encountered.append(error_msg)
            error_step_input_context = {"query": current_query_for_expert, "archetype": archetype}
            if provision_id: # Add provision_id to error context if relevant
                 error_step_input_context["provision_id_context"] = provision_id

            error_step = ReasoningStep(
                step_id=f"error_{archetype.lower()}_{uuid.uuid4()}",
                description=error_msg,
                persona_display_name=f"{archetype} System Error",
                status="error",
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow(),
                model_used="N/A",
                persona_profile_id=current_profile.profile_id if 'current_profile' in locals() and hasattr(current_profile, 'profile_id') else "N/A",
                input_context=error_step_input_context,
                output_generated=error_msg,
                associated_axes=[],
                issues_identified=[error_msg]
            )
            all_steps.append(error_step)
            conversation_logger.error(f"EXPERT_EXCEPTION: {task_id} - Archetype: {archetype} - {error_msg}")

    # Synthesizer Step
    if planner_rationale != "Planner critically failed.":
        logger.info("Executing SynthesizerExpert...")
        synthesizer_input = f"Original Query: {query}{f' (related to Provision ID: {provision_id})' if provision_id else ''}\nExpert History (Planner + Experts):\n{''.join(history)}"
        conversation_logger.info(f"SYNTHESIZER_INPUT: {task_id} - {synthesizer_input}")
        
        try:
            synthesizer_profile = get_synthesizer_persona_profile()
            synthesizer_step = simulate_synthesizer_expert(original_query=query, history=history, profile=synthesizer_profile)
            all_steps.append(synthesizer_step)

            conversation_logger.info(f"SYNTHESIZER_OUTPUT: {task_id} - {synthesizer_step.output_generated}")

            if synthesizer_step.status == "completed" and synthesizer_step.output_generated:
                final_synth_summary = synthesizer_step.output_generated
            else:
                error_msg = f"Synthesizer step failed or produced no output. Status: {synthesizer_step.status}"
                logger.error(error_msg)
                errors_encountered.append(error_msg)
                conversation_logger.error(f"SYNTHESIZER_ERROR: {task_id} - {error_msg}")

            if synthesizer_step.confidence_score is not None:
                overall_confidence_scores.append(synthesizer_step.confidence_score)

        except Exception as e:
            error_msg = f"Exception during SynthesizerExpert execution: {str(e)}"
            logger.exception(error_msg)
            errors_encountered.append(error_msg)
            conversation_logger.error(f"SYNTHESIZER_EXCEPTION: {task_id} - {error_msg}")

    avg_confidence = sum(overall_confidence_scores) / len(overall_confidence_scores) if overall_confidence_scores else 0.0

    logger.info(f"Completed Quad Persona Reasoning for task_id: {task_id} with confidence: {avg_confidence}")
    
    # Log the final result
    conversation_logger.info(f"TASK_COMPLETE: {task_id} - Final Summary: {final_synth_summary}")
    conversation_logger.info(f"TASK_METRICS: {task_id} - Confidence: {avg_confidence}, Steps: {len(all_steps)}, Errors: {len(errors_encountered)}")
    
    # Save the complete reasoning trace to a JSON file for reference
    try:
        original_query_context = {"query": query}
        if provision_id:
            original_query_context["provision_id"] = provision_id
            if provision_object: # Also add title if provision was fetched
                original_query_context["provision_title"] = provision_object.title

        trace_result = ReasoningTrace(
            task_id=task_id,
            request_timestamp=request_timestamp,
            original_query=original_query_context, # Store query and provision_id if present
            steps=all_steps,
            final_response_summary=final_synth_summary,
            overall_confidence_score=avg_confidence,
            personas_involved_ids=list(set(s.persona_profile_id for s in all_steps if s.persona_profile_id)),
            reasoning_models_used=list(set(s.model_used for s in all_steps if s.model_used)),
            ukg_axes_queried=list(set(axis for s in all_steps for axis in s.associated_axes)),
            audit_trail_notes=[
                f"Planner Rationale: {planner_rationale}",
                f"Executed {len(planned_sequence)} expert steps.",
                "Synthesis step performed."
            ] + ([f"Errors encountered: {len(errors_encountered)}."] if errors_encountered else []),
            errors_encountered=errors_encountered,
            total_refinement_iterations=0
        )
        
        # Ensure logs directory exists
        logs_dir = "logs/conversations"
        os.makedirs(logs_dir, exist_ok=True)

        with open(os.path.join(logs_dir, f"{task_id}_trace.json"), "w") as f:
            f.write(trace_result.model_dump_json(indent=2))
            logger.info(f"Successfully saved trace to logs/conversations/{task_id}_trace.json")

    except Exception as e:
        logger.error(f"Failed to save trace to JSON or construct ReasoningTrace: {e}", exc_info=True)
        # Even if saving fails, try to return the trace object if it was constructed
        if 'trace_result' in locals():
            return trace_result
        # If trace_result construction failed, we might need to return a basic error response
        # or re-raise, but for now, let FastAPI handle it if trace_result is available.

    return trace_result

@app.get("/test-kgm")
async def test_kgm():
    return {"message": "This is a test endpoint for the Knowledge Graph Manager"}

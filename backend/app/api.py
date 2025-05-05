from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
# Use new specific models
from .models import Regulation, Provision, Role, Expert # Import new models
from .kg_manager import KnowledgeGraphManager
# Compliance and simulation logic might need updates if they relied on old models
from .compliance import filter_for_compliance 
from .simulation.simulation_manager import simulate_full_expert_reasoning 

router = APIRouter()
# Initialize manager with all data paths
kgm = KnowledgeGraphManager(
    regulations_path="app/data/pillars.yaml", # Use original pillars file for regulations
    provisions_path="app/data/nodes.yaml",   # Use original nodes file for provisions etc.
    roles_path="app/data/roles.yaml", # Add path to roles.yaml
    experts_path="app/data/experts.yaml", # Add path to experts.yaml
    # mappings_path="app/data/mappings.yaml" # We can ignore mappings for now
)

# --- Refactored Endpoints --- 

# Endpoint for Regulations (replaces /pillars)
@router.get("/regulations", response_model=List[Regulation])
def get_all_regulations():
    """Returns a list of all available regulations."""
    return kgm.get_all_regulations()

@router.get("/regulations/{regulation_id}", response_model=Regulation)
def get_regulation(regulation_id: str):
    """Gets details for a specific regulation."""
    regulation = kgm.get_regulation_by_id(regulation_id)
    if not regulation:
        raise HTTPException(status_code=404, detail="Regulation not found")
    return regulation

# Endpoint for Provisions (replaces /nodes)
@router.get("/provisions", response_model=List[Provision])
def query_provisions_endpoint(
    regulation_id: Optional[str] = None,
    jurisdiction: Optional[str] = None,
    tag: Optional[str] = None,
    role_id: Optional[str] = None,
    min_confidence: Optional[float] = Query(None, ge=0.0, le=1.0),
    compliance_tag: Optional[str] = Query(None)
):
    """Queries provisions based on various criteria including confidence and compliance tags."""
    provisions = kgm.query_provisions(
        regulation_id=regulation_id, 
        jurisdiction=jurisdiction, 
        tag=tag, 
        role_id=role_id,
        min_confidence=min_confidence,
        compliance_tag=compliance_tag
    )
    # TODO: Re-implement simulation logic if needed for provisions
    # TODO: Re-implement compliance filtering if needed (filter_for_compliance might need update)
    return provisions

@router.get("/provisions/{provision_id}", response_model=Provision)
def get_provision(provision_id: str):
    """Gets details for a specific provision."""
    provision = kgm.get_provision_by_id(provision_id)
    if not provision:
        raise HTTPException(status_code=404, detail="Provision not found")
    # TODO: Add compliance filtering back if required for single provision view
    return provision

# --- Endpoints for Roles and Experts (Implement Logic) ---
@router.get("/roles/{role_id}", response_model=Role)
def get_role(role_id: str):
    """Gets details for a specific role."""
    role = kgm.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    # Linking is now done during initialization by _link_entities
    return role

@router.get("/experts/{expert_id}", response_model=Expert)
def get_expert(expert_id: str):
    """Gets details for a specific expert."""
    expert = kgm.get_expert_by_id(expert_id)
    if not expert:
        raise HTTPException(status_code=404, detail="Expert not found")
    # Expert.provisions are loaded directly if present in experts.yaml, 
    # or could be linked similarly if needed in the future.
    return expert

# --- Simulation Endpoint (Needs Verification) ---
# This endpoint might need modification if simulation operates on Provisions now
@router.post("/simulate/provision/{provision_id}") # Changed path slightly for clarity
def simulate_expert_reasoning_endpoint(provision_id: str, confidence_goal: float = 0.995):
    """Runs expert reasoning simulation on a specific provision."""
    provision = kgm.get_provision_by_id(provision_id)
    if not provision:
        raise HTTPException(status_code=404, detail="Provision not found")
    # !! IMPORTANT: Verify simulate_full_expert_reasoning works with Provision model
    # It might expect the old KnowledgeNode structure. Adapt simulation logic if necessary.
    updated_provision, history = simulate_full_expert_reasoning(provision, kgm, confidence_goal=confidence_goal)
    # Return provision with updated confidence, metadata, and audit trail
    return updated_provision # Assuming the function returns the updated object

# --- Deprecated Endpoints (Remove or Keep with Warnings) ---

# @router.get("/pillars/{pillar_id}", response_model=Pillar)
# def get_pillar(pillar_id: str):
#     # ... (keep old implementation or raise error)

# @router.get("/pillars", response_model=List[Pillar])
# def get_all_pillars():
#     # ...

# @router.get("/nodes/{node_id}", response_model=KnowledgeNode)
# def get_node(node_id: str, compliance: Optional[str] = Query(None)):
#     # ...

# @router.get("/nodes", response_model=List[KnowledgeNode])
# def query_nodes(...):
#     # ...

# Note: Removed compliance logic from get_node/query_nodes for now.
# It needs to be re-evaluated based on how compliance applies to Provisions.
# Also removed simulation logic from query_nodes - needs review.

from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from .models import KnowledgeNode, Pillar
from .kg_manager import KnowledgeGraphManager
from .compliance import filter_for_compliance
from .simulation import simulate_expert_refinement
from .simulation.simulation_manager import simulate_full_expert_reasoning

router = APIRouter()
# Update these paths as needed for your data location
kgm = KnowledgeGraphManager("backend/app/data/pillars.yaml", "backend/app/data/nodes.yaml")

@router.get("/nodes/{node_id}", response_model=KnowledgeNode)
def get_node(node_id: str, compliance: Optional[str] = Query(None)):
    node = kgm.get_node_by_id(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    if compliance:
        permitted = filter_for_compliance([node], [compliance])
        if not permitted:
            raise HTTPException(status_code=403, detail="Restricted by compliance")
    return node

@router.get("/pillars/{pillar_id}", response_model=Pillar)
def get_pillar(pillar_id: str):
    pillar = kgm.get_pillar_by_id(pillar_id)
    if not pillar:
        raise HTTPException(status_code=404, detail="Pillar not found")
    return pillar

@router.get("/nodes", response_model=List[KnowledgeNode])
def query_nodes(
    axis1: Optional[str] = None,
    axis2: Optional[str] = None,
    axis8: Optional[str] = None,    # compliance tag
    min_confidence: Optional[float] = None,
    simulation_role: Optional[str] = None
):
    axis_filters = {k: v for k, v in {"axis1": axis1, "axis2": axis2, "axis8": axis8}.items() if v is not None}
    nodes = kgm.query_nodes(**axis_filters)
    if min_confidence is not None:
        nodes = [n for n in nodes if n.axes.axis9 and n.axes.axis9 >= min_confidence]
    if simulation_role:
        nodes = [simulate_expert_refinement(n, simulation_role) for n in nodes]
    if axis8:
        nodes = filter_for_compliance(nodes, [axis8])
    return nodes

@router.post("/simulate/{node_id}")
def simulate_expert_reasoning(node_id: str, confidence_goal: float = 0.995):
    node = kgm.get_node_by_id(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    node = simulate_full_expert_reasoning(node, kgm, confidence_goal=confidence_goal)
    # Return node with updated confidence, metadata, and audit trail
    return node

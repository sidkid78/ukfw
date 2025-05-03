import yaml
from backend.app.models import KnowledgeNode
from backend.app.kg_manager import KnowledgeGraphManager
from backend.app.simulation.simulation_manager import simulate_full_expert_reasoning

def test_simulate_expert_reasoning():
    kgm = KnowledgeGraphManager("backend/app/data/pillars.yaml", "backend/app/data/nodes.yaml")
    node = kgm.get_node_by_id("USID:PL16:0001")
    assert node is not None
    original_conf = node.axes.axis9
    node = simulate_full_expert_reasoning(node, kgm, confidence_goal=0.995)
    # Should update confidence and add refinement history
    assert node.axes.axis9 <= original_conf
    assert hasattr(node, 'metadata')
    assert 'refinement_history' in node.metadata
    assert isinstance(node.metadata['refinement_history'], list)

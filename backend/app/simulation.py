from .models import KnowledgeNode
from typing import Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def simulate_expert_refinement(node: KnowledgeNode, persona: str) -> KnowledgeNode:
    """
    Simulate an expert review process for a KnowledgeNode.
    - If persona matches any value in node.axes.axis12 (None or list), increment axis9 by 0.01 (max 1.0).
    - Log the refinement in node.metadata['expert_refined'].
    - If no match, node is unchanged.
    - Handles missing axis9/axis12 robustly.
    Example:
        node = simulate_expert_refinement(node, "Theoretical Physicist")
        # If persona matches, node.axes.axis9 += 0.01 (max 1.0),
        # and node.metadata['expert_refined'] is updated.
    """
    axis12 = getattr(node.axes, 'axis12', None)
    personas = axis12 if isinstance(axis12, list) else [axis12] if axis12 else []
    if persona in personas:
        current_conf = getattr(node.axes, 'axis9', 0.0) or 0.0
        new_conf = min(1.0, current_conf + 0.01)
        node.axes.axis9 = new_conf
        if not hasattr(node, 'metadata') or node.metadata is None:
            node.metadata = {}
        entry = {
            'persona': persona,
            'action': 'refined',
            'result': new_conf,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        node.metadata.setdefault('expert_refined', []).append(entry)
        logger.info(f"Expert refinement: persona={persona}, old_conf={current_conf}, new_conf={new_conf}, node_id={getattr(node, 'node_id', None)}")
    return node

# Example usage:
# node = simulate_expert_refinement(node, "Theoretical Physicist")
# After refinement, if persona matches, node.axes.axis9 is incremented and metadata updated.

# Enhancement suggestion:
# For even richer feedback, add a 'quality_score', reviewer notes, or integrate with a feedback/metrics system.

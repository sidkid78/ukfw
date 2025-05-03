from .tree_of_thought import tree_of_thought_refinement
from .validation import autonomous_layer3_agent

def simulate_full_expert_reasoning(node, context, confidence_goal=0.995):
    # Step 1: ToT/AoT recursive refinement
    node, history = tree_of_thought_refinement(node, context, confidence_goal=confidence_goal)
    # Step 2: If still not confident, invoke Layer 3
    if (getattr(node.axes, 'axis9', 0.0) or 0.0) < confidence_goal:
        node = autonomous_layer3_agent(node, context)
    # Optionally repeat or escalate; for now, single pass
    return node

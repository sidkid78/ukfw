from .knowledge_algorithms import KNOWLEDGE_ALGORITHMS
from .expert_roles import EXPERT_ROLE_LIBRARY, get_roles_for_node

def tree_of_thought_refinement(node, context, history=None, depth=0, max_depth=3, confidence_goal=0.995):
    """
    Recursive reasoning (ToT/AoT) for nodes: applies expert algorithms, escalates as needed.
    Returns node with updated confidence & audit.
    """
    if history is None:
        history = []

    current_conf = getattr(node.axes, 'axis9', 0.0)
    history.append({
        "depth": depth,
        "node_id": getattr(node, 'node_id', None),
        "starting_confidence": current_conf,
        "actions": []
    })

    # Decide which roles ("experts") to apply at this layer
    roles = get_roles_for_node(node)
    for role in roles:
        expert_config = EXPERT_ROLE_LIBRARY.get(role, {})
        algos = expert_config.get("algorithms", [])
        for algo in algos:
            func = KNOWLEDGE_ALGORITHMS.get(algo)
            if func:
                result = func(node, context)
                history[-1]["actions"].append({
                    "role": role,
                    "algorithm": algo,
                    "result": result
                })
                current_conf = min(current_conf, result["validation"])
                node.axes.axis9 = current_conf

    # Check: do we need refinement (recursive step)?
    if current_conf < confidence_goal and depth < max_depth:
        node, history = tree_of_thought_refinement(
            node,
            context,
            history=history,
            depth=depth+1,
            max_depth=max_depth,
            confidence_goal=confidence_goal
        )

    if not hasattr(node, "metadata"):
        node.metadata = {}
    node.metadata.setdefault("refinement_history", []).extend(history)
    return node, history

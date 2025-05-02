from typing import List
from .models import KnowledgeNode

def filter_for_compliance(nodes: List[KnowledgeNode], user_compliance_tags: List[str]) -> List[KnowledgeNode]:
    """
    Only expose nodes that are not restricted or match compliance tags (axis8).
    If axis8 is None or empty, node is visible to all. If axis8 is set, at least one tag must match.
    """
    filtered = []
    for node in nodes:
        tags = node.axes.axis8
        if not tags:
            filtered.append(node)
        else:
            tag_list = tags if isinstance(tags, list) else [tags]
            if any(tag in user_compliance_tags for tag in tag_list):
                filtered.append(node)
    return filtered

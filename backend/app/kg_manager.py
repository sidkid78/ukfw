import yaml
from typing import List, Optional, Dict
from .models import KnowledgeNode, Pillar

class KnowledgeGraphManager:
    def __init__(self, pillars_path: str, nodes_path: str):
        self.pillars: Dict[str, Pillar] = {}
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.load_data(pillars_path, nodes_path)

    def load_data(self, pillars_path: str, nodes_path: str):
        with open(pillars_path, 'r') as f:
            data = yaml.safe_load(f)
            for p in data.get('pillars', []):
                pillar = Pillar(**p)
                self.pillars[pillar.pillar_id] = pillar
        with open(nodes_path, 'r') as f:
            data = yaml.safe_load(f)
            for n in data.get('nodes', []):
                node = KnowledgeNode(**n)
                self.nodes[node.node_id] = node

    def get_node_by_id(self, node_id: str) -> Optional[KnowledgeNode]:
        return self.nodes.get(node_id)

    def get_pillar_by_id(self, pillar_id: str) -> Optional[Pillar]:
        return self.pillars.get(pillar_id)

    def query_nodes(self, **axis_filters) -> List[KnowledgeNode]:
        matches = []
        for node in self.nodes.values():
            axis = node.axes.dict()
            if all(axis.get(ax) == val for ax, val in axis_filters.items() if val is not None):
                matches.append(node)
        return matches

    def query_confidence(self, min_confidence: float) -> List[KnowledgeNode]:
        return [n for n in self.nodes.values() if (n.axes.axis9 or 0) >= min_confidence]

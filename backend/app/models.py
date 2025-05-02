from typing import List, Dict, Union, Optional
from pydantic import BaseModel

class AxisCoordinate(BaseModel):
    axis1: str
    axis2: Optional[str] = None
    axis3: Optional[Union[str, int]] = None
    axis4: Optional[int] = None
    axis5: Optional[Union[str, int]] = None
    axis6: Optional[str] = None
    axis7: Optional[str] = None
    axis8: Optional[Union[str, List[str]]] = None
    axis9: Optional[float] = None
    axis10: Optional[str] = None
    axis11: str
    axis12: Optional[Union[str, List[str]]] = None
    axis13: Optional[Union[str, Dict]] = None

class KnowledgeNodeLink(BaseModel):
    target_node_id: str
    relationship_type: str
    weight: Optional[float] = 1.0
    axis_vector_diff: Optional[List[Union[int, float, str]]] = None
    metadata: Optional[Dict[str, Union[str, float, int, bool]]] = {}

class KnowledgeNode(BaseModel):
    node_id: str
    label: str
    description: str
    pillar_id: str
    axes: AxisCoordinate
    metadata: Dict[str, Union[str, float, int, dict, list]]
    simulation_roles: Optional[List[str]] = []
    links: Optional[List[KnowledgeNodeLink]] = []
    compliance_visible: Optional[bool] = True

class Pillar(BaseModel):
    pillar_id: str
    name: str
    description: str
    parent_pillar_id: Optional[str] = None
    metadata: Dict[str, Union[str, float, int, dict, list]]
    axes: AxisCoordinate

class KnowledgeGraph(BaseModel):
    pillars: List[Pillar]
    nodes: List[KnowledgeNode]

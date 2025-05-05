from typing import List, Dict, Union, Optional, Any
from pydantic import BaseModel, Field
from datetime import date, datetime
from enum import Enum

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

class NodeMetadata(BaseModel):
    provenance: Optional[str] = None
    audit_trail: Optional[List[Any]] = None
    confidence: Optional[float] = None
    compliance: Optional[List[str]] = None
    class Config:
        extra = 'allow'

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
    metadata: NodeMetadata = Field(default_factory=NodeMetadata)
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

class RegulatoryAxis(str, Enum):
    JURISDICTION = 'jurisdiction'
    PILLAR = 'pillar'
    PROVISION = 'provision'
    ROLE = 'role'
    EXPERT = 'expert'
    SPIDERWEB = 'spiderweb'
    HONEYCOMB = 'honeycomb'
    OCTOPUS = 'octopus'
    LOCATION = 'location'

class Regulation(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    jurisdiction: str
    pillar: str
    location_code: Optional[str] = None
    effective_date: Optional[date] = None
    provisions: List[str] = Field(default_factory=list)

class Provision(BaseModel):
    id: str
    regulation_id: str
    section: Optional[str] = None
    title: str
    text: str
    hierarchy_level: Optional[int] = None
    parent_id: Optional[str] = None
    jurisdiction: str
    roles_responsible: List[str] = Field(default_factory=list)
    crosswalks: List[str] = Field(default_factory=list)
    spiderweb_links: List[str] = Field(default_factory=list)
    octopus_refs: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    metadata: Optional[Dict] = None

class Role(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    jurisdiction: Optional[str] = None
    expertise_domains: List[str] = Field(default_factory=list)
    provisions: List[str] = Field(default_factory=list)

class Expert(BaseModel):
    id: str
    name: str
    role_id: str
    domains: List[str] = Field(default_factory=list)
    provisions: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    contact: Optional[str] = None

class SpiderwebNode(BaseModel):
    id: str
    source_provision: str
    target_provision: str
    relationship_type: str
    weight: float
    risk: Optional[float] = None
    note: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    axes_involved: List[RegulatoryAxis]

class HoneycombNode(BaseModel):
    id: str
    source_provision: str
    target_provision: str
    xwalk_type: str
    axes_involved: List[RegulatoryAxis]
    weight: Optional[float] = None
    note: Optional[str] = None

class OctopusNode(BaseModel):
    id: str
    domain: str
    regulatory_bodies: List[str]
    parent_nodes: Optional[List[str]] = None
    linked_provisions: List[str]
    experts: List[str]
    axes_involved: List[RegulatoryAxis]

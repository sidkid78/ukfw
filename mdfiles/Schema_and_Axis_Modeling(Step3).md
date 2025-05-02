# 

## **1. 13-Axis Multi-Dimensional Coordinate System**

### **1.1 Axis Reference Table**

| **Axis** | **Name** | **Description / Role** | **Typical Values / Encoding** | **System Notes** |
| --- | --- | --- | --- | --- |
| 1 | Pillar Domain (Core) | Major Pillar (PL01–PL87) – Ontological/disciplinary anchor | `PL_code` | Core pillar reference, e.g. PL16=Physics |
| 2 | Subdomain Typology | Key subdomain/track (library subclass, discipline subdivision, NAICS) | str or code | Extensible per pillar (e.g. Plasma Physics) |
| 3 | Branch Hierarchy | Tree branch context within pillar/subpillar (family, subfield, topic) | Path notation or integer | Maps node’s parent-child in structure |
| 4 | Hierarchical Depth (H) | Depth level in tree (root=0, +1 per child) | int | Used for pruning, scope rules |
| 5 | Temporal (T(x)) | Temporal frame/context (era, year, period, system version) | ISO8601 datetime, period code, int | Key for versioning, historical events, dynamic knowledge |
| 6 | Provenance / Source | Source, origin, or chain of evidence | URI, DOI, source_id | Used for traceability, validation, audit |
| 7 | Octopus Node System | Ecosystem assignment – cross-pillar/discipline “domain mesh/network” | int or str (ecosystem_id) | Important for sectoral/industry mapping, e.g. “Financial” |
| 8 | Compliance / Regulatory | Compliance domain: regulatory constraint/cert mapping | str or list (e.g. GDPR, HIPAA) | Used for API filtering, access control |
| 9 | Confidence / Validation | Confidence score, validation result, reviewed status | float (0–1), label | Drives recursive refinement/AI trust gating |
| 10 | Cultural/Linguistic Context | Cultural or linguistic background/context | str or enum | For inclusivity, translation, indigenous knowledge |
| 11 | Unified System Coordination | Unified ID, global locator (Nuremberg Number, SAM.gov, UUID) | str (UUID, USID, registry id) | System-wide unique mapping |
| 12 | Simulation / Expert Role | Contextual agent/expert role invoked | str, enum, list | For quad-persona, expert simulation (e.g. “Aerospace Engineer”) |
| 13 | Dynamic Metadata / Extension | Context-dependent tags, version, custom metainformation | dict / list / str | Used for future extensibility, temporary context, schemas |

---

## **2. YAML Schema Definitions**

### **2.1 Pillar Definition (`pillars.yaml`)**

```yaml
pillars:
  - pillar_id: PL16
    name: Physics & Astronomy
    description: Scientific study of matter, energy, space, and time.
    parent_pillar_id: null
    metadata:
      confidence: 1.0
      provenance: LibraryOfCongress:QC
      compliance_tags: [ ]
      cultural_context: Western
      version: 2024.1
    axes:
      axis1: PL16                        # Core Pillar
      axis2: Physics                     # Subdomain Typology
      axis3: "0"                         # Branch Hierarchy (root)
      axis4: 0                           # Hierarchical Depth
      axis5: Epoch:Modern                # Temporal
      axis6: "https://id.loc.gov/authorities/subjects/sh85101653" # Provenance
      axis7: Ecosystem:ScienceResearch   # Octopus
      axis8: None                        # Compliance
      axis9: 1.0                         # Confidence
      axis10: Western                    # Cultural/Linguistic Context
      axis11: USID:PL16                  # Unified System
      axis12: None                       # Expert Role
      axis13: { tags: ['root'], version: '2024.1' }

```

### **2.2 Knowledge Node Example (`nodes.yaml`)**

```yaml
nodes:
  - node_id: USID:PL16:0001
    label: "Foundations of Gravity"
    description: "Theories and models explaining gravitation, from Newtonian to contemporary theories."
    pillar_id: PL16
    axes:
      axis1: PL16
      axis2: Gravity
      axis3: "0.1"                      # This node is a child of root, first subtopic
      axis4: 1
      axis5: Year:1915                  # General Relativity
      axis6: "doi:10.1093/acprof:9780198504241.003.0002"
      axis7: Ecosystem:Physics
      axis8: None
      axis9: 0.98
      axis10: Western
      axis11: USID:PL16:0001
      axis12: ["Theoretical Physicist"]
      axis13: { tags: ['historical', 'model'], reviewed_by: ['Einstein, A.'] }
    metadata:
      confidence: 0.98
      provenance: doi:10.1093/acprof:9780198504241.003.0002
      compliance_tags: [ ]
      cultural_context: Western
      version: 2024.1
      last_reviewed: "2022-08-01"
      audit_trail:
        - by: system
          timestamp: "2022-08-01T10:00:00Z"
          action: create

```

### **2.3 Axis System Reference (`axes.yaml`)**

```yaml
axes:
  - axis: 1
    name: Pillar Domain
    description: Ontological pillar identifier PL01–PL87.
    encoding: "PL_code"
  - axis: 2
    name: Subdomain Typology
    description: Subdiscipline or industry mapping.
    encoding: "string"
  # ... (repeat for axes 3–13 as per table above)

```

---

## **3. Python Data Model (Pydantic)**

```python
from typing import List, Dict, Union, Optional
from pydantic import BaseModel

class AxisCoordinate(BaseModel):
    axis1: str                           # Pillar domain (PL code)
    axis2: Optional[str] = None          # Subdomain
    axis3: Optional[Union[str, int]] = None  # Branch path/hierarchy
    axis4: Optional[int] = None          # Depth
    axis5: Optional[Union[str, int]] = None  # Temporal
    axis6: Optional[str] = None          # Provenance/source
    axis7: Optional[str] = None          # Octopus/Ecosystem
    axis8: Optional[Union[str, List[str]]] = None  # Compliance
    axis9: Optional[float] = None        # Confidence
    axis10: Optional[str] = None         # Cultural/linguistic
    axis11: str                          # Unified System ID
    axis12: Optional[Union[str, List[str]]] = None    # Expert role context
    axis13: Optional[Union[str, Dict]] = None         # Dynamic/custom

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

class Pillar(BaseModel):
    pillar_id: str
    name: str
    description: str
    parent_pillar_id: Optional[str] = None
    metadata: Dict[str, Union[str, float, int, dict, list]]
    axes: AxisCoordinate

```

- **Note:** Dict `metadata` required for extensibility (provenance, confidence, audit, cultural).
- **All schema elements readily serializable for in-memory, YAML, and database adaptation.**

---

## **4. Interoperability & API Representation**

- **API Endpoints** should use above models for request/response, e.g.:
    - `GET /nodes/{id}` → returns `KnowledgeNode`
    - `POST /nodes` → expects full axis metadata block
- **Filtering** on endpoints (e.g. `/nodes?pillar=PL16&axis8=GDPR`) uses axis values directly.
- **Compliance/security tags** filter visibility at API serialization layer.
- **YAML/JSON-RPC Serialization** supported directly via the above schemas.

---

## **5. Stubs & Example Instantiation**

**Sample “in-memory” node:**

```python
sample_node = KnowledgeNode(
    node_id="USID:PL16:0001",
    label="Foundations of Gravity",
    description="Theories and models explaining gravitation, from Newtonian to contemporary theories.",
    pillar_id="PL16",
    axes=AxisCoordinate(
        axis1="PL16",
        axis2="Gravity",
        axis3="0.1",
        axis4=1,
        axis5="Year:1915",
        axis6="doi:10.1093/acprof:9780198504241.003.0002",
        axis7="Ecosystem:Physics",
        axis8=None,
        axis9=0.98,
        axis10="Western",
        axis11="USID:PL16:0001",
        axis12=["Theoretical Physicist"],
        axis13={"tags": ["historical", "model"], "reviewed_by": ["Einstein, A."]}
    ),
    metadata={
        "confidence": 0.98,
        "provenance": "doi:10.1093/acprof:9780198504241.003.0002",
        "compliance_tags": [],
        "cultural_context": "Western",
        "version": "2024.1",
        "last_reviewed": "2022-08-01",
        "audit_trail": []
    },
    simulation_roles=["Theoretical Physicist"],
    links=[]
)

```

---

## **6. Best Practices & Extensibility**

- **Schema files (YAML/JSON)**: Axis and pillar definitions are flat files, easily edited and hot-reloaded.
- **Metadata**: All objects allow arbitrary metatags (for compliance, provenance, audit, culture, version, and more).
- **Axis system**: Easily extensible—add new axis by extending the AxisCoordinate model and schemas, no full rewrite required.
- **Compliance**: API and schema designed for future ISO, HIPAA, GDPR, indigenous knowledge tags.
- **Simulation**: Axis-12 is reserved for quad/expert persona context; always include in modeling for future reasoning.
- **Localization/culture**: Axis-10 metadata should always be set, even if “default/Western”.

---

## **7. Specification Deliverables**

- [x]  **13-Axis Table** with names, definitions, encoding and roles
- [x]  **YAML schemas** for pillars, nodes, axes (see above)
- [x]  **Python/Pydantic models** for implementation and API sharing
- [x]  **Stubs/sample records** ready for both in-memory and file-based simulation
- [x]  **Direct mapping** to API contracts and compliance filtering

---

## **8. Next Steps / Handoff Notes**

- AI agents, recursive reasoning, and simulation engines can leverage the axis metadata for domain traversal and persona selection.
- Frontend teams can consume axis definitions for filter/slider UI.
- Security/compliance engineers have a clear reference for tagging and access patterns.
- Future DB choice (e.g. Neo4j) can natively ingest/export YAML-serialized model as shown.

---

## **9. References**

- Model follows best practices in [semantic web/knowledge graphs](https://www.w3.org/TR/rdf-schema/), [modern API data modeling](https://json-schema.org/), and compliance tagging (see GDPR, HIPAA standards).
- Aligns to requirements and metadata tagging for cross-sector/industry extensibility.

---

**This schema and modeling reference is directly deployable for further backend/API prototyping, test data generation, compliance/metadata engine integration, and is extensible for future roadmap axes and features as specified in the broader UKFW project.**
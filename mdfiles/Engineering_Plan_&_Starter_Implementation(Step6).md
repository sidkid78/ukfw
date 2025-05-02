## **1. UX PRINCIPLES & KEY INTERACTION GOALS**

- **Graph Navigation**: Visual drill-down from Pillar → Axis → Node; expose multi-dimensional axes and relationships visually (graph, matrix, or faceted).
- **Powerful Multi-modal Query**: Support text (“What is Axis 7/Octopus for PL48?”), filter, and expert persona queries; advanced axis selection.
- **Provenance, Confidence, & Compliance**: Present detailed metadata, source, confidence, regulatory tags, and simulated expert insights cleanly and intuitively.
- **Expert Persona Emulation**: Allow users to select/view responses as different expert personas and observe differences in output.
- **Usability for Scale**: Virtualized lists, progressive data loading, intelligent chunking, async graph exploration for large graphs.
- **Security/Compliance Awareness**: UI respects “compliance/visibility” flags returned by API.
- **Real-Time/Reactive**: Indicate live refinements, recursive loops (possible with polling/SSE upgrades).
- **Extensible Visual Foundations**: Abstracted data types, easily plugin new visualization or query modes.

---

## **2. RECOMMENDED FILE/FOLDER LAYOUT**

```
/ukfw-frontend/
  /app/
    layout.tsx
    page.tsx                          # Home/dashboard
    /pillars/
      [pillarId]/page.tsx
    /nodes/
      [nodeId]/page.tsx
    /axes/
      [axisNum]/[axisValue]/page.tsx
    /query/
      page.tsx                        # Advanced search/query UI

  /components/
    GraphViewer.tsx
    AxisInspector.tsx
    NodeDetailPanel.tsx
    QueryPanel.tsx
    PersonaSwitch.tsx
    ProvenancePanel.tsx
    ComplianceBadge.tsx

  /lib/
    api.ts                            # API calls (axios/fetch, configurable endpoint)
    types.ts                          # Types shared with backend (by OpenAPI or manual)
    utils.ts                          # Formatters/parsers

  /styles/
    (css|tailwind|chakra)

  /public/
    (icons, logos, etc.)

  /__tests__/
    (unit/integration tests)

```

---

## **3. CORE FUNCTIONALITY**

### **3.1 API INTEGRATION**

**Create api.ts:**

(Handles endpoints, adds persona, compliance, etc.)

```tsx
// lib/api.ts
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function getPillars() {
  const res = await fetch(`${BASE_URL}/pillars/`);
  return await res.json();
}

export async function getPillar(id: string) {
  const res = await fetch(`${BASE_URL}/pillars/${id}`);
  return await res.json();
}

export async function getNode(id: string, complianceTag?: string, persona?: string) {
  let url = `${BASE_URL}/nodes/${id}`;
  const params = [];
  if (complianceTag) params.push(`compliance=${encodeURIComponent(complianceTag)}`);
  // Add persona support if needed on endpoint
  if (params.length) url += '?' + params.join('&');
  const res = await fetch(url);
  return await res.json();
}

// Query nodes by axis, confidence, persona, etc.
export async function queryNodes({ axisFilters = {}, minConfidence, simulationRole, compliance }) {
  const params = new URLSearchParams();
  Object.entries(axisFilters).forEach(([k, v]) => v && params.append(k, v));
  if (minConfidence) params.append('min_confidence', String(minConfidence));
  if (simulationRole) params.append('simulation_role', simulationRole);
  if (compliance) params.append('axis8', compliance);
  const res = await fetch(`${BASE_URL}/nodes?${params}`);
  return await res.json();
}

```

---

### **3.2 DATA TYPES (Shared With Backend)**

**(lib/types.ts)** Use OpenAPI-generated types (with openapi-typescript) or handcraft key types for rapid dev:

```
export interface AxisCoordinate {
  axis1: string;
  axis2?: string;
  // ... up to axis13
  axis13?: any;
}

export interface KnowledgeNodeLink {
  target_node_id: string;
  relationship_type: string;
  weight?: number;
  axis_vector_diff?: any[];
  metadata?: Record<string, any>;
}

export interface KnowledgeNode {
  node_id: string;
  label: string;
  description: string;
  pillar_id: string;
  axes: AxisCoordinate;
  metadata: Record<string, any>;
  simulation_roles?: string[];
  links?: KnowledgeNodeLink[];
  compliance_visible?: boolean;
}

export interface Pillar {
  pillar_id: string;
  name: string;
  description: string;
  parent_pillar_id?: string;
  axes: AxisCoordinate;
  metadata: Record<string, any>;
}

```

---

### **3.3 GRAPH VISUALIZATION**

- For interactive/large graphs: **react-force-graph** ([react-force-graph](https://github.com/vasturiano/react-force-graph)), **Sigma.js**, or **Cytoscape.js** via React adapters.
- Abstract nodes/edges for graph compatibility.
- **Virtualized Table/List/Tree** for alternative axis-centered exploration.

**components/GraphViewer.tsx**

```tsx
import dynamic from 'next/dynamic';
import { KnowledgeNode } from '../lib/types';

// Use dynamic import to avoid SSR issues (these libraries are often browser-only)
const ForceGraph2D = dynamic(() => import('react-force-graph').then(mod => mod.ForceGraph2D), { ssr: false });

export default function GraphViewer({ nodes, onNodeClick }) {
  // Transform KnowledgeNode list into graph format
  const graphData = {
    nodes: nodes.map(n => ({ id: n.node_id, name: n.label, pillar: n.pillar_id, ...n })),
    links: nodes.flatMap(n =>
      (n.links || []).map(l => ({
        source: n.node_id,
        target: l.target_node_id,
        label: l.relationship_type,
        weight: l.weight || 1,
      }))
    ),
  };

  return (
    <ForceGraph2D
      graphData={graphData}
      nodeLabel="name"
      nodeAutoColorBy="pillar"
      linkLabel="label"
      onNodeClick={onNodeClick}
      width={800}
      height={600}
    />
  );
}

```

---

### **3.4 AXIS INSPECTOR**

Lets users drill by axis: see which nodes are contained by any set of axis coordinates, and what’s available per axis (faceted navigation).

**components/AxisInspector.tsx**

```tsx
import { useState } from 'react';

export default function AxisInspector({ axes, onAxisSelect }) {
  return (
    <div className="axis-inspector">
      {Object.entries(axes).map(([axis, value]) => (
        <div key={axis}>
          <strong>{axis.toUpperCase()}</strong>:&nbsp;
          <span style={{ cursor: 'pointer', textDecoration: 'underline' }}
                onClick={() => onAxisSelect(axis, value)}>
            {String(value)}
          </span>
        </div>
      ))}
    </div>
  );
}

```

---

### **3.5 NODE DETAIL / METADATA VIEW**

Shows node description, provenance, simulation, confidence, compliance, and axis coordinates.

**components/NodeDetailPanel.tsx**

```tsx
import ProvenancePanel from './ProvenancePanel';
import ComplianceBadge from './ComplianceBadge';

export default function NodeDetailPanel({ node }) {
  return (
    <div className="node-detail">
      <h2>{node.label}</h2>
      <p>{node.description}</p>
      <div>Node ID: <code>{node.node_id}</code></div>
      <div>Pillar: <code>{node.pillar_id}</code></div>
      <AxisInspector axes={node.axes} onAxisSelect={(a, v) => {/*...*/}} />
      <ComplianceBadge tags={node.axes.axis8} />
      <ProvenancePanel metadata={node.metadata} />
      <div>
        <b>Confidence:</b> {((node.axes.axis9 ?? 0) * 100).toFixed(1)}%
      </div>
      {node.simulation_roles?.length &&
        <div>
          <b>Simulated expertise:</b> {node.simulation_roles.join(', ')}
        </div>
      }
      {/* Optionally show links/related nodes */}
    </div>
  );
}

```

**Provenance and Compliance UI:**

```tsx
// components/ComplianceBadge.tsx
export function ComplianceBadge({ tags }) {
  if (!tags) return null;
  const tagList = Array.isArray(tags) ? tags : [tags];
  return (
    <span>
      {tagList.map(tag => (
        <span key={tag} className="badge badge-compliance">{tag}</span>
      ))}
    </span>
  );
}

// components/ProvenancePanel.tsx
export function ProvenancePanel({ metadata }) {
  return (
    <div className="provenance">
      {/* source attribution, audit trail, etc. */}
      {metadata?.provenance && (
        <div>
          <b>Source:</b> {metadata.provenance}
        </div>
      )}
      {metadata?.audit_trail &&
        <pre className="provenance-trail">{JSON.stringify(metadata.audit_trail, null, 2)}</pre>
      }
    </div>
  );
}

```

---

### **3.6 PERSONA/EXPERT ROLE SWITCHER**

Let user select which simulated expert they wish AI responses from.

**components/PersonaSwitch.tsx**

```tsx
export default function PersonaSwitch({ personas, value, onChange }) {
  return (
    <select value={value} onChange={(e) => onChange(e.target.value)}>
      <option value="">Default Expert</option>
      {personas.map(persona => (
        <option key={persona} value={persona}>{persona}</option>
      ))}
    </select>
  );
}

```

---

### **3.7 ADVANCED QUERY UI**

- Support axis selection, min confidence slider, persona, compliance.
- Submit runs queryNodes({axisFilters, minConfidence, ...}).

**components/QueryPanel.tsx**

```tsx
import { useState } from 'react';
import { queryNodes } from '../lib/api';

export default function QueryPanel({ onResults }) {
  const [axis1, setAxis1] = useState('');
  const [axis8, setAxis8] = useState('');  // compliance tag
  const [minConfidence, setMinConfidence] = useState(0.8);
  const [persona, setPersona] = useState('');

  async function submit(e) {
    e.preventDefault();
    const results = await queryNodes({
      axisFilters: { axis1, axis8 },
      minConfidence,
      simulationRole: persona,
      compliance: axis8,
    });
    onResults(results);
  }

  return (
    <form onSubmit={submit}>
      <input value={axis1} onChange={e => setAxis1(e.target.value)} placeholder="Axis1 (Pillar)" />
      <input value={axis8} onChange={e => setAxis8(e.target.value)} placeholder="Compliance tag"/>
      <input type="number" min={0} max={1} step={0.01} value={minConfidence}
           onChange={e => setMinConfidence(Number(e.target.value))} />
      {/* Persona picker */}
      <input value={persona} onChange={e => setPersona(e.target.value)} placeholder="Expert persona" />
      <button type="submit">Query</button>
    </form>
  );
}

```

---

## **4. ROUTING/UI PAGES EXAMPLES**

### **4.1 Home (Knowledge Dashboard)**

**app/page.tsx**

```tsx
import { getPillars } from '../lib/api';
import Link from 'next/link';

export default async function Home() {
  const pillars = await getPillars();
  return (
    <div>
      <h1>UKFW Knowledge Graph</h1>
      <ul>
        {pillars.map(p => (
          <li key={p.pillar_id}><Link href={`/pillars/${p.pillar_id}`}>{p.name}</Link></li>
        ))}
      </ul>
      {/* Optionally, show stats, query panel, main graph snapshot */}
    </div>
  );
}

```

### **4.2 Pillar Detail**

**app/pillars/[pillarId]/page.tsx**

```tsx
import { getPillar, queryNodes } from '../../../lib/api';
import GraphViewer from '../../../components/GraphViewer';

export default async function PillarPage({ params }) {
  const pillar = await getPillar(params.pillarId);
  const nodes = await queryNodes({ axisFilters: { axis1: pillar.name }});
  return (
    <div>
      <h2>Pillar: {pillar.name}</h2>
      <p>{pillar.description}</p>
      <GraphViewer nodes={nodes} onNodeClick={/* ...route to node */} />
    </div>
  );
}

```

### **4.3 Node Detail**

**app/nodes/[nodeId]/page.tsx**

```tsx
import { getNode } from '../../../lib/api';
import NodeDetailPanel from '../../../components/NodeDetailPanel';

export default async function NodePage({ params, searchParams }) {
  const compliance = searchParams.compliance;
  const persona = searchParams.persona;
  const node = await getNode(params.nodeId, compliance, persona);
  return <NodeDetailPanel node={node} />;
}

```

---

## **5. VISUAL SCALE, PERFORMANCE & REAL-TIME**

- Use **windowed/virtualized lists** for thousands of nodes.
- Fetch graph/query results **lazily** (on node click, expand, or via faceted batch).
- Consider **SWR/react-query for caching/revalidation**.
- For recursive/long-running simulation, support **polling** (loading.../confidence updating) or add **WebSocket/SSE** UI if/when backend supports.

---

## **6. ACCESSIBILITY, SECURITY, COMPLIANCE FRONTEND MEASURES**

- Hide/display nodes/UI elements as per `compliance_visible` and axis 8 returned fields.
- Ensure query forms can only select/submit allowed compliance/persona combos.
- Show compliance tags (HIPAA, GDPR, etc.) visibly in results/cards.
- Support “expand metadata” for expert/validation history, audit trails.

---

## **7. STYLES & COMPONENTIZATION**

- Consider **Tailwind**/ChakraUI for rapid grid/layout/faceting.
- Relate badge, panel, axis, etc to a modular atomic design.

---

## **8. TESTING**

- Use **Jest/React Testing Library** for UI unit, **Cypress/Playwright** for e2e.
- Mock API layer with realistic type data for frontend-inside tests.

---

## **9. EXTENSION PATHS**

- Add **multi-modal input** (upload, image, etc) later—scaffold now via button/file input.
- Add graph **edit** or contribution if permissions.
- Plug-in advanced OpenAPI types with code-gen for strict type contract.

---

## **10. SUMMARY TABLE**

| **Component** | **Location** | **Key Roles** |
| --- | --- | --- |
| API integration | lib/api.ts | Fetches/query, persona, compliance |
| Graph visualization | components/GraphViewer.tsx | Pillar/Axis/Node/Relation exploration |
| Axis Inspector | components/AxisInspector.tsx | Multi-axis drilldown/context nav |
| Node details | components/NodeDetailPanel.tsx | Metadata, provenance, compliance, axes |
| Query UI | components/QueryPanel.tsx | Complex, persona, compliance query |
| Persona Switcher | components/PersonaSwitch.tsx | Emulate experts/simulated outputs |
| Compliance UI | components/ComplianceBadge.tsx | Regulatory context, secure display |
| Provenance/Audit UI | components/ProvenancePanel.tsx | Source/history/recursive display |

---

## **11. MINIMUM FUNCTIONAL BOOTSTRAP DELIVERABLE**

1. **Set up Next.js App Router project.**
2. Implement API methods (see above for `lib/api.ts`, configure endpoint!).
3. Implement core shared types.
4. Scaffold out pages for `/pillars`, `/pillars/[pillarId]`, `/nodes/[nodeId]`.
5. Add **GraphViewer** using mock or real node data.
6. Add advanced **QueryPanel** for axis/compliance/persona input/output.
7. Implement NodeDetailPanel with axis, confidence, provenance, compliance.

*You now have a UI enabling hierarchical multi-axis graph visualization, multi-modal queries, persona toggling, and rich compliance-aware detail—all mapped to your FastAPI contract.*

---

**This foundation fully supports your backend API, is highly extensible, and enables rapid evolution toward advanced AI/UX/graph-driven interfaces as the UKFW system grows.**
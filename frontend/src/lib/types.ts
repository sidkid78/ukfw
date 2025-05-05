export interface AxisCoordinate {
  axis1: string;
  axis2?: string;
  axis3?: string;
  axis4?: number;
  axis5?: string;
  axis6?: string;
  axis7?: string;
  axis8?: string | string[];
  axis9?: number;
  axis10?: string;
  axis11?: string;
  axis12?: string | string[];
  axis13?: Record<string, string | number | boolean | Record<string, string | number | boolean>>;
}

export interface KnowledgeNodeLink {
  target_node_id: string;
  relationship_type: string;
  weight?: number;
  axis_vector_diff?: (number | string)[];
  metadata?: Record<string, string | number | boolean | Record<string, string | number | boolean>>;
}

// Define a more specific type for node metadata
export interface NodeMetadata {
  provenance?: string;
  audit_trail?: unknown[]; // Use unknown[] instead of any[]
  confidence?: number; // Or use axis9?
  compliance?: string | string[]; // Specify the type for compliance
  [key: string]: unknown; // Use unknown instead of any for other keys
}

export interface KnowledgeNode {
  node_id: string;
  label: string;
  description: string;
  pillar_id: string;
  axes: AxisCoordinate;
  metadata: NodeMetadata; // Use the specific metadata type
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
  metadata: Record<string, string | number | boolean | Record<string, string | number | boolean>>;
}

// --- New Regulatory Mapping Types (from mappings.md) ---

export enum RegulatoryAxis {
  JURISDICTION = 'jurisdiction',
  PILLAR = 'pillar',
  PROVISION = 'provision',
  ROLE = 'role',
  EXPERT = 'expert',
  SPIDERWEB = 'spiderweb',
  HONEYCOMB = 'honeycomb',
  OCTOPUS = 'octopus',
  LOCATION = 'location'
}

export interface Regulation {
  id: string;
  title: string;
  description?: string;
  jurisdiction: string;
  pillar: string;
  location_code?: string;
  effective_date?: string; // Use string for dates, format as needed
  provisions: string[];
}

export interface Provision {
  id: string;
  regulation_id: string;
  section: string;
  title: string;
  text: string;
  hierarchy_level: number;
  parent_id?: string;
  jurisdiction: string;
  roles_responsible: string[];
  crosswalks: string[];
  spiderweb_links: string[];
  octopus_refs: string[];
  tags: string[];
}

export interface Role {
  id: string;
  name: string;
  description?: string;
  jurisdiction?: string;
  expertise_domains: string[];
  provisions: string[];
}

export interface Expert {
  id: string;
  name: string;
  role_id: string;
  domains: string[];
  provisions: string[];
  location?: string;
  contact?: string;
}

export interface SpiderwebNode {
  id: string;
  source_provision: string;
  target_provision: string;
  relationship_type: string;
  weight: number;
  risk?: number;
  note?: string;
  created_at: string; // Use string for datetimes
  axes_involved: RegulatoryAxis[];
}

export interface HoneycombNode {
  id: string;
  source_provision: string;
  target_provision: string;
  xwalk_type: string;
  axes_involved: RegulatoryAxis[];
  weight?: number;
  note?: string;
}

export interface OctopusNode {
  id: string;
  domain: string;
  regulatory_bodies: string[];
  parent_nodes?: string[];
  linked_provisions: string[];
  experts: string[];
  axes_involved: RegulatoryAxis[];
}


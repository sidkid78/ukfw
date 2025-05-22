import type { 
  Regulation, Provision, Role, Expert, 
  SpiderwebNode, HoneycombNode, OctopusNode,
  ReasoningTrace, ReasoningStep, PersonaProfile, 
  EducationRequirement, CertificationLicense, Publication
} from './types';

// Re-export the types to mark them as used by this module's public API
export type { 
  ReasoningTrace, ReasoningStep, PersonaProfile, 
  EducationRequirement, CertificationLicense, Publication,
  // Also include others if they are part of other function signatures in this file 
  // or if this file is intended as the primary type export hub for its features.
  // For now, focusing on the ones related to runQuadReasoning and flagged by linter.
  Regulation, Provision, Role, Expert, // Assuming these are used by other exported functions
  SpiderwebNode, HoneycombNode, OctopusNode // Assuming these are used by other exported functions
};

const BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// --- Regulation Endpoints (was Pillar) ---
export async function getRegulations(): Promise<Regulation[]> {
  console.log(`Fetching regulations from: ${BASE_URL}/regulations`); // Log URL
  try {
    const res = await fetch(`${BASE_URL}/regulations`); // Changed endpoint
    console.log("Fetch response status:", res.status);
    if (!res.ok) {
      const errorText = await res.text().catch(() => 'Could not read error response text');
      console.error("Fetch error details:", res.status, errorText);
      throw new Error('Failed to fetch regulations');
    }
    const data = await res.json();
    console.log("Fetched regulations data:", data); // Log successful data
    return data;
  } catch (error) {
    console.error("Error during fetch/processing:", error); // Log any other errors
    // Re-throw the error to be caught by the calling component
    throw new Error(`Failed to fetch regulations: ${error instanceof Error ? error.message : String(error)}`); 
  }
}

export async function getRegulation(id: string): Promise<Regulation> {
  const res = await fetch(`${BASE_URL}/regulations/${id}`); // Changed endpoint
  if (!res.ok) throw new Error(`Failed to fetch regulation ${id}`);
  return await res.json();
}

// --- Provision Endpoints (was Node) ---
export async function getProvision(id: string): Promise<Provision> {
  const res = await fetch(`${BASE_URL}/provisions/${id}`); // Changed endpoint
  if (!res.ok) throw new Error(`Failed to fetch provision ${id}`);
  return await res.json();
}

// Interface for query parameters, matching backend
interface QueryProvisionsParams {
  regulation_id?: string;
  jurisdiction?: string;
  tag?: string;
  role_id?: string;
  min_confidence?: number;
  compliance_tag?: string;
}

export async function queryProvisions(queryParams: QueryProvisionsParams): Promise<Provision[]> {
  const params = new URLSearchParams();
  // Append parameters only if they have a value
  if (queryParams.regulation_id) params.append('regulation_id', queryParams.regulation_id);
  if (queryParams.jurisdiction) params.append('jurisdiction', queryParams.jurisdiction);
  if (queryParams.tag) params.append('tag', queryParams.tag);
  if (queryParams.role_id) params.append('role_id', queryParams.role_id);

  const queryString = params.toString();
  const url = `${BASE_URL}/provisions${queryString ? '?' + queryString : ''}`; // Changed endpoint
  
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to query provisions');
  return await res.json();
}

// --- Role Endpoint ---
export async function getRoleById(id: string): Promise<Role> {
  const res = await fetch(`${BASE_URL}/roles/${id}`);
  if (!res.ok) {
    console.error(`API Error: Failed to fetch role ${id}`, res.status, await res.text().catch(() => ''));
    throw new Error(`Failed to fetch role ${id}`);
  }
  return await res.json();
}

// --- Expert Endpoint ---
export async function getExpertById(id: string): Promise<Expert | null> {
  try {
    const response = await fetch(`${BASE_URL}/experts/${id}`);
    if (!response.ok) {
      if (response.status === 404) {
        console.warn(`Expert with ID ${id} not found.`);
        return null;
      }
      throw new Error(`Failed to fetch expert ${id}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error fetching expert:", error);
    return null;
  }
}

// Placeholder function to get all roles (if needed)
export async function getAllRoles(): Promise<Role[]> {
  // Assuming an endpoint `/roles` exists or will be added
  const res = await fetch(`${BASE_URL}/roles`); 
  if (!res.ok) throw new Error('Failed to fetch all roles');
  return await res.json();
}

// Placeholder function to get all experts (if needed)
export async function getAllExperts(): Promise<Expert[]> {
  // Assuming an endpoint `/experts` exists or will be added
  const res = await fetch(`${BASE_URL}/experts`);
  if (!res.ok) throw new Error('Failed to fetch all experts');
  return await res.json();
}

// Define expected response structure for provision mapping
export interface ProvisionMappingResponse {
  provision: Provision;
  spiderwebs: SpiderwebNode[];
  honeycombs: HoneycombNode[];
  octopus: OctopusNode[]; // Assuming the mapping endpoint returns full Octopus nodes
  roles: Role[];
  experts: Expert[];
  spiderweb_score?: number; // Add other relevant scores if returned by API
  compliance_score?: number;
  simulated_expert?: Expert | { name: string; role?: string };
}

// Example placeholder for a mapping endpoint mentioned in mappings.md
export async function getProvisionMapping(provisionId: string): Promise<ProvisionMappingResponse> {
  // Assuming an endpoint like /mapping/provision/{provisionId} exists
  const res = await fetch(`${BASE_URL}/mapping/provision/${provisionId}`); 
  if (!res.ok) throw new Error(`Failed to fetch mapping for provision ${provisionId}`);
  return await res.json(); 
}

// Define expected response structure for audit manifest
export interface AuditManifestResponse {
  regulation: Regulation;
  provisions: Array<{ // Simplified provision info for the manifest view
    provision_id: string;
    title: string;
    status: number; // 0 or 1
    spiderwebs?: SpiderwebNode[]; // Use specific type for spiderwebs
  }>;
  total_gap_score: number;
  gaps: Array<{ // Gap item structure
    provision_id: string;
    title: string;
    missing: boolean;
    expected: number;
    actual: number;
  }>;
}

// Example placeholder for audit manifest endpoint
export async function getAuditManifest(regulationId: string): Promise<AuditManifestResponse> {
  const res = await fetch(`${BASE_URL}/audit/manifest/${regulationId}`); 
  if (!res.ok) throw new Error(`Failed to fetch audit manifest for regulation ${regulationId}`);
  return await res.json(); 
}

// --- Quad Persona Reasoning Endpoint ---
export async function runQuadReasoning(query: string, provisionId?: string): Promise<ReasoningTrace | null> {
  try {
    const requestBody: { query: string; provision_id?: string } = { query };
    if (provisionId) {
      requestBody.provision_id = provisionId;
    }

    const response = await fetch(`${BASE_URL}/reason/quad`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: response.statusText }));
      console.error(`Failed to run quad reasoning: ${response.status}`, errorData);
      throw new Error(`Failed to run quad reasoning: ${errorData.detail || response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error running quad reasoning:", error);
    return null;
  }
}

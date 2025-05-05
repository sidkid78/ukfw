export type PersonaMetadata = {
    persona_type: string;
    name: string;
    job_roles: string[];
    skills: string[];
    certifications: string[];
    training: string[];
    education: string[];
    research_base: string[];
  };
  
  export type PersonaTrace = {
    persona: PersonaMetadata;
    step: number;
    title: string;
    summary: string;
    details?: string;
  };
  
  export type QuadPersonaResponse = {
    query: string;
    trace: PersonaTrace[];
    final_response: string;
  };
  
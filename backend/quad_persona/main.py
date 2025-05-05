from fastapi import FastAPI 
from typing import List, Dict 

from quad_persona.persona_functions import simulate_knowledge_expert, simulate_sector_expert, simulate_regulatory_expert, simulate_compliance_expert
from quad_persona.schema.data_models import QuadPersonaResponse, PersonaTrace 

app = FastAPI(title="Quad Persona Engine")

@app.post("/quad-persona", response_model=QuadPersonaResponse)
def run_quad_persona(request: Dict[str, str]):
    query = request["query"]
    trace = [] 
    step_results = []
    # P1: Knowledge Expert
    p1_summary, p1_meta = simulate_knowledge_expert(query, step_results)
    trace.append(PersonaTrace(persona=p1_meta, step=1, title="Theoretical Coverage", summary=p1_summary, details=""))
    step_results.append(p1_summary)
    # P2: Sector Expert 
    p2_summary, p2_meta = simulate_sector_expert(query, step_results)
    trace.append(PersonaTrace(persona=p2_meta, step=2, title="Industry Contextualization", summary=p2_summary, details=""))
    step_results.append(p2_summary)
    # P3: Regulatory Expert 
    p3_summary, p3_meta = simulate_regulatory_expert(query, step_results)
    trace.append(PersonaTrace(persona=p3_meta, step=3, title="Regulatory Overlay", summary=p3_summary, details=""))
    step_results.append(p3_summary)
    # P4: Compliance Expert 
    p4_summary, p4_meta = simulate_compliance_expert(query, step_results)
    trace.append(PersonaTrace(persona=p4_meta, step=4, title="Compliance Finalization", summary=p4_summary, details=""))
    step_results.append(p4_summary)
    # Compose final response 
    final = "\n\n".join(t.summary for t in trace)
    return QuadPersonaResponse(query=query, trace=trace, final_response=final)
    
    
    
    

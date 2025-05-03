import os
import openai

# Load env vars (for local dev)
from dotenv import load_dotenv
load_dotenv()

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4.1")

def structural_validation(node, context):
    score = 1.0 if getattr(node, 'label', None) and getattr(node, 'links', None) else 0.9
    return {"validation": score, "explanation": "Basic structure verified."}


def taxonomy_integrity(node, context):
    score = 1.0 if getattr(node, 'pillar_id', None) in getattr(context, 'pillars', {}) else 0.8
    return {"validation": score, "explanation": "Taxonomy/pillar integrity checked."}

def compliance_check(node, context):
    tags = getattr(node.axes, 'axis8', None)
    compliant = tags is None or "GDPR" in tags or "HIPAA" in tags
    score = 1.0 if compliant else 0.0
    return {"validation": score, "explanation": "Compliance tags checked."}

def confidence_validator(node, context):
    if getattr(node.axes, 'axis9', None) is None:
        return {"validation": 0.5, "explanation": "No confidence declared"}
    return {"validation": node.axes.axis9, "explanation": "Confidence field read"}

def gpt_4_1_expert_reasoning(node, context, prompt_template=None):
    """
    Calls Azure OpenAI GPT-4.1 to reason about the node.
    """
    if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_ENDPOINT:
        return {"validation": 0.0, "explanation": "Azure OpenAI credentials not set."}

    # Build prompt
    prompt = prompt_template or (
        f"You are an expert knowledge graph validator. "
        f"Given the following node and context, assess its validity, confidence, and suggest improvements.\n"
        f"Node: {node}\nContext: {context}\n"
        f"Respond with a JSON: {{'validation': float, 'explanation': str}}"
    )

    try:
        response = openai.chat.completions.create(
            api_key=AZURE_OPENAI_API_KEY,
            api_base=AZURE_OPENAI_ENDPOINT,
            api_type="azure",
            api_version="2024-12-01-preview",  # Use the latest available
            deployment_id=AZURE_OPENAI_DEPLOYMENT_NAME,
            model="gpt-4-1",  # Optional, for clarity
            messages=[
                {"role": "system", "content": "You are a domain expert for knowledge graph validation."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=512,
        )
        # Parse response
        content = response.choices[0].message["content"]
        import json
        result = json.loads(content)
        return result
    except Exception as e:
        return {"validation": 0.0, "explanation": f"GPT-4.1 error: {str(e)}"}

KNOWLEDGE_ALGORITHMS = {
    "structural_validation": structural_validation,
    "taxonomy_integrity": taxonomy_integrity,
    "compliance_check": compliance_check,
    "confidence_validator": confidence_validator,
    "gpt_4_1_expert_reasoning": gpt_4_1_expert_reasoning,
    # etc.
}

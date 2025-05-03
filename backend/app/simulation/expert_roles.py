EXPERT_ROLE_LIBRARY = {
    "Knowledge Expert": {
        "description": "Deep understanding of structural and factual organization.",
        "algorithms": ["structural_validation", "taxonomy_integrity"]
    },
    "Sector Expert": {
        "description": "Applies sector-specific knowledge and heuristics.",
        "algorithms": ["sector_rules", "industry_regulations"]
    },
    "Regulatory Expert": {
        "description": "Validates regulatory and compliance alignment.",
        "algorithms": ["compliance_check", "gdpr_check", "hipaa_check"]
    },
    "Compliance Agent": {
        "description": "Enforces security, audits provenance."
    },
    "Theoretical Physicist": {
        "description": "Models advanced theoretical relationships.",
        "algorithms": ["theoretical_consistency"]
    },
    "LLM Expert": {
        "description": "Uses GPT-4.1 for advanced reasoning and validation.",
        "algorithms": ["gpt_4_1_expert_reasoning"]
    },
    # ... extend with more as per UKFW plan
}

def get_roles_for_node(node):
    # Use node.axis12 (expertise required) or simulation_roles etc.
    if hasattr(node, 'simulation_roles') and node.simulation_roles:
        return node.simulation_roles
    elif hasattr(node, 'axes') and getattr(node.axes, 'axis12', None):
        axis12 = node.axes.axis12
        return axis12 if isinstance(axis12, list) else [axis12]
    else:
        # Default roles (fallback)
        return ["Knowledge Expert", "Sector Expert"]

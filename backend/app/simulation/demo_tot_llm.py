import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from simulation.tree_of_thought import tree_of_thought_refinement
from simulation.knowledge_algorithms import KNOWLEDGE_ALGORITHMS

# Uncomment to mock the LLM for a dry run (no API call)
def mock_gpt_4_1_expert_reasoning(node, context, prompt_template=None):
    return {"validation": 0.95, "explanation": "Mocked GPT-4.1: node looks good."}
KNOWLEDGE_ALGORITHMS["gpt_4_1_expert_reasoning"] = mock_gpt_4_1_expert_reasoning

class Axes:
    axis9 = 0.0  # Initial confidence
    axis12 = None  # Not used here

class Node:
    node_id = "demo-node"
    label = "Demo Node"
    links = ["n2"]
    axes = Axes()
    simulation_roles = ["LLM Expert"]
    metadata = {}

class Context:
    pillars = {"pillar1": "desc"}

if __name__ == "__main__":
    node = Node()
    context = Context()
    updated_node, history = tree_of_thought_refinement(node, context, confidence_goal=0.9)
    print("Final confidence:", updated_node.axes.axis9)
    print("Refinement history:")
    import json
    print(json.dumps(history, indent=2))
    print("LLM explanation(s):")
    for h in history:
        for action in h["actions"]:
            if action["role"] == "LLM Expert":
                print("-", action["result"]["explanation"])
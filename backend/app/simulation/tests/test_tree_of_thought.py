import pytest
from simulation.tree_of_thought import tree_of_thought_refinement
from simulation.knowledge_algorithms import KNOWLEDGE_ALGORITHMS

# Mock the GPT-4.1 function to avoid real API calls
def mock_gpt_4_1_expert_reasoning(node, context, prompt_template=None):
    return {"validation": 0.95, "explanation": "Mocked GPT-4.1: node looks good."}

def test_tot_with_llm(monkeypatch):
    # Patch the LLM function
    monkeypatch.setitem(KNOWLEDGE_ALGORITHMS, "gpt_4_1_expert_reasoning", mock_gpt_4_1_expert_reasoning)

    # Minimal node/context stubs
    class Axes: axis9 = 0.0
    class Node:
        node_id = "test-node"
        label = "Test Node"
        links = ["n2"]
        axes = Axes()
        simulation_roles = ["LLM Expert"]
        metadata = {}

    class Context:
        pillars = {"pillar1": "desc"}

    node = Node()
    context = Context()

    # Run ToT loop
    updated_node, history = tree_of_thought_refinement(node, context, confidence_goal=0.9)
    assert updated_node.axes.axis9 >= 0.9
    assert any(
        action["role"] == "LLM Expert" and action["algorithm"] == "gpt_4_1_expert_reasoning"
        for h in history for action in h["actions"]
    )
    print("Test passed. Node confidence:", updated_node.axes.axis9)

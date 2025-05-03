import yaml
import pytest
from backend.app.models import KnowledgeNode, Pillar

def test_load_pillars():
    with open("backend/app/data/pillars.yaml") as f:
        data = yaml.safe_load(f)
        for p in data["pillars"]:
            Pillar(**p)

def test_load_nodes():
    with open("backend/app/data/nodes.yaml") as f:
        data = yaml.safe_load(f)
        for n in data["nodes"]:
            KnowledgeNode(**n)

def test_load_axes():
    with open("backend/app/data/axes.yaml") as f:
        data = yaml.safe_load(f)
        for a in data["axes"]:
            assert "axis" in a and "name" in a

def test_compliance_tags():
    with open("backend/app/data/nodes.yaml") as f:
        data = yaml.safe_load(f)
        for n in data["nodes"]:
            tags = n["axes"].get("axis8")
            if tags:
                tag_list = tags if isinstance(tags, list) else [tags]
                for tag in tag_list:
                    assert tag in {"GDPR", "HIPAA", "None"}, f"Invalid compliance tag: {tag}"

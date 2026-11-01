import pytest
 
from agent.errors import DecisionError
from agent.validator import validate_decision
 
 
def test_valid_lookup():
    validate_decision({"action": "lookup_code_smell", "arguments": {"name": "Large class"}})
 
 
@pytest.mark.parametrize("decision", [
    {"action": "delete_files", "arguments": {}},
    {"action": "lookup_code_smell", "arguments": {}},
    {"action": "lookup_code_smell", "arguments": {"name": 100}},
    {"action": "finish"},
])
def test_invalid_decisions(decision):
    with pytest.raises(DecisionError):
        validate_decision(decision)

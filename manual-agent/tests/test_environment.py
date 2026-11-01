from agent.environment import NOT_FOUND, lookup_code_smell
 
 
def test_existing_code_smell():
    assert lookup_code_smell("large-class").startswith("large-class:")
 
 
def test_name_is_normalized():
    assert lookup_code_smell("   DaTa CLumps ").startswith("data-clumps:")
 
 
def test_unknown_code_smell():
    assert lookup_code_smell("uknown code smell").startswith(NOT_FOUND)

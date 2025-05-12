from app.tools.no_response import clarification_message
from app.tools.no_response import no_response
from app.tools.no_response import agent_response


def test_clarification_message_format():
    result = clarification_message()
    assert isinstance(result, dict)
    assert result["Category"] == "Agent"
    assert isinstance(result["result"], list)
    assert len(result["result"]) == 1
    assert isinstance(result["result"][0], str)
    
def test_no_response_format():
    query = "What is TB?"
    result = no_response(query)
    assert isinstance(result, dict)
    assert result["question"] == query
    assert result["type"] == "By Search Query"
    assert result["Category"] == "NTEP"
    assert isinstance(result["anwser"], list)
    assert len(result["anwser"]) == 1
    assert isinstance(result["anwser"][0], str)
    
def test_agent_response_format():
    result = agent_response()
    assert isinstance(result, dict)
    assert result["Category"] == "Agent"
    assert isinstance(result["result"], list)
    assert len(result["result"]) == 1
    assert isinstance(result["result"][0], str)

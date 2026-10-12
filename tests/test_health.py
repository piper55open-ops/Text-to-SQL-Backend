from server import app
from unittest.mock import patch

def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_question_is_trimmed():
    client = app.test_client()

    with patch("server.run_agent_for_web") as mock_agent:
        mock_agent.return_value = "fake answer"

        response = client.post(
            "/api/chat",
            json={"question": "   How many users?   "}
        )

    assert response.status_code == 200
    assert response.get_json() == {"answer": "fake answer"}

    mock_agent.assert_called_once_with("How many users?")

def test_whitespace_question():
    client = app.test_client()

    with patch("server.run_agent_for_web") as mock_agent:
        response = client.post(
            "/api/chat",
            json={"question": "   "}
        )

    assert response.status_code == 400
    assert response.get_json() == {"error": "没收到问题呀"}

    mock_agent.assert_not_called()

def test_non_string_question():
    client = app.test_client()

    with patch("server.run_agent_for_web") as mock_agent:
        response = client.post(
            "/api/chat",
            json={"question": 123}
        )

    assert response.status_code == 400
    assert response.get_json() == {"error": "没收到问题呀"}

    mock_agent.assert_not_called()
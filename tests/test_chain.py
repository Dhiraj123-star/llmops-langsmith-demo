from src.run import ask

def test_ask_returns_string():
    response = ask("What is CI/CD?")
    assert isinstance(response, str)
    assert len(response) > 0
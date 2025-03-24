import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.enums import AppEnum

client = TestClient(app)


# Mock the file writer to avoid actual file operations during tests
@pytest.fixture(autouse=True)
def mock_append_output(monkeypatch):
    # This will store the calls to the mocked function
    calls = []

    # Mock
    def mock_append(company, record_type, data):
        calls.append({"company": company, "record_type": record_type, "data": data})

    # Set the function to be replaced with the mock
    monkeypatch.setattr("app.main.append_output_to_jsonl", mock_append)

    # Return the calls list, to be used in tests to assert the correct calls were made
    return calls


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": AppEnum.ROOT_ENDPOINT_MSSG}

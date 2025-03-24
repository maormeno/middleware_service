import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.enums import AppEnum, InvoiceEnum

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_append_output_to_jsonl_calls(monkeypatch):
    """Mock the file writer to avoid actual file operations during tests"""
    # This will store the calls to the mocked function
    calls = []

    # Mock
    def mock_append(company, record_type, data):
        calls.append({"company": company, "record_type": record_type, "data": data})

    # Set the function to be replaced with the mock, keep in mind that mocking functions
    # has to be where the function is used, not where it is defined
    monkeypatch.setattr("app.main.append_output_to_jsonl", mock_append)

    # Return the calls list, to be used in tests to assert the correct calls were made
    return calls


def test_api_missing_fields(mock_append_output_to_jsonl_calls):
    """Test that the API returns a 422 error when the required fields are missing"""
    invoice_data = {
        "mock_wrong_field": "mock_wrong_value",
    }

    response = client.post("/invoice-record", json=invoice_data)

    # Check the file writing function was not called
    assert len(mock_append_output_to_jsonl_calls) == 0

    # Check the response
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert AppEnum.MISSING_REQUIRED_FIELDS_MSSG in response.json()["detail"]


def test_api_lines_empty(mock_append_output_to_jsonl_calls):
    """Test that the API returns a 422 error when the lines are empty"""
    invoice_data = {
        "company": "A",
        "invoiceId": "INV1001",
        "invoiceDate": "2025-03-15",
        "lines": [],
    }

    response = client.post("/invoice-record", json=invoice_data)

    # Check the file writing function was not called
    assert len(mock_append_output_to_jsonl_calls) == 0

    # Check the response
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert InvoiceEnum.INVOICE_LINES_EMPTY_MSSG in response.json()["detail"]


def test_api_unknown_company(mock_append_output_to_jsonl_calls):
    """Test that the API returns a 404 error when the company is unknown"""
    invoice_data = {
        "company": "Mock Wrong Company",
        "invoiceId": "INV1001",
        "invoiceDate": "2025-03-15",
        "lines": [
            {"description": "Mock Line 1", "amount": 100.0},
            {"description": "Mock Line 2", "amount": 200.0},
        ],
    }

    response = client.post("/invoice-record", json=invoice_data)

    # Check the file writing function was not called
    assert len(mock_append_output_to_jsonl_calls) == 0

    # Check the response
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert AppEnum.UNKNOWN_COMPANY_MSSG in response.json()["detail"]


def test_api_invoice_company_a_uses_strategy_a(mock_append_output_to_jsonl_calls):
    """Test that when called for company A, strategy A is used, returning a 201 status code"""
    invoice_data = {
        "company": "A",
        "invoiceId": "INV1001",
        "invoiceDate": "2025-03-15",
        "lines": [
            {"description": "Mock Line 1", "amount": 100.0},
            {"description": "Mock Line 2", "amount": 200.0},
        ],
    }

    # Call the endpoint
    response = client.post("/invoice-record", json=invoice_data)

    # Check the file writing function was called correctly
    assert len(mock_append_output_to_jsonl_calls) == 1
    assert mock_append_output_to_jsonl_calls[0]["company"] == "A"
    assert mock_append_output_to_jsonl_calls[0]["record_type"] == "invoice"

    # Check the response
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert "message" in response_data
    assert "data" in response_data


def test_api_vendor_company_b_uses_strategy_b(mock_append_output_to_jsonl_calls):
    """Test that when called for company B, strategy B is used, returning a 201 status code"""
    invoice_data = {
        "company": "B",
        "invoiceId": "INV1001",
        "invoiceDate": "2025-03-15",
        "lines": [
            {"description": "Mock Line 1", "amount": 100.0},
            {"description": "Mock Line 2", "amount": 200.0},
        ],
    }

    response = client.post("/invoice-record", json=invoice_data)

    # Check the file writing function was called correctly
    assert len(mock_append_output_to_jsonl_calls) == 1
    assert mock_append_output_to_jsonl_calls[0]["company"] == "B"
    assert mock_append_output_to_jsonl_calls[0]["record_type"] == "invoice"

    # Check the response
    assert response.status_code == status.HTTP_201_CREATED
    response_data = response.json()
    assert "message" in response_data
    assert "data" in response_data


def test_api_internal_server_error(monkeypatch):
    """Test that unexpected exceptions are converted to 500 errors and informs the client"""

    # Mock function that raises exception
    def mock_raise_exception(*args, **kwargs):
        raise Exception("Mocked Internal Server Error Exception")

    # Mock the function to raise the exception, use InvoiceStrategyA as an example
    monkeypatch.setattr(
        "app.services.invoice.InvoiceStrategyA.process_invoice", mock_raise_exception
    )

    # Call the endpoint with a valid request body for company A
    response = client.post(
        "/invoice-record",
        json={
            "company": "A",
            "invoiceId": "INV1001",
            "invoiceDate": "2025-03-15",
            "lines": [
                {"description": "Mock Line 1", "amount": 100.0},
                {"description": "Mock Line 2", "amount": 200.0},
            ],
        },
    )

    # Check the response
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "Mocked Internal Server Error Exception" in response.json()["detail"]

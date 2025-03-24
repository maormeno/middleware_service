import os
import pytest
import jsonlines
from app.utils.file_writer import append_output_to_jsonl


@pytest.fixture
def mock_jsonl_path(monkeypatch, tmp_path):
    """Fixture to create a temporary directory and redirect output there"""
    test_file = tmp_path / "test_output.jsonl"

    # Keep track of the original working directory
    original_dir = os.getcwd()

    # Change to the temporary directory
    os.chdir(tmp_path)

    # After the test completes
    yield test_file

    # Restore the original working directory
    os.chdir(original_dir)


def test_append_output_to_jsonl_fresh_file(mock_jsonl_path):
    """Test that data is correctly written to the JSONL file"""

    # Test function with test input data
    test_input = {
        "company": "Mock Company",
        "record_type": "vendor",
        "data": {
            "vendorName": "Mock Vendor",
            "country": "Mock Country",
            "bank": "Mock Bank",
        },
    }

    # Call the function
    append_output_to_jsonl(
        company=test_input["company"],
        record_type=test_input["record_type"],
        data=test_input["data"],
        output_file=mock_jsonl_path,  # Use mocked path
    )

    # Verify file exists
    assert mock_jsonl_path.exists()

    # Read back the file content to verify
    with jsonlines.open(mock_jsonl_path, mode="r") as f:
        records = list(f)

        # Should have one record
        assert len(records) == 1

        # Verify record content
        assert records[0]["company"] == test_input["company"]
        assert records[0]["record_type"] == test_input["record_type"]
        assert records[0]["data"] == test_input["data"]


def test_append_multiple_records(mock_jsonl_path):
    """Test that multiple records can be appended to the same JSONL file"""

    # First record
    test_input_1 = {
        "company": "Mock Company A",
        "record_type": "vendor",
        "data": {"mock_key": "mock_value"},
    }
    append_output_to_jsonl(
        company=test_input_1["company"],
        record_type=test_input_1["record_type"],
        data=test_input_1["data"],
        output_file=mock_jsonl_path,
    )

    # Second record
    test_input_2 = {
        "company": "Mock Company B",
        "record_type": "invoice",
        "data": {"mock_key": "mock_value"},
    }
    append_output_to_jsonl(
        company=test_input_2["company"],
        record_type=test_input_2["record_type"],
        data=test_input_2["data"],
        output_file=mock_jsonl_path,
    )

    # Verify file exists
    assert mock_jsonl_path.exists()

    # Read back the file content to verify
    with jsonlines.open(mock_jsonl_path, mode="r") as f:
        records = list(f)

        # Should have two records
        assert len(records) == 2

        # First record
        assert records[0]["company"] == test_input_1["company"]
        assert records[0]["record_type"] == test_input_1["record_type"]
        assert records[0]["data"] == test_input_1["data"]

        # Second record
        assert records[1]["company"] == test_input_2["company"]
        assert records[1]["record_type"] == test_input_2["record_type"]
        assert records[1]["data"] == test_input_2["data"]

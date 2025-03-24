 Middleware Integration Service

A middleware service that normalizes vendor and invoice data from different companies into a standardized format, applying company-specific business logic.

## Features

- Vendor and invoice data normalization with company-specific validation rules
- REST API endpoints `/vendor-record` and `/invoice-record`
- Standardized JSON output format with persistent storage of transformed data in a JSONL file
- Input samples with a ready-to-use testing client
- Thoroughly documented endpoints, classes, methods, and functions
- Comprehensive error handling
- Unit test battery with 100% coverage

## Running the middleware service

### Prerequisites

- Python 3.8+
- FastAPI
- uvicorn
- pytest (for running tests)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/maormeno/middleware_service
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Service

Start the middleware service locally in your terminal:
```bash
cd app
fastapi dev main.py
```

The service will be available at `http://127.0.0.1:8000/`

### Testing the service

The `/vendor-record` and `/invoice-record` endpoints can be tested by sending HTTP requests to where the service is running using Postman.

However, a demo is provided in the [`/demo/`](https://github.com/maormeno/middleware_service/tree/main/demo) folder, where you can find a [`demo_client.py`](https://github.com/maormeno/middleware_service/blob/main/demo/demo_client.py) script, along with several input samples for each endpoint in json format.
To try them, just uncomment one of the `ENDPOINT` values together with one of their corresponding `SAMPLE_FILE`. A description of each input is provided on an inline comment, and you can check its content by opening the correpsonding file. By default, the `vendor` service is used with the first input file:

```python
    # VENDOR:
    ENDPOINT = "vendor-record"
    SAMPLE_FILE = "a_1.json"  # COMPANY A, INTERNATIONAL VENDOR
    # SAMPLE_FILE = "a_2.json" # COMPANY A, LOCAL VENDOR
    # SAMPLE_FILE = "b_1.json" # COMPANY B, LOCAL VENDOR, MISSING DETAILS
    # SAMPLE_FILE = "b_2.json" # COMPANY B, LOCAL VENDOR, COMPLETE DETAILS
    # SAMPLE_FILE = "error_unknown_company.json" # UNKNOWN COMPANY C
    # SAMPLE_FILE = "error_missing_fields.json" # MISSING FIELDS

    # INVOICE
    # ENDPOINT = "invoice-record"
    # SAMPLE_FILE = "a_1.json" # COMPANY A, ALCOHOL INVOICE
    # SAMPLE_FILE = "a_2.json" # COMPANY A, NO ALCOHOL INVOICE
    # SAMPLE_FILE = "b_1.json" # COMPANY B, ALCOHOL INVOICE
    # SAMPLE_FILE = "b_2.json" # COMPANY B, TOBACCO INVOICE
    # SAMPLE_FILE = "b_3.json" # COMPANY B, BOTH INVOICE
    # SAMPLE_FILE = "b_4.json" # COMPANY B, NO SPECIAL KEYWORDS INVOICE
    # SAMPLE_FILE = "error_missing_lines.json" # MISSING INVOICE LINES
```

Then, the script can be run simply with:
```bash
python input_samples/client.py
```

The response is printed to the terminal for a quick look, but, as required, all the outputs will be saved, given they are correct, in the file `output.jsonl` at the root of the project in a standardized format.

### Unit Tests

A suite of unit tests with 100% coverage is provided in the `/tests/` folder, where you can take a look and check all the edge cases and expected behaviors of the different components. You can run it from the root of the project:

```bash
pytest
```

(For reference [])


## API Endpoints
The API exposes two endpoints, each with minimum required fields that are validated upon reception.

### 1. Vendor Endpoint
POST /vendor-record

Sample request, with the minimum required fields:
```json
{
    "company": "A",
    "vendorName": "Global Supplies Ltd.",
    "country": "FR",
    "bank": "Bank X"
}
```

### 2. Invoice Endpoint
POST /invoice-record

Sample request, with the minimum required fields:
```json
{
    "company": "A",
    "invoiceId": "INV1001",
    "invoiceDate": "2025-03-15",
    "lines": [
        {"description": "Office supplies", "amount": 150.00},
        {"description": "Beverages - alcohol", "amount": 200.00}
    ]
}
```

### Errors

The service implements the main status codes for errors:
- 422 "Unprocessable entity" when the request is missing required fields
- 404 "Not found" if the company included in the request does not have a valid implementation
- 500 "Internal server error" when there was an exception raised by the endpoint on the server end (this is only simulated on the tests as there were no internal server errors when testing the samples).

When the request was successfully processed, transformed, and written to the output, it returns status code 201 "created".

## Business Logic

For the business logic, a particularity worth mentioning is the use of the [Strategy](https://refactoring.guru/design-patterns/strategy) behavioral design pattern to separate the company-specific logics and specific rules. Although there are only two companies (thus, strategies) at the moment, this sets the bases to maintain a growing codebase with more complex and particular logic brought by new companies.

The particular business logic for each company and connection point is as follows, assuming valid request schemas:

### Vendor Processing

#### Company A
- International vendors (non-US) receive an additional `internationalBank` field with a verification message
- All other vendor fields are passed through as-is

#### Company B
- US vendors are validated for the presence of `registrationNumber` and `taxId`
- Assigns `vendorStatus` to `"Verified"` when both are present, or `"Incomplete - missing registration/tax details"` if one or both of them are missing
- Non-US vendors are passed as is, without adding a `vendorStatus`

### Invoice Processing

#### Company A
- Checks for `"alcohol"` keyword in line items (case-insensitive)
- Assigns `account` codes:
  - `ALC-001`: If `alcohol` is present in some line
  - `STD-001`: If `alcohol` isn't present

#### Company B
- Checks for both `"alcohol"` and `"tobacco"` keywords
- Assigns `account` codes:
  - `ALC-B`: If `alcohol` is present but not `tobacco`
  - `TOB-B`: If `tobacco` is present but not `alcohol`
  - `MULTI-B`: If both `alcohol` and `tobacco` are present
  - `STD-B`: If neither is present

## Output Format

The service writes each transformed record from both types as new line-delimited JSON entry in a JSONL file named `output.jsonl` in the root directory, in the format:

```json
{
    "company": "", // Name of the company
    "record_type": "", // `vendor` or `invoice`
    "data": {...} // The data after transformation
}
```

### Sample Output Format

```jsonl
{"company": "B", "record_type": "vendor", "data": {"vendorName": "Local Goods Inc.", "country": "US", "bank": "Local Bank Y", "vendorStatus": "Incomplete - missing registration/tax details"}}
{"company": "A", "record_type": "invoice", "data": {"invoiceId": "INV1001", "invoiceDate": "2025-03-15", "account": "ALC-001", "lines": [{"description": "Office supplies", "amount": 150.0}, {"description": "Beverages - alcohol", "amount": 200.0}]}}
{"company": "B", "record_type": "vendor", "data": {"vendorName": "Trusted Suppliers LLC", "country": "US", "bank": "Local Bank Z", "vendorStatus": "Verified"}}
{"company": "A", "record_type": "invoice", "data": {"invoiceId": "INV1002", "invoiceDate": "2025-03-16", "account": "STD-001", "lines": [{"description": "Office supplies", "amount": 100.0}, {"description": "Cleaning services", "amount": 75.0}]}}
```
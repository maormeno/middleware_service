"""Sample requests to the middleware_service"""

from httpx import Client
import os
import json


def main():
    # Uncomment one endpoint and sample file

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

    client = Client()
    url = f"http://127.0.0.1:8000/{ENDPOINT}"

    # Pick the input file to test
    input_dir = os.path.abspath(os.path.dirname(__file__))
    with open(f"{input_dir}/{ENDPOINT.split('-')[0]}/{SAMPLE_FILE}", "r") as f:
        data = json.load(f)
        print("-" * 100)
        print("INPUT DATA:")
        print(data)

    response = client.post(url, json=data)
    print("\n")
    print(response)
    print(response.json())
    print("-" * 100)


if __name__ == "__main__":
    main()

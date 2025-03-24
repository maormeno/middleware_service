from enum import Enum


class AppEnum(str, Enum):
    """Enums for persistent string values related to the application"""

    ROOT_ENDPOINT_MSSG = "Middleware service is running."
    MISSING_REQUIRED_FIELDS_MSSG = "Missing required fields"
    UNKNOWN_COMPANY_MSSG = "Unknown company"


class VendorEnum(str, Enum):
    """Enums for persistent string values related to vendor"""

    CONFIRM_INTERNATIONAL_BANK_MSSG = "Please confirm international bank details"
    STATUS_VERIFIED = "Verified"
    STATUS_INCOMPLETE = "Incomplete - missing registration/tax details"
    VENDOR_RECORD_PROCESSED_MSSG = "Vendor record processed successfully for company: "


class InvoiceEnum(str, Enum):
    """Enums for persistent string values related to invoice"""

    ACCOUNT_ALC_001 = "ALC-001"
    ACCOUNT_STD_001 = "STD-001"
    ACCOUNT_ALC_B = "ALC-B"
    ACCOUNT_TOB_B = "TOB-B"
    ACCOUNT_MULTI_B = "MULTI-B"
    ACCOUNT_STD_B = "STD-B"
    INVOICE_RECORD_PROCESSED_MSSG = (
        "Invoice record processed successfully for company: "
    )
    INVOICE_LINES_EMPTY_MSSG = "Invoice must have at least one line"

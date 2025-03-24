from pydantic import BaseModel
from typing import Literal, LiteralString, Optional

from app.enums import VendorEnum


class InvoiceLine(BaseModel):
    description: str
    amount: float


class InvoiceInputBody(BaseModel):
    """Model for the /invoice-record endpoint body"""

    # Continue here (finish the model, endpoint, and service for invoice records)
    company: str  # "A", "B"
    invoiceId: str
    invoiceDate: str
    lines: list[InvoiceLine]
    other_details: Optional[dict] = None


class InvoiceOutput(BaseModel):
    """Generic parent model for processed invoice outputs from the corresponding endpoint."""

    invoiceId: str
    invoiceDate: str
    account: str
    lines: list[InvoiceLine]

from pydantic import BaseModel
from typing import Literal, LiteralString, Optional

from app.enums import VendorEnum


class VendorInputBody(BaseModel):
    """Model for the /vendor-record endpoint body"""

    company: str  # "A", "B"
    vendorName: str  # "Vendor A", "Vendor B"
    country: str  # In ISO country code format, e.g. "US", "FR"
    bank: str  # "Bank A", "Bank B"
    registrationNumber: Optional[str] = None
    taxId: Optional[str] = None
    other_details: Optional[dict] = None  # Additional details about the vendor


class _VendorOutput(BaseModel):
    """Generic parent model for processed vendor outputs from the corresponding endpoint."""

    vendorName: str
    country: str
    bank: str


class VendorOutputA(_VendorOutput):
    """Model for processed vendor output records for Company A."""

    internationalBank: Optional[Literal[VendorEnum.CONFIRM_INTERNATIONAL_BANK_MSSG]] = (
        None
    )


class VendorOutputB(_VendorOutput):
    """Model for processed vendor output records for Company B."""

    vendorStatus: Optional[
        Literal[
            VendorEnum.STATUS_INCOMPLETE,
            VendorEnum.STATUS_VERIFIED,
        ]
    ]

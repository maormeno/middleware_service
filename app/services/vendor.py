"""Vendor service that implements the company-specific rules through a strategy pattern."""

from abc import ABC, abstractmethod

from app.models.vendor import (
    VendorInputBody,
    VendorOutputA,
    VendorOutputB,
)
from app.enums import VendorEnum


class VendorAbstractStrategy(ABC):
    """Abstract base class for vendor service strategies"""

    @classmethod
    @abstractmethod
    def process_vendor(cls, vendor: VendorInputBody) -> VendorOutputA | VendorOutputB:
        """Check specific fields according to company rules"""
        pass  # pragma: no cover (skip coverage in tests)


class VendorStrategyA(VendorAbstractStrategy):
    """Strategy for company A"""

    @classmethod
    def process_vendor(cls, vendor: VendorInputBody) -> VendorOutputA:
        """Check specific fields according to company A rules"""
        return VendorOutputA(
            vendorName=vendor.vendorName,
            country=vendor.country,
            bank=vendor.bank,
            # Only add internationalBank if country is not local (US)
            internationalBank=(
                VendorEnum.CONFIRM_INTERNATIONAL_BANK_MSSG
                if vendor.country != "US"
                else None
            ),
        )


class VendorStrategyB(VendorAbstractStrategy):
    """Strategy for company B"""

    @classmethod
    def process_vendor(cls, vendor: VendorInputBody) -> VendorOutputB:
        """Check specific fields according to company B rules"""
        if vendor.country == "US":
            if vendor.registrationNumber and vendor.taxId:
                vendor_status = VendorEnum.STATUS_VERIFIED
            else:
                vendor_status = VendorEnum.STATUS_INCOMPLETE
        else:
            # RE-CHECK: I'm assuming that non-US vendors don't need verification, therefore no vendor status?
            vendor_status = None

        return VendorOutputB(
            vendorName=vendor.vendorName,
            country=vendor.country,
            bank=vendor.bank,
            vendorStatus=vendor_status,
        )

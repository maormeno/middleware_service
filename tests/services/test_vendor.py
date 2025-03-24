import pytest

from app.models.vendor import VendorInputBody, VendorOutputA, VendorOutputB
from app.services.vendor import VendorStrategyA, VendorStrategyB
from app.enums import VendorEnum


class TestVendorStrategyA:
    """Test class for vendor strategy A"""

    def test_vendor_strategy_A_returns_correct_type(self):
        """Test that VendorStrategyA always returns a VendorOutputA instance"""
        vendor_input = VendorInputBody(
            company="A",
            vendorName="Mock Vendor",
            country="Mock Country",
            bank="Mock Bank",
        )
        result = VendorStrategyA.process_vendor(vendor_input)
        assert isinstance(result, VendorOutputA)

    def _verify_core_fields(self, result, vendor_input):
        """Helper method to verify core fields"""
        assert result.vendorName == vendor_input.vendorName
        assert result.country == vendor_input.country
        assert result.bank == vendor_input.bank

    def test_vendor_strategy_A_international_vendor(self):
        """Test that the international vendor strategy returns confirmation message"""
        # Test input
        vendor_input = VendorInputBody(
            company="A",
            vendorName="Global Supplies Ltd.",
            country="FR",  # non-US
            bank="Bank X",
        )

        # Call the strategy
        result = VendorStrategyA.process_vendor(vendor_input)

        # Verify core fields
        self._verify_core_fields(result, vendor_input)

        # Assert the internationalBank is correct
        assert result.internationalBank == VendorEnum.CONFIRM_INTERNATIONAL_BANK_MSSG

    def test_vendor_strategy_A_non_international_vendor(self):
        """Test that the non-international vendor strategy returns no internationalBank message"""
        # Test input
        vendor_input = VendorInputBody(
            company="A",
            vendorName="Global Supplies Ltd.",
            country="US",  # local US
            bank="Bank X",
        )

        # Call the strategy
        result = VendorStrategyA.process_vendor(vendor_input)

        # Verify core fields
        self._verify_core_fields(result, vendor_input)

        # Assert the internationalBank is correct
        assert result.internationalBank is None


class TestVendorStrategyB:
    """Test class for vendor strategy B"""

    def test_vendor_strategy_B_returns_correct_type(self):
        """Test that VendorStrategyB returns a VendorOutputB instance"""
        vendor_input = VendorInputBody(
            company="B",
            vendorName="Mock Vendor",
            country="Mock Country",
            bank="Mock Bank",
        )
        result = VendorStrategyB.process_vendor(vendor_input)
        assert isinstance(result, VendorOutputB)

    def _verify_core_fields(self, result, vendor_input):
        """Helper method to verify core fields"""
        assert result.vendorName == vendor_input.vendorName
        assert result.country == vendor_input.country
        assert result.bank == vendor_input.bank

    def test_vendor_strategy_B_local_vendor_missing_registration_number_and_tax_id(
        self,
    ):
        """Test that a US vendor missing both registrationNumber and taxId returns incomplete status"""
        # Test input
        vendor_input = VendorInputBody(
            company="B",
            vendorName="Local Goods Inc.",
            country="US",
            bank="Local Bank Y",
        )

        # Call the strategy
        result = VendorStrategyB.process_vendor(vendor_input)

        # Verify core fields
        self._verify_core_fields(result, vendor_input)

        # Assert the vendorStatus is correct
        assert result.vendorStatus == VendorEnum.STATUS_INCOMPLETE

    def test_vendor_strategy_B_local_vendor_missing_registration_number(self):
        """Test that a US vendor missing only registrationNumber returns incomplete status"""
        # Test input
        vendor_input = VendorInputBody(
            company="B",
            vendorName="Local Goods Inc.",
            country="US",
            bank="Local Bank Y",
            taxId="Mock-Tax-ID-01",
        )

        # Call the strategy
        result = VendorStrategyB.process_vendor(vendor_input)

        # Verify core fields
        self._verify_core_fields(result, vendor_input)

        # Assert the vendorStatus is correct
        assert result.vendorStatus == VendorEnum.STATUS_INCOMPLETE

    def test_vendor_strategy_B_local_vendor_missing_tax_id(self):
        """Test that a US vendor missing only taxId returns incomplete status"""
        # Test input
        vendor_input = VendorInputBody(
            company="B",
            vendorName="Mock Vendor",
            country="US",
            bank="Mock Bank",
            registrationNumber="Mock-Registration-Number-01",
        )

        # Call the strategy
        result = VendorStrategyB.process_vendor(vendor_input)

        # Verify core fields
        self._verify_core_fields(result, vendor_input)

        # Assert the vendorStatus is correct
        assert result.vendorStatus == VendorEnum.STATUS_INCOMPLETE

    def test_vendor_strategy_B_local_vendor_complete_details(self):
        """Test that a US vendor with complete details returns verified status"""
        # Test input
        vendor_input = VendorInputBody(
            company="B",
            vendorName="Trusted Suppliers LLC",
            country="US",
            bank="Local Bank Z",
            registrationNumber="REG12345",
            taxId="TAX67890",
        )

        # Call the strategy
        result = VendorStrategyB.process_vendor(vendor_input)

        # Verify core fields
        self._verify_core_fields(result, vendor_input)

        # Assert the vendorStatus is correct
        assert result.vendorStatus == VendorEnum.STATUS_VERIFIED

    def test_vendor_strategy_B_non_local_vendor(
        self,
    ):
        """Test that a non-US vendor returns no vendorStatus"""
        # Test input
        vendor_input = VendorInputBody(
            company="B",
            vendorName="Mock Vendor",
            country="Non-US",
            bank="Mock Bank",
        )

        # Call the strategy
        result = VendorStrategyB.process_vendor(vendor_input)

        # Verify core fields
        self._verify_core_fields(result, vendor_input)

        # Assert the vendorStatus is correct
        assert result.vendorStatus is None

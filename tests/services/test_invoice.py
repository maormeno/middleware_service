import pytest

from app.models.invoice import InvoiceInputBody, InvoiceLine, InvoiceOutput
from app.services.invoice import InvoiceStrategyA, InvoiceStrategyB
from app.enums import InvoiceEnum


class TestInvoiceStrategyA:
    """Test class for invoice strategy A"""

    def _verify_core_fields(self, result, invoice_input):
        """Helper method to verify core fields"""
        assert result.invoiceId == invoice_input.invoiceId
        assert result.invoiceDate == invoice_input.invoiceDate
        assert result.lines == invoice_input.lines

    def test_invoice_company_A_alcohol_line(self):
        """Test that InvoiceStrategyA returns the correct account for an alcohol line, case insensitive"""
        invoice_input = InvoiceInputBody(
            company="A",
            invoiceId="INV1001",
            invoiceDate="2025-03-15",
            lines=[
                InvoiceLine(description="Office supplies", amount=150.0),
                InvoiceLine(description="Beverages - alcohol", amount=200.0),
            ],
        )

        # lowercase
        result = InvoiceStrategyA.process_invoice(invoice_input)
        self._verify_core_fields(result, invoice_input)
        assert result.account == InvoiceEnum.ACCOUNT_ALC_001

        # uppercase
        invoice_input.lines = [
            InvoiceLine(description="Office supplies", amount=150.0),
            InvoiceLine(description="Beverages - Alcohol", amount=200.0),
        ]
        result = InvoiceStrategyA.process_invoice(invoice_input)
        assert result.account == InvoiceEnum.ACCOUNT_ALC_001

    def test_invoice_company_A_no_alcohol_line(self):
        """Test that InvoiceStrategyA returns the correct account for a non-alcohol line"""
        invoice_input = InvoiceInputBody(
            company="A",
            invoiceId="INV1002",
            invoiceDate="2025-03-16",
            lines=[
                InvoiceLine(description="Office supplies", amount=100.0),
                InvoiceLine(description="Cleaning services", amount=75.0),
            ],
        )

        result = InvoiceStrategyA.process_invoice(invoice_input)
        self._verify_core_fields(result, invoice_input)
        assert result.account == InvoiceEnum.ACCOUNT_STD_001


class TestInvoiceStrategyB:
    """Test class for invoice strategy B"""

    def _verify_core_fields(self, result, invoice_input):
        """Helper method to verify core fields"""
        assert result.invoiceId == invoice_input.invoiceId
        assert result.invoiceDate == invoice_input.invoiceDate
        assert result.lines == invoice_input.lines

    def test_invoice_company_B_alcohol(self):
        """Test that InvoiceStrategyB returns the correct account for an alcohol"""

        invoice_input = InvoiceInputBody(
            company="B",
            invoiceId="INV2001",
            invoiceDate="2025-03-17",
            lines=[
                InvoiceLine(description="Alcohol beverages", amount=300.0),
                InvoiceLine(description="Stationery", amount=50.0),
            ],
        )

        result = InvoiceStrategyB.process_invoice(invoice_input)
        self._verify_core_fields(result, invoice_input)
        assert result.account == InvoiceEnum.ACCOUNT_ALC_B

    def test_invoice_company_B_tabacco(self):
        """Test that InvoiceStrategyB returns the correct account for an tabacco"""

        invoice_input = InvoiceInputBody(
            company="B",
            invoiceId="INV2002",
            invoiceDate="2025-03-18",
            lines=[
                InvoiceLine(description="Tobacco products", amount=400.0),
                InvoiceLine(description="Miscellaneous", amount=80.0),
            ],
        )

        result = InvoiceStrategyB.process_invoice(invoice_input)
        self._verify_core_fields(result, invoice_input)
        assert result.account == InvoiceEnum.ACCOUNT_TOB_B

    def test_invoice_company_B_alcohol_and_tabacco(self):
        """Test that InvoiceStrategyB returns the correct account for an alcohol and tabacco"""

        invoice_input = InvoiceInputBody(
            company="B",
            invoiceId="INV2003",
            invoiceDate="2025-03-19",
            lines=[
                InvoiceLine(description="Alcohol beverages", amount=150.0),
                InvoiceLine(description="Tobacco products", amount=200.0),
            ],
        )

        result = InvoiceStrategyB.process_invoice(invoice_input)
        self._verify_core_fields(result, invoice_input)
        assert result.account == InvoiceEnum.ACCOUNT_MULTI_B

    def test_invoice_company_B_no_special_keyword(self):
        """Test that InvoiceStrategyB returns the correct account for a line without a special keyword"""

        invoice_input = InvoiceInputBody(
            company="B",
            invoiceId="INV2004",
            invoiceDate="2025-03-20",
            lines=[
                InvoiceLine(description="Office supplies", amount=90.0),
                InvoiceLine(description="Cleaning services", amount=60.0),
            ],
        )

        result = InvoiceStrategyB.process_invoice(invoice_input)
        self._verify_core_fields(result, invoice_input)
        assert result.account == InvoiceEnum.ACCOUNT_STD_B

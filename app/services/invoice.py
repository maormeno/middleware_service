"""Invoice service that implements the company-specific rules through a strategy pattern."""

from abc import ABC, abstractmethod

from app.models.invoice import (
    InvoiceInputBody,
    InvoiceOutput,
)
from app.enums import InvoiceEnum


class InvoiceAbstractStrategy(ABC):
    """Abstract base class for invoice service strategies"""

    @classmethod
    @abstractmethod
    def process_invoice(cls, invoice: InvoiceInputBody) -> InvoiceOutput:
        """Check specific fields according to company rules"""
        pass  # pragma: no cover (skip coverage in tests)


class InvoiceStrategyA(InvoiceAbstractStrategy):
    """Strategy for company A"""

    @classmethod
    def process_invoice(cls, invoice: InvoiceInputBody) -> InvoiceOutput:
        """Check specific fields according to company A rules"""

        lines = invoice.lines

        invoice_account = InvoiceEnum.ACCOUNT_STD_001

        for line in lines:
            if "alcohol" in line.description.lower():
                invoice_account = InvoiceEnum.ACCOUNT_ALC_001

        return InvoiceOutput(
            invoiceId=invoice.invoiceId,
            invoiceDate=invoice.invoiceDate,
            account=invoice_account,
            lines=invoice.lines,
        )


class InvoiceStrategyB(InvoiceAbstractStrategy):
    """Strategy for company B"""

    @classmethod
    def process_invoice(cls, invoice: InvoiceInputBody) -> InvoiceOutput:
        """Check specific fields according to company B rules"""

        lines = invoice.lines

        alcohol_account = False
        tobacco_account = False

        for line in lines:
            if "alcohol" in line.description.lower():
                alcohol_account = True
            if "tobacco" in line.description.lower():
                tobacco_account = True

        if alcohol_account and tobacco_account:
            account = InvoiceEnum.ACCOUNT_MULTI_B
        elif alcohol_account:
            account = InvoiceEnum.ACCOUNT_ALC_B
        elif tobacco_account:
            account = InvoiceEnum.ACCOUNT_TOB_B
        else:
            account = InvoiceEnum.ACCOUNT_STD_B

        return InvoiceOutput(
            invoiceId=invoice.invoiceId,
            invoiceDate=invoice.invoiceDate,
            account=account,
            lines=invoice.lines,
        )

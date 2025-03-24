"""
Entrypoint for the middleware service API.
"""

from collections import defaultdict

from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.models.vendor import VendorInputBody
from app.services.vendor import VendorStrategyA, VendorStrategyB

from app.models.invoice import InvoiceInputBody
from app.services.invoice import InvoiceStrategyA, InvoiceStrategyB

from app.utils.file_writer import append_output_to_jsonl
from app.enums import AppEnum, InvoiceEnum, VendorEnum

app = FastAPI(
    title="Vendor and Invoice Record Processing Middleware Service",
    description="A service that processes and normalizes vendor and invoice records according to their company-specific requirements",
)


# From https://stackoverflow.com/questions/58642528/displaying-of-fastapi-validation-errors-to-end-users @Dariosky
@app.exception_handler(RequestValidationError)
async def custom_form_validation_error(request, exc):
    """Override validation exceptions reformatting the response to be more user-friendly"""
    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(filtered_loc)  # nested fields with dot-notation
        reformatted_message[field_string].append(msg)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder(
            {
                "detail": AppEnum.MISSING_REQUIRED_FIELDS_MSSG,
                "errors": reformatted_message,
            }
        ),
    )


@app.get("/")
def root():
    return {"message": AppEnum.ROOT_ENDPOINT_MSSG}


@app.post("/vendor-record")
def process_vendor_record(vendor_input: VendorInputBody):
    """Endpoint to process vendor records"""
    try:
        # Process the vendor record depending on the company
        if vendor_input.company == "A":
            vendor_output = VendorStrategyA.process_vendor(vendor_input)
        elif vendor_input.company == "B":
            vendor_output = VendorStrategyB.process_vendor(vendor_input)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=AppEnum.UNKNOWN_COMPANY_MSSG,
            )

        append_output_to_jsonl(
            vendor_input.company, "vendor", vendor_output.model_dump()
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": (
                    f"{VendorEnum.VENDOR_RECORD_PROCESSED_MSSG.value} '{vendor_input.company}'"
                ),
                "data": vendor_output.model_dump(),
            },
        )

    except HTTPException as e:
        # Continue with the raised exception as is
        raise e

    except Exception as e:
        # If an exception is raised that is not an HTTPException, raise a 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@app.post("/invoice-record")
def process_invoice_record(invoice_input: InvoiceInputBody):
    """Endpoint to process invoice records"""
    try:
        if len(invoice_input.lines) == 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=InvoiceEnum.INVOICE_LINES_EMPTY_MSSG,
            )

        # Process the invoice record depending on the company
        if invoice_input.company == "A":
            invoice_output = InvoiceStrategyA.process_invoice(invoice_input)
        elif invoice_input.company == "B":
            invoice_output = InvoiceStrategyB.process_invoice(invoice_input)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=AppEnum.UNKNOWN_COMPANY_MSSG,
            )

        append_output_to_jsonl(
            invoice_input.company, "invoice", invoice_output.model_dump()
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": (
                    f"{InvoiceEnum.INVOICE_RECORD_PROCESSED_MSSG.value} '{invoice_input.company}'"
                ),
                "data": invoice_output.model_dump(),
            },
        )

    except HTTPException as e:
        # Continue with the raised exception as is
        raise e

    except Exception as e:
        # If an exception is raised that is not an HTTPException, raise a 500 error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )

from typing import Literal
from jsonlines import jsonlines

from app.settings import OUTPUT_FILE


def append_output_to_jsonl(
    company: str,
    record_type: Literal["vendor", "invoice"],
    data: dict,
    output_file: str = OUTPUT_FILE,
) -> None:
    """
    Append a dictionary to a JSONL file.
    """
    new_json = {"company": company, "record_type": record_type, "data": data}

    with jsonlines.open(output_file, mode="a") as f:
        f.write(new_json)

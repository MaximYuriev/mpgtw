from dataclasses import dataclass


@dataclass
class HttpResponseDTO:
    detail: str
    data: list[dict] | dict | None = None

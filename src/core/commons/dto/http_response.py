from dataclasses import dataclass


@dataclass
class HttpResponseDTO:
    detail: str
    data: dict | None = None

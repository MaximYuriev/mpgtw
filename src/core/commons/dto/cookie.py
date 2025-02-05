from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class CookieDTO:
    key: str
    value: str

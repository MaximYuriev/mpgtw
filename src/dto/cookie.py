from dataclasses import dataclass, field

from config import COOKIE_KEY_NAME


@dataclass(frozen=True, eq=False)
class CookieDTO:
    key: str = field(default=COOKIE_KEY_NAME, kw_only=True)
    value: str

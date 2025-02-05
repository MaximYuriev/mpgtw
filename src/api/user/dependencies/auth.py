from typing import Annotated

from fastapi import Depends

from authorizer.config import authorizer_config
from authorizer.http.dependencies import get_token_from_cookie
from src.core.commons.dto.cookie import CookieDTO


def get_auth_cookie(
        token: Annotated[str, Depends(get_token_from_cookie)]
) -> CookieDTO:
    return CookieDTO(
        key=authorizer_config.cookie.name,
        value=token
    )

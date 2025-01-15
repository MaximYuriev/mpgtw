from fastapi import HTTPException, status


class HTTPLoginIsNotUniqueException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )

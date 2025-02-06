from src.core.commons.dto.http_response import HttpResponseDTO
from src.core.commons.exceptions.sender import HttpSenderValidateException


class BaseHttpSender:
    @staticmethod
    def _validate_responses(response_body: dict) -> HttpResponseDTO:
        try:
            return HttpResponseDTO(**response_body)
        except TypeError:
            raise HttpSenderValidateException

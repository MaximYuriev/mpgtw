import jwt

from config import PRIVATE_KEY_PATH, PUBLIC_KEY_PATH
from .payloads import BasePayload


class JWT:
    _CRYPT_ALGORITHM = 'RS256'

    @staticmethod
    def create_jwt(
            payload: BasePayload,
            private_key: str = PRIVATE_KEY_PATH.read_text(),
            algorithm: str = _CRYPT_ALGORITHM,
    ):
        token_data = payload.__dict__
        return jwt.encode(token_data, private_key, algorithm=algorithm)

    @staticmethod
    def parse_jwt(
            token: str,
            public_key: str = PUBLIC_KEY_PATH.read_text(),
            algorithm: str = _CRYPT_ALGORITHM,
            verify_signature: bool = True
    ):
        return jwt.decode(token, public_key, algorithms=[algorithm], options={"verify_signature": verify_signature})

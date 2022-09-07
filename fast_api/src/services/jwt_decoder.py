from http import HTTPStatus
from typing import Dict, Union, Any

import jwt

from core.config import settings


def jwt_decoder(token: str) -> Union[Dict, Any]:
    try:
        jwt_settings = settings.jwt_settings
        decode_token = jwt.decode(jwt=token, key=jwt_settings.JWT_SECRET_KEY,
                                  algorithms=jwt_settings.JWT_ALGORITHM)
        return decode_token
    except jwt.ExpiredSignatureError:
        # Signature has expired
        return HTTPStatus.UNAUTHORIZED

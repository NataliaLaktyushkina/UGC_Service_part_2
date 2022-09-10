import http
from datetime import datetime
from typing import Union, Optional, Any

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError

from .jwt_decoder import jwt_decoder


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Union[list[str], Optional[Any]]:  # type: ignore
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request=request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail="Invalid authentication scheme.")
            if not self.verify_jwt(jwtoken=credentials.credentials):
                raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail="Invalid token or expired token.")
            return jwt_decoder(token=credentials.credentials).get("user_id")

        raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail="Invalid authorization code.")

    @staticmethod
    def verify_jwt(jwtoken: str) -> bool:
        try:
            payload: dict = jwt_decoder(jwtoken)
            expire_time: int = payload.get("exp")  # type: ignore
            current_time: int = int(datetime.now().timestamp())
        except InvalidTokenError:
            return False
        return expire_time > current_time

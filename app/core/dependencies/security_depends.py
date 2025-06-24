from typing import Annotated
from fastapi import Depends

from app.core.security.jwt_handler import JwtHandler
from app.core.security.password_hasher import PasswordHasher


_jwt_handler_instance = JwtHandler()

def _get_jwt_handler() -> JwtHandler:
    return _jwt_handler_instance


JWTHandlerDependency = Annotated[JwtHandler, Depends(dependency=_get_jwt_handler)]


def _get_pass_hasher() -> PasswordHasher:
    return PasswordHasher()

PasswordHasherDependency = Annotated[PasswordHasher, Depends(_get_pass_hasher)]

async def get_token_payload(
    token: Annotated[str, Depends(dependency=_jwt_handler_instance.oauth_scheme)],
    jwt_handler: JWTHandlerDependency
) -> dict:
    return jwt_handler.decode_access_token(token=token)

AccessTokenDependency = Annotated[dict, Depends(get_token_payload)]

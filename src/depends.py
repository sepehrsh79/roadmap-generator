from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.controllers.auth import AuthController
from src.core.database import DBManager, get_db
from src.core.exceptions import ForbiddenException
from src.repository.jwt import JWTHandler
from src.schema.auth import RefreshToken

http_bearer = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    # Check if the authorization scheme is 'Bearer'
    if credentials.scheme != "Bearer":
        raise ForbiddenException("Invalid Header")

    # Decode the refresh token from the Authorization header
    access_token = credentials.credentials
    if not access_token:
        raise ForbiddenException("Access-Token is not provided")

    # Decode the refresh token
    token = JWTHandler.decode(access_token)
    user_id = token.get("user_id")

    # Ensure the token contains the user_id
    if not user_id:
        raise ForbiddenException("Invalid Access Token")

    return user_id


async def get_current_user_with_refresh(request_data: RefreshToken):
    # Extract and decode the refresh token from the request body
    refresh_token = request_data.refresh_token
    if not refresh_token:
        raise ForbiddenException("Refresh token not provided")

    # Decode and verify the refresh token
    refresh_token_data = JWTHandler.decode(refresh_token)
    user_id = refresh_token_data.get("verify")

    # Ensure the token contains the user_id or relevant information
    if not user_id:
        raise ForbiddenException("Invalid Refresh Token")

    # Return the user_id or authenticated user data
    return user_id


async def get_current_user_from_db(
    db_session: DBManager = Depends(get_db), user_id: str = Depends(get_current_user)
):
    return await AuthController(db_session).me(user_id)

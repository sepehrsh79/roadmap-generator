import asyncio
import base64
import io

import qrcode
from pyotp import random_base32, totp

from src.core.config import settings

from src.core.database import DBManager
from src.core.exceptions import (
    BadRequestException,
    CustomException,
    UnauthorizedException,
)
from src.core.redis.client import RedisManager
from src.repository.jwt import JWTHandler
from src.repository.password import PasswordHandler
from src.crud.users import UserCRUD
from src.schema.auth import Token
from src.schema.user import UserOut, UserOutRegister


class AuthController:
    user_crud = UserCRUD()
    password_handler = PasswordHandler
    jwt_handler = JWTHandler

    def __init__(
        self,
        db_session: DBManager,
        redis_session: RedisManager | None = None,
        user_crud: UserCRUD | None = None,
    ):
        self.user_crud = user_crud or self.user_crud
        self.db_session = db_session
        self.redis_session = redis_session

    async def register(self, password: str, username: str) -> UserOutRegister:
        user = await self.user_crud.get_by_username(
            self.db_session,
            username=username,
        )

        if user:
            raise BadRequestException("User already exists with this username")

        password = self.password_handler.hash(password)
        user = await self.user_crud.create(
            db_session=self.db_session,
            username=username,
            password=password,
            gauth=str(random_base32()),
        )

        assert user is not None
        provisioning_uri = totp.TOTP(user.gauth).provisioning_uri()
        buffered = io.BytesIO()
        qrcode.make(provisioning_uri).save(buffered)
        return UserOutRegister(
            username=user.username,
            updated_at=user.updated_at,
            created_at=user.created_at,
            gauth=user.gauth,
            qr_img=base64.b64encode(buffered.getvalue()).decode(),
        )

    async def login(self, username: str, password: str, existing_session_id: str)-> Token:
        if not self.redis_session:
            raise CustomException("Database connection is not initialized")

        user = await self.user_crud.get_by_username(self.db_session, username=username)
        if (not user) or (not self.password_handler.verify(user.password, password)):
            raise BadRequestException("Invalid credentials")

        refresh_token = self.jwt_handler.encode_refresh_token(
            payload={"sub": "refresh_token", "verify": str(user.id)}
        )

        await self.redis_session.set(
            name=refresh_token, value=user.id, ex=self.jwt_handler.refresh_token_expire
        )

        token = Token(
            access_token=None,
            refresh_token=refresh_token,
        )
        # if user was verified
        session_id_redis = await self.redis_session.get(existing_session_id)
        if str(session_id_redis) == str(user.id):
            token.access_token = self.jwt_handler.encode(payload={"user_id": str(user.id)})
            return token

        return token

    async def logout(self, refresh_token) -> None:
        if not refresh_token:
            raise BadRequestException
        if not self.redis_session:
            raise CustomException("Database connection is not initialized")
        await self.redis_session.delete(refresh_token)
        return None

    async def me(self, user_id) -> UserOut:
        user = await self.user_crud.get_by_id(self.db_session, user_id)
        if not user:
            raise BadRequestException("Invalid credentials")
        return UserOut(
            id=user.id,
            username=user.username,
            updated_at=user.updated_at,
            created_at=user.created_at,
        )

    async def verify(
        self,
        refresh_token: str,
        session_id: str,
        code: str,
        settings=settings,
    ) -> None:
        if not self.redis_session:
            raise CustomException("Database connection is not initialized")
        session_id_redis, user_id = await asyncio.gather(
            self.redis_session.get(session_id), self.redis_session.get(refresh_token)
        )
        if not user_id or len(str(user_id)) < 5:
            raise UnauthorizedException("Invalid Refresh Token")
        elif session_id_redis != str(user_id):
            user = await self.user_crud.get_by_id(self.db_session, user_id=user_id)
            assert user is not None
            if not totp.TOTP(user.gauth).verify(code):
                raise BadRequestException("Invalid Code")
            await self.redis_session.set(
                session_id, value=user_id, ex=(settings.SESSION_EXPIRE_MINUTES) * 60
            )
        else:
            raise BadRequestException("Already Verified")
        return None

    async def refresh_token(self, old_refresh_token: str, session_id: str) -> Token | str:
        if not self.redis_session:
            raise CustomException("Database connection is not initialized")

        user_id, ttl, session_id = await asyncio.gather(
            self.redis_session.get(old_refresh_token),
            self.redis_session.ttl(old_refresh_token),
            self.redis_session.get(session_id),
        )
        if not user_id or len(str(user_id)) < 5:
            return UnauthorizedException("Invalid Refresh Token")

        if session_id != user_id:
            raise UnauthorizedException(
                "Please verify using 2 step authentication first"
            )

        access_token = self.jwt_handler.encode(payload={"user_id": str(user_id)})
        refresh_token = self.jwt_handler.encode_refresh_token(
            payload={"sub": "refresh_token", "verify": str(user_id)}
        )

        await asyncio.gather(
            self.redis_session.set(refresh_token, user_id, ex=ttl),
            self.redis_session.delete(old_refresh_token),
        )
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )

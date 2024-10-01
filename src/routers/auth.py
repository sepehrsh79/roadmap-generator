from fastapi import APIRouter, Depends, Request, Response

from src.controllers.auth import AuthController
from src.core.database import DBManager, get_db
from src.core.redis.client import RedisManager, get_redis_db
from src.depends import (
    get_current_user_from_db,
    get_current_user_with_refresh,
)
from src.schema.user import UserRegister, UserOut, UserOutRegister, UserLogin

router = APIRouter(
    prefix="/auth",
    tags=[
        "auth",
    ],
)


@router.post(
    "/register", description="register new user", response_model=UserOutRegister
)
async def register(
    data: UserRegister, db_session: DBManager = Depends(get_db)
) -> UserOutRegister:
    return await AuthController(db_session=db_session).register(**data.dict())


@router.post("/login", description="Create access and refresh tokens for verified user")
async def login(
    data: UserLogin,
    request: Request,
    response: Response,
    db_session: DBManager = Depends(get_db),
    redis_db: RedisManager = Depends(get_redis_db),
):
    try:
        tokens = await AuthController(
            db_session=db_session, redis_session=redis_db
        ).login(
            **data.dict(), existing_session_id=request.cookies.get("Session-Id", "")
        )
    except Exception as e:
        raise e
    response.set_cookie(
        key="Refresh-Token",
        value=tokens.refresh_token,
        secure=True,
        httponly=True,
        samesite="strict",
    )
    if tokens.access_token:
        response.set_cookie(
            key="Access-Token",
            value=tokens.access_token,
            secure=True,
            httponly=True,
            samesite="strict",
        )
    return {
        "access_token": tokens.access_token,
        "refresh_token": tokens.refresh_token,
    }


@router.post("/verify", description="verify user")
async def verify(
    request: Request,
    code: str,
    db_session: DBManager = Depends(get_db),
    redis_db: RedisManager = Depends(get_redis_db),
    user_id: str = Depends(get_current_user_with_refresh),
):
    assert user_id is not None
    await AuthController(db_session=db_session, redis_session=redis_db).verify(
        refresh_token=request.cookies.get("Refresh-Token", ""),
        session_id=request.cookies.get("Session-Id", ""),
        code=code,
    )
    return {"message": "user verify successfully"}


@router.post("/refresh", description="refresh access token")
async def refresh_token(
    response: Response,
    request: Request,
    db_session: DBManager = Depends(get_db),
    redis_db: RedisManager = Depends(get_redis_db),
    user_id: str = Depends(get_current_user_with_refresh),
):
    assert user_id is not None
    try:
        tokens = await AuthController(
            db_session=db_session, redis_session=redis_db
        ).refresh_token(
            old_refresh_token=request.cookies.get("Refresh-Token", ""),
            session_id=request.cookies.get("Session-Id", ""),
        )
    except Exception as e:
        raise e

    assert tokens.access_token is not None
    response.set_cookie(
        key="Refresh-Token",
        value=tokens.refresh_token,
        secure=True,
        httponly=True,
        samesite="strict",
    )
    response.set_cookie(
        key="Access-Token",
        value=tokens.access_token,
        secure=True,
        httponly=True,
        samesite="strict",
    )
    return {
        "access_token": tokens.access_token,
        "refresh_token": tokens.refresh_token,
    }


@router.get("/me")
async def me(current_user: UserOut = Depends(get_current_user_from_db)) -> UserOut:
    return current_user


@router.delete("/logout")
async def logout(
    response: Response,
    request: Request,
    redis_db: RedisManager = Depends(get_redis_db),
):
    await AuthController(redis_session=redis_db, db_session=None).logout(  # type: ignore
        request.cookies.get("Refresh-Token", ""),  # type: ignore
    )
    response.set_cookie(
        key="Refresh-Token",
        value="",
        secure=True,
        httponly=True,
        samesite="strict",
    )
    response.set_cookie(
        key="Access-Token",
        value="",
        secure=True,
        httponly=True,
        samesite="strict",
    )
    return None

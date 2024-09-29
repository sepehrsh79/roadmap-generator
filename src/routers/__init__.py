from fastapi import APIRouter

from .auth import router as auth_router
from .input import router as input_router

routers = APIRouter()
routers.include_router(auth_router)
routers.include_router(input_router)

import datetime
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr


class CurrentUser(BaseModel):
    id: UUID | None = Field(None, description="User ID")

    class Config:
        validate_assignment = True


class UserRegister(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(CurrentUser):
    username: str
    email: EmailStr
    updated_at: datetime.datetime
    created_at: datetime.datetime


class UserQuery(UserOut):
    gauth: str


class UserOutRegister(UserQuery):
    qr_img: str

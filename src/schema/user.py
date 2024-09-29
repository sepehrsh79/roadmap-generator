import datetime

from pydantic import BaseModel, Field, EmailStr


class CurrentUser(BaseModel):
    id: int | None = Field(None, description="User ID")

    class Config:
        validate_assignment = True


class UserIn(BaseModel):
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

from enum import Enum
from pydantic import BaseModel, field_validator, Field, EmailStr, ConfigDict
from re import search


class UserBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr


class UserIn(UserBase):
    password: str = Field(..., min_length=8)

    @field_validator('password')
    @classmethod
    def password_strength(cls, pwd) -> str:
        if not search(r'[A-Z]', pwd):
            raise ValueError('The password must contain at least one capital letter.')
        if not search(r'[a-z]', pwd):
            raise ValueError('The password must contain at least one lowercase letter.')
        if not search(r'[0-9]', pwd):
            raise ValueError('The password must contain at least one number.')
        if not search(r'[^A-Za-z0-9]', pwd):
            raise ValueError('The password must contain at least one special character.')
        return pwd


class UserOut(UserBase):
    pass


class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserInDB(UserBase):
    hashed_password: str
    role: str = Role.USER.value

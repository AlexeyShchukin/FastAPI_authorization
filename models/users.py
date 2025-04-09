from enum import Enum
from pydantic import BaseModel, field_validator, Field, EmailStr, ConfigDict, constr
from re import search


class UserBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: constr(max_length=16) = Field(description="Username must be not more than 16 characters")
    email: EmailStr


class UserIn(UserBase):
    password: constr(min_length=8) = Field(description="""Password must be minimum 8 characters 
    including one capital and one lowercase letter, one number and one special character""")

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

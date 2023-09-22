from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


# region Users


class UserBase(BaseModel):
    """
    Base class for users

    Args:
        BaseModel (class): Pydantic base model
    """
    email: EmailStr

    class Config:
        from_attributes = True


class User(UserBase):
    """
    Class User

    Args:
        UserBase (class): User base class adding password
    """
    password: str


class UserResponse(UserBase):
    """
    Derived class from UserBase for responses to hide the password

    Args:
        UserBase (class): Base class for users
    """
    id: int
    created_at: datetime


# endregion

# region LOGIN
class UserLogin(BaseModel):
    """
    Schema for user API Auth

    Args:
        BaseModel (class): base model for our user
    """
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int

# endregion


# region Post


class PostBase(BaseModel):
    title: str
    content: str
    published: bool

    class Config:
        from_attributes = True


class CreatePost(PostBase):
    pass


class ResponsePost(PostBase):
    id: int
    created_at: datetime
    author_id: int
    owner: UserResponse

# endregion

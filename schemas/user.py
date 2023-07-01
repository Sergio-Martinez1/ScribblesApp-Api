from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date


class NewUser(BaseModel):
    username: str = Field(min_length=1, max_length=1000)
    email: str
    password: str = Field(min_length=1, max_length=1000)
    profile_photo: Optional[str] = None
    cover_photo: Optional[str] = None
    description: Optional[str] = None
    personal_url: Optional[str] = None
    location: Optional[str] = None
    birthday: Optional[date] = Field(None,
                                     example="2023-05-28",
                                     description="User birthday")
    prohibited_posts: Optional[List[int]] = None

    class Config:
        schema_extra = {
            "example": {
                "username": "user",
                "email": "user@email.com",
                "password": "SecurePassword21@",
                "profile_photo": "http://image.com",
                "cover_photo": "http://image.com",
                "description": "Description example",
                "personal_url": "http://personal.com",
                "location": "Washington D.C., United States",
                "birthday": "2023-05-28",
                "prohibited_posts": [15, 5, 103]
            }
        }
        orm_mode = True


class UserUpdate(BaseModel):
    email: Optional[str] = None
    profile_photo: Optional[str] = None
    cover_photo: Optional[str] = None
    description: Optional[str] = None
    personal_url: Optional[str] = None
    location: Optional[str] = None
    birthday: Optional[date] = Field(None,
                                     example="2023-05-28",
                                     description="User birthday")

    class Config:
        schema_extra = {
            "example": {
                "email": "user@email.com",
                "profile_photo": "http://image.com",
                "cover_photo": "http://image.com",
                "description": "Description example",
                "personal_url": "http://personal.com",
                "location": "Washington D.C., United States",
                "birthday": "2023-05-28",
            }
        }
        orm_mode = True


class MyUser(BaseModel):
    username: str = Field(min_length=1, max_length=1000)
    email: str
    creation_date: date = Field(...,
                                example="2023-05-28",
                                description="User creation date")
    profile_photo: Optional[str] = None
    cover_photo: Optional[str] = None
    description: Optional[str] = None
    personal_url: Optional[str] = None
    location: Optional[str] = None
    birthday: Optional[date] = Field(None,
                                     example="2023-05-28",
                                     description="User birthday")
    prohibited_posts: Optional[List[int]] = None

    class Config:
        schema_extra = {
            "example": {
                "username": "user",
                "email": "user@email.com",
                "creation_date": "2023-05-28",
                "profile_photo": "http://image.com",
                "cover_photo": "http://image.com",
                "description": "Description example",
                "personal_url": "http://personal.com",
                "location": "Washington D.C., United States",
                "birthday": "2023-05-28",
                "prohibited_posts": [15, 5, 103]
            }
        }
        orm_mode = True


class PublicUser(BaseModel):
    username: str = Field(min_length=1, max_length=1000)
    creation_date: date = Field(...,
                                example="2023-05-28",
                                description="User creation date")
    profile_photo: Optional[str] = None
    cover_photo: Optional[str] = None
    description: Optional[str] = None
    personal_url: Optional[str] = None
    location: Optional[str] = None
    birthday: Optional[date] = Field(None,
                                     example="2023-05-28",
                                     description="User birthday")

    class Config:
        schema_extra = {
            "example": {
                "username": "Pepe21",
                "creation_date": "2023-05-28",
                "profile_photo": "http://image.com",
                "cover_photo": "http://image.com",
                "description": "Description example",
                "personal_url": "http://personal.com",
                "location": "Washington D.C., United States",
                "birthday": "2023-05-28"
            }
        }
        orm_mode = True


class PlainUser(BaseModel):
    id: int
    username: str = Field(min_length=1, max_length=1000)
    profile_photo: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "username": "Pepe21",
                "profile_photo": "http://image.com",
            }
        }
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    profile_photo: Optional[str] = None


class PasswordChange(BaseModel):
    password: str = Field(min_length=1, max_length=1000)
    new_password: str = Field(min_length=1, max_length=1000)


class UsernameChange(BaseModel):
    username: str = Field(min_length=1, max_length=1000)
    password: str = Field(min_length=1, max_length=1000)

from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    username: str = Field(min_length=1, max_length=1000)
    email: str
    password: str = Field(min_length=1, max_length=1000)
    image: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "username": "Pepe21",
                "email": "pepe21@email.com",
                "password": "pepe21A1",
                "image": "http://image.com"
            }
        }
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str

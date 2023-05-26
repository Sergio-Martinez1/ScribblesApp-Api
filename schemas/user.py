from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    username: str = Field(min_length=4, max_length=30)
    email: str
    password: str = Field(min_length=6, max_length=30)
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

from pydantic import BaseModel, Field


class Tag(BaseModel):
    content: str = Field(default=None)

    class Config():
        schema_extra = {
            "example": {
                "content": "Movies",
            }
        }
        orm_mode = True

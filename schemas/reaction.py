from pydantic import BaseModel


class Reaction(BaseModel):
    user_id: int
    post_id: int

    class Config():
        schema_extra = {
            "example": {
                "user_id": 1,
                "post_id": 1
            }
        }
        orm_mode = True

from pydantic import BaseModel


class ReactionIn(BaseModel):
    post_id: int

    class Config():
        schema_extra = {
            "example": {
                "post_id": 1
            }
        }
        orm_mode = True


class ReactionOut(BaseModel):
    id: int
    user_id: int
    post_id: int

    class Config():
        schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "post_id": 1
            }
        }
        orm_mode = True

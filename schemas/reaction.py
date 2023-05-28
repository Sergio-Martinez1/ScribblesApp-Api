from pydantic import BaseModel


class Reaction(BaseModel):
    user_id: int

    class Config():
        orm_mode = True

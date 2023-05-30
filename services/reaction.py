from sqlalchemy.orm import Session
from models.models import Reaction as ReactionModel
from schemas.reaction import Reaction


class ReactionService():
    def __init__(self):
        pass

    async def get_reactions(self, db: Session):
        return db.query(ReactionModel).all()

    async def create_reaction(self, reaction: Reaction, db: Session):
        new_reaction = ReactionModel(**reaction.dict())
        db.add(new_reaction)
        db.commit()
        return

    async def delete_reaction(self, id: int, db: Session):
        result = db.query(ReactionModel).filter(ReactionModel.id == id).first()
        if not result:
            return
        db.delete(result)
        db.commit()
        return

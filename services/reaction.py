from sqlalchemy.orm import Session
from models.models import Reaction as ReactionModel
from schemas.reaction import Reaction
from models.models import User as UserModel
from fastapi import HTTPException, status


class ReactionService():

    def __init__(self):
        pass

    async def get_reactions(self, db: Session):
        reactions = db.query(ReactionModel).all()
        if not reactions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='No reactions found')
        return reactions

    async def create_reaction(self, reaction: Reaction, db: Session,
                              username: str):
        user_exist = db.query(UserModel).filter(
            UserModel.username == username).first()
        if not user_exist:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Sign in first")

        new_reaction = ReactionModel(**reaction.dict())
        db.add(new_reaction)
        db.commit()
        return

    async def delete_reaction(self, id: int, db: Session, username: str):
        reaction = db.query(ReactionModel).filter(
            ReactionModel.id == id).first()
        if not reaction:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Reaction not exist")

        creator = db.query(UserModel).filter(
            UserModel.id == reaction.user_id).first()
        if username != creator.username:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Operation not allowed")
        db.delete(reaction)
        db.commit()
        return

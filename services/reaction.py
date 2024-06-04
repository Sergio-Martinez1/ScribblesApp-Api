from sqlalchemy.orm import Session
from models.models import Reaction as ReactionModel
from schemas.reaction import ReactionIn
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

    async def get_my_reactions(self, db: Session, username: str):
        myUser = db.query(UserModel).filter(
            UserModel.username == username).first()
        if not myUser:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User does no exist")
        reactions = db.query(ReactionModel).filter(
            ReactionModel.user_id == myUser.id).all()
        if not reactions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='No reactions found')
        return reactions

    async def create_reaction(self, reaction: ReactionIn, db: Session,
                              username: str):
        user_exist = db.query(UserModel).filter(
            UserModel.username == username).first()
        if not user_exist:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Sign in first")
        reaction_exist = db.query(ReactionModel).filter(
            ReactionModel.post_id == reaction.post_id).filter(
                ReactionModel.user_id == user_exist.id).first()
        if reaction_exist:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Reaction in this post already exist")

        new_reaction = ReactionModel(user_id=user_exist.id,
                                     post_id=reaction.post_id)
        db.add(new_reaction)
        db.commit()
        return new_reaction

    async def delete_reaction(self, post_id: int, db: Session, username: str):
        creator = db.query(UserModel).filter(
            UserModel.username == username).first()
        if not creator:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="User does not exist")
        reaction = db.query(ReactionModel).filter(
            ReactionModel.post_id == post_id).filter(
                ReactionModel.user_id == creator.id).first()
        if not reaction:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Reaction in this post not exist")
        db.delete(reaction)
        db.commit()
        return

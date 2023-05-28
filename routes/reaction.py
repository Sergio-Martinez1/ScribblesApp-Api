from fastapi import APIRouter, Depends, status
from typing import List
from schemas.reaction import Reaction
from db_config.database import get_db
from sqlalchemy.orm import Session
from services.reaction import ReactionService

reactions_router = APIRouter(prefix='/reactions', tags=['reactions'])


@reactions_router.get('/',
                      response_model=List[Reaction],
                      status_code=status.HTTP_200_OK)
async def get_reactions(db: Session = Depends(get_db)):
    reactions = await ReactionService().get_reactions(db)
    return reactions

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from typing import List
from schemas.reaction import Reaction
from db_config.database import get_db
from sqlalchemy.orm import Session
from services.reaction import ReactionService
from auth.authenticate import authenticate

reactions_router = APIRouter(prefix='/reactions', tags=['reactions'])


@reactions_router.get('/',
                      response_model=List[Reaction],
                      status_code=status.HTTP_200_OK)
async def get_reactions(db: Session = Depends(get_db)):
    reactions = await ReactionService().get_reactions(db)
    return reactions


@reactions_router.post('/',
                       response_model=dict,
                       status_code=status.HTTP_201_CREATED)
async def create_reaction(reaction: Reaction,
                          db: Session = Depends(get_db),
                          user: str = Depends(authenticate)):
    await ReactionService().create_reaction(reaction, db, user)
    return JSONResponse(content={"message": "Succesful reaction created."})


@reactions_router.delete('/{id}',
                         response_model=dict,
                         status_code=status.HTTP_200_OK)
async def delete_reaction(id: int,
                          db: Session = Depends(get_db),
                          user: str = Depends(authenticate)):
    await ReactionService().delete_reaction(id, db, user)
    return JSONResponse(content={"message": "Succesful reaction deleted."})

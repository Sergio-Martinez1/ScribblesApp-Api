from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from typing import List
from schemas.tag import Tag
from db_config.database import get_db
from sqlalchemy.orm import Session
from services.tag import TagService
from auth.authenticate import authenticate

tags_router = APIRouter(prefix='/tags', tags=['tags'])


@tags_router.get('/', response_model=List[Tag], status_code=status.HTTP_200_OK)
async def get_tags(db: Session = Depends(get_db)):
    tags = await TagService().get_tags(db)
    return tags


@tags_router.get('/top',
                 status_code=status.HTTP_200_OK)
async def get_top_tags(db: Session = Depends(get_db)):
    tags = await TagService().get_top_tags(db, 3)
    return tags


@tags_router.post('/',
                  response_model=dict,
                  status_code=status.HTTP_201_CREATED)
async def create_tag(tag: Tag,
                     db: Session = Depends(get_db),
                     user: str = Depends(authenticate)):
    await TagService().create_tag(tag, db, user)
    return JSONResponse(content={"message": "Succesful tag created."},
                        status_code=status.HTTP_201_CREATED)


@tags_router.delete('/{id}',
                    response_model=dict,
                    status_code=status.HTTP_200_OK)
async def delete_tag(id: int,
                     db: Session = Depends(get_db),
                     user: str = Depends(authenticate)):
    await TagService().delete_tag(id, db, user)
    return JSONResponse(content={"message": "Succesful tag deleted."})

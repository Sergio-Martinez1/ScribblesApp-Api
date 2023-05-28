from fastapi import APIRouter, Depends, status
from typing import List
from schemas.tag import Tag
from db_config.database import get_db
from sqlalchemy.orm import Session
from services.tag import TagService


tags_router = APIRouter(prefix='/tags', tags=['tags'])


@tags_router.get('/',
                 response_model=List[Tag],
                 status_code=status.HTTP_200_OK)
async def get_tags(db: Session = Depends(get_db)):
    tags = await TagService().get_tags(db)
    return tags

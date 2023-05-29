from fastapi import APIRouter, Depends, status
from typing import List
from schemas.comment import Comment
from db_config.database import get_db
from sqlalchemy.orm import Session
from services.comment import CommentService


comments_router = APIRouter(prefix='/comments', tags=['comments'])


@comments_router.get('/',
                     response_model=List[Comment],
                     status_code=status.HTTP_200_OK)
async def get_comments(db: Session = Depends(get_db)):
    comments = await CommentService().get_comments(db)
    return comments

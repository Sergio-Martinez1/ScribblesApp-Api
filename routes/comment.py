from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
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


@comments_router.post('/',
                      response_model=dict,
                      status_code=status.HTTP_201_CREATED)
async def create_comment(comment: Comment,
                         db: Session = Depends(get_db)):
    await CommentService().create_comment(comment, db)
    return JSONResponse(content={"message": "Succesful comment created."})


@comments_router.put('/{id}',
                     response_model=dict,
                     status_code=status.HTTP_200_OK)
async def update_comment(id: int, comment: Comment,
                         db: Session = Depends(get_db)):
    await CommentService().update_comment(id, comment, db)
    return JSONResponse(content={"message": "Succesful comment update."})


@comments_router.delete('/{id}',
                        response_model=dict,
                        status_code=status.HTTP_200_OK)
async def delete_comment(id: int,
                         db: Session = Depends(get_db)):
    await CommentService().delete_comment(id, db)
    return JSONResponse(content={"message": "Succesful comment deleted."})

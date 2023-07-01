from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from typing import List
from schemas.comment import CommentIn, CommentOut, CommentToEdit
from db_config.database import get_db
from sqlalchemy.orm import Session
from services.comment import CommentService
from auth.authenticate import authenticate

comments_router = APIRouter(prefix='/comments', tags=['comments'])


@comments_router.get('/all',
                     response_model=List[CommentOut],
                     status_code=status.HTTP_200_OK)
async def get_comments(db: Session = Depends(get_db)):
    comments = await CommentService().get_comments(db)
    return comments


@comments_router.get('/{post_id}',
                     response_model=List[CommentOut],
                     status_code=status.HTTP_200_OK)
async def get_comments_in_post(post_id: int, db: Session = Depends(get_db)):
    comments = await CommentService().get_comments_in_post(post_id, db)
    return comments


@comments_router.post('/',
                      response_model=dict,
                      status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentIn,
                         db: Session = Depends(get_db),
                         user: str = Depends(authenticate)):
    await CommentService().create_comment(comment, db, user)
    return JSONResponse(content={"message": "Comment created successfully."},
                        status_code=status.HTTP_201_CREATED)


@comments_router.put('/{id}',
                     response_model=dict,
                     status_code=status.HTTP_200_OK)
async def update_comment(id: int,
                         comment: CommentToEdit,
                         db: Session = Depends(get_db),
                         user: str = Depends(authenticate)):
    await CommentService().update_comment(id, comment, db, user)
    return JSONResponse(content={"message": "Succesful comment update."})


@comments_router.delete('/{id}',
                        response_model=dict,
                        status_code=status.HTTP_200_OK)
async def delete_comment(id: int,
                         db: Session = Depends(get_db),
                         user: str = Depends(authenticate)):
    await CommentService().delete_comment(id, db, user)
    return JSONResponse(content={"message": "Succesful comment deleted."})

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from services.post import PostService
from db_config.database import get_db
from typing import List
from schemas.post import PostIn, PostOut
from auth.authenticate import authenticate

posts_router = APIRouter(prefix='/posts', tags=['posts'])


@posts_router.get('/',
                  response_model=List[PostOut],
                  status_code=status.HTTP_200_OK)
async def get_posts(db: Session = Depends(get_db)) -> List[PostOut]:

    posts = await PostService().get_posts(db)
    return posts


@posts_router.post('/',
                   response_model=dict,
                   status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostIn,
    db: Session = Depends(get_db),
    user: str = Depends(authenticate)
) -> dict:

    await PostService().create_post(db, post, user)
    return JSONResponse(content={'message': 'Post sucessfully created'},
                        status_code=status.HTTP_201_CREATED)


@posts_router.put('/{id}', response_model=dict, status_code=status.HTTP_200_OK)
async def update_post(
    id: int,
    post: PostIn,
    db: Session = Depends(get_db),
    user: str = Depends(authenticate)
) -> dict:

    await PostService().update_post(db, post, id, user)
    return JSONResponse(content={'message': 'Post sucessfully updated'},
                        status_code=status.HTTP_200_OK)


@posts_router.delete('/{id}', status_code=status.HTTP_200_OK)
async def delete_post(
    id: int, db: Session = Depends(get_db), user: str = Depends(authenticate)
) -> dict:

    await PostService().delete_post(db, id, user)
    return JSONResponse(content={'message': 'Post sucessfully deleted'},
                        status_code=status.HTTP_200_OK)

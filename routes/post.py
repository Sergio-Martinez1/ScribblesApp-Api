from fastapi import APIRouter, status, Depends, Query
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


@posts_router.get('/home',
                  response_model=List[PostOut],
                  status_code=status.HTTP_200_OK)
async def get_home_posts(user: str = Depends(authenticate),
                         db: Session = Depends(get_db),
                         offset: int = Query(default=0, ge=0),
                         limit: int = Query(default=10,
                                            ge=1)) -> List[PostOut]:
    posts = await PostService().get_home_posts(username=user,
                                               db=db,
                                               offset=offset,
                                               limit=limit)
    return posts


@posts_router.get('/myPosts',
                  response_model=List[PostOut],
                  status_code=status.HTTP_200_OK)
async def get_my_posts(user: str = Depends(authenticate),
                       db: Session = Depends(get_db),
                       offset: int = Query(default=0, ge=0),
                       limit: int = Query(default=10, ge=1)) -> List[PostOut]:
    posts = await PostService().get_my_posts(username=user,
                                             db=db,
                                             offset=offset,
                                             limit=limit)
    return posts


@posts_router.get('/pagination',
                  response_model=List[PostOut],
                  status_code=status.HTTP_200_OK)
async def get_posts_pagination(limit: int = Query(default=10, ge=1),
                               offset: int = Query(default=0, ge=0),
                               db: Session = Depends(get_db)) -> List[PostOut]:
    posts = await PostService().get_posts_pagination(db,
                                                     limit=limit,
                                                     offset=offset)
    return posts


@posts_router.get('/tags/{tag_content}',
                  response_model=List[PostOut],
                  status_code=status.HTTP_200_OK)
async def get_posts_with_tag(tag_content: str,
                             limit: int = Query(default=10, ge=1),
                             offset: int = Query(default=0, ge=0),
                             db: Session = Depends(get_db)) -> List[PostOut]:
    posts = await PostService().get_posts_with_tag(db=db,
                                                   tag_content=tag_content,
                                                   limit=limit,
                                                   offset=offset)
    return posts


@posts_router.get('/user/{user_id}',
                  response_model=List[PostOut],
                  status_code=status.HTTP_200_OK)
async def get_posts_by_user_id(
        user_id: int, db: Session = Depends(get_db)) -> List[PostOut]:
    posts = await PostService().get_posts_by_user_id(db, user_id)
    return posts


@posts_router.get('/{id}',
                  response_model=PostOut,
                  status_code=status.HTTP_200_OK)
async def get_post(id: int, db: Session = Depends(get_db)) -> PostOut:
    post = await PostService().get_post(id, db)
    return post


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


@posts_router.post('/dont_show_post/{id}', status_code=status.HTTP_200_OK)
async def dont_show_post(id: int,
                         db: Session = Depends(get_db),
                         user: str = Depends(authenticate)):
    await PostService().dont_show_post(db=db, id=id, username=user)
    return JSONResponse(content={'message': 'Post sucessfully added'},
                        status_code=status.HTTP_200_OK)

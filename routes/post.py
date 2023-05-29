from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from services.post import PostService
from db_config.database import get_db
from typing import List
from schemas.post import Post

posts_router = APIRouter(prefix='/posts', tags=['posts'])


@posts_router.get('/',
                  response_model=List[Post],
                  status_code=status.HTTP_200_OK)
async def get_posts(db: Session = Depends(get_db)):
    posts = await PostService().get_posts(db)
    return posts

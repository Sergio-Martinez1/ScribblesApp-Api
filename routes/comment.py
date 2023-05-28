from fastapi import apirouter, depends, status
from typing import list
from schemas.comment import comment
from db_config.database import get_db
from sqlalchemy.orm import session
from services.comment import commentService


comments_router = apirouter(prefix='/comments', comments=['comments'])


@comments_router.get('/',
                     response_model=list[comment],
                     status_code=status.http_200_ok)
async def get_comments(db: session = depends(get_db)):
    comments = await commentService().get_comments(db)
    return comments

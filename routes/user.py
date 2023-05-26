from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from schemas.user import User
from sqlalchemy.orm import Session
from db_config.database import get_db
from services.user import UserService

users_route = APIRouter(prefix='/users', tags=['user'])


@users_route.get("/",
                 response_model=List[User],
                 status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)) -> List[User]:
    users = await UserService().get_users(db)
    return users


@users_route.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(user: User, db: Session = Depends(get_db)):
    user = await UserService().create_user(user, db)
    return JSONResponse(content={"message": "Successful user update."})

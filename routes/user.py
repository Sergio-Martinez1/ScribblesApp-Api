from typing import List
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from schemas.user import User
from schemas.user import TokenResponse
from sqlalchemy.orm import Session
from db_config.database import get_db
from services.user import UserService
from fastapi.security import OAuth2PasswordRequestForm

users_route = APIRouter(prefix='/users', tags=['user'])


@users_route.get("/",
                 response_model=List[User],
                 status_code=status.HTTP_200_OK)
async def get_users(db: Session = Depends(get_db)) -> List[User]:
    users = await UserService().get_users(db)
    return users


@users_route.post('/signup',
                  status_code=status.HTTP_201_CREATED,
                  response_model=dict)
async def sign_user_up(user: User, db: Session = Depends(get_db)) -> dict:

    await UserService().create_user(user, db)
    return JSONResponse(content={"message": "User created succesfully."},
                        status_code=status.HTTP_201_CREATED)


@users_route.post('/signin', response_model=TokenResponse)
async def sign_user_in(request: OAuth2PasswordRequestForm = Depends(),
                       db: Session = Depends(get_db)) -> TokenResponse:

    return await UserService().login_user(request.username, request.password,
                                          db)

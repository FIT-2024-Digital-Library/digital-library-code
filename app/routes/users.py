from fastapi import APIRouter, HTTPException, status, Response, Depends

from sqlalchemy import select, insert

from app.crud.users import register_user, login_user
from app.db.database import async_session_maker
from app.db.models import user_table
from app.schemas.users import UserRegister, UserLogin, User, UserLogined

from app.users.auth import get_password_hash, create_access_token
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['user']
)


@router.get('/profile', response_model=UserLogined, summary='Returns authorized user')
async def get_profile(user_data: User = Depends(get_current_user)):
    return user_data


@router.post('/login', response_model=UserLogined, summary='Logs user in')
async def login(response: Response, user_data: UserLogin):
    check = await login_user(user_data)
    if check is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Wrong password or email')
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True, secure=True, samesite='none')
    data = dict(check)
    data.pop('password_hash')
    return data


@router.post('/register', response_model=UserLogined, summary='Creates new user')
async def register(user_data: UserRegister):
    data = await register_user(user_data)
    return data


@router.post("/logout", response_model=None, summary='Log out of system')
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token", secure=True, samesite='none')
    return {'message': 'You successfully logged out'}

from fastapi import APIRouter, HTTPException, status, Response, Depends

from app.crud.users import set_admin_role_for_user, find_user_by_id, get_users_from_db, update_user_in_db, \
    delete_user_from_db
from app.crud.users import register_user, login_user
from app.schemas import UserRegister, UserLogin, User, UserLogined
from app.settings import async_session_maker
from app.utils.auth import create_access_token, get_current_user, get_current_admin_user

router = APIRouter(
    prefix='/users',
    tags=['user']
)


@router.get('/profile', response_model=UserLogined, summary='Returns authorized user')
async def get_profile(user_data: User = Depends(get_current_user)):
    return user_data


@router.post('/login', response_model=UserLogined, summary='Logs user in')
async def login(response: Response, user_data: UserLogin):
    async with async_session_maker() as session:
        check = await login_user(session, user_data)
        if check is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Wrong password or email')
        access_token = create_access_token({"sub": str(check.id)})
        response.set_cookie(key="users_access_token", value=access_token, httponly=True, secure=True, samesite='none')
        data = dict(check)
        data.pop('password_hash')
        await session.commit()
        return data


@router.post('/register', response_model=UserLogined, summary='Creates new user')
async def register(user_data: UserRegister):
    async with async_session_maker() as session:
        data = await register_user(session, user_data)
        await session.commit()
        return data


@router.post("/logout", response_model=None, summary='Log out of system')
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token", secure=True, samesite='none')
    return {'message': 'You successfully logged out'}


@router.post('/{user_id}/get_admin_role', response_model=UserLogined, summary='Logs user in')
async def get_admin_role(user_id: int, User=Depends(get_current_user)):
    async with async_session_maker() as session:
        data = await set_admin_role_for_user(session, user_id)
        await session.commit()
        return data


@router.put('/{user_id}/update', response_model=UserLogined, summary='Updates user by id')
async def update_user_by_id(user_id: int, user_data: UserRegister, User=Depends(get_current_user)):
    async with async_session_maker() as session:
        data = await update_user_in_db(session, user_id, user_data)
        await session.commit()
        return data


@router.delete('/{user_id}/delete', response_model=UserLogined, summary='Deletes user by id')
async def delete_user_by_id(user_id: int, User=Depends(get_current_admin_user)):
    async with async_session_maker() as session:
        data = await delete_user_from_db(session, user_id)
        if data is None:
            raise HTTPException(status_code=403, detail="User doesn't exist")
        await session.commit()
        return data


@router.get('/{user_id}', response_model=UserLogined, summary='Returns user by id')
async def get_user_by_id(user_id: int, User=Depends(get_current_admin_user)):
    async with async_session_maker() as session:
        user = await find_user_by_id(session, user_id)
        if user is None:
            raise HTTPException(status_code=403, detail="User doesn't exist")
        return user


@router.get('/', response_model=list[UserLogined], summary='Returns all users')
async def get_users(User=Depends(get_current_admin_user)):
    async with async_session_maker() as session:
        data = await get_users_from_db(session)
        return data

from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncConnection

from app.crud.users import find_user_by_id
from app.schemas.users import User
from app.settings import auth_cred, db_engine
from app.models import db_metadata, user_table, author_table, genre_table, book_table


class CrudException(BaseException):
    def __init__(self, *args):
        super().__init__(*args)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, auth_cred.secret_key, algorithm=auth_cred.algorithm)
    return encode_jwt


def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, auth_cred.secret_key, algorithms=[auth_cred.algorithm])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid')

    expire = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')

    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User author_id wasn\'t found')

    user = await find_user_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.privileges == 'admin':
        return current_user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='No permission')


async def insert_test_data(connection: AsyncConnection):
    await connection.execute(user_table.insert().values(
        name='Kirill', email='Kirill@pochta.ru', password_hash='abc', privileges='admin'
    ))
    author_id = await connection.execute(author_table.insert().values(name="Pushkin"))
    genre_id = await connection.execute(genre_table.insert().values(name="Poem"))
    await connection.execute(book_table.insert().values(
        title='Evgeniy Onegin', pdf_url='http://ya.ru',
        author=author_id.inserted_primary_key[0],
        genre=genre_id.inserted_primary_key[0]
    ))


async def create_tables() -> None:
    async with db_engine.begin() as connection:
        await connection.run_sync(db_metadata.drop_all)
        await connection.run_sync(db_metadata.create_all)
        await insert_test_data(connection)

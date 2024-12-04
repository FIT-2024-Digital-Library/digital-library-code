from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection, async_sessionmaker
from .models import db_metadata, user_table, author_table, genre_table, book_table
from os import getenv
from pydantic import Field
import config
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='POSTGRES_', validate_default=False)
    login: str = config.postgres_login
    password: str = config.postgres_password
    hostname: str = config.postgres_hostname
    db_name: str


pg_cred = PostgresSettings()

db_engine = create_async_engine(
    f"postgresql+asyncpg://{pg_cred.login}:{pg_cred.password}@{pg_cred.hostname}/{pg_cred.db_name}", echo=True
)
async_session_maker = async_sessionmaker(db_engine, expire_on_commit=False)


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

from sqlalchemy.ext.asyncio import create_async_engine
from .models import db_metadata, user_table, book_table
from os import getenv

LOGIN = getenv('POSTGRES_LOGIN')
PASSWORD = getenv('POSTGRES_PASSWORD')
HOST = 'localhost:5432'
DB_NAME = 'digital-library'

db_engine = create_async_engine(
    f"postgresql+asyncpg://{LOGIN}:{PASSWORD}@{HOST}/{DB_NAME}", echo=True
)

async def create_tables() -> None:
    async with db_engine.begin() as connection:
        await connection.run_sync(db_metadata.drop_all)
        await connection.run_sync(db_metadata.create_all)
        await connection.execute(user_table.insert().values(
            name='Kirill', email='Kirill@pochta.ru', password_hash='abc', privileges='admin'
        ))
        await connection.execute(book_table.insert().values(
            title='Holy Bibe', pdf_url='http://ya.ru'
        ))
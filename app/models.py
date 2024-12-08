from sqlalchemy import MetaData, Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM

db_metadata = MetaData()

privileges_enum = ENUM("basic", "admin", name="privileges", metadata=db_metadata)

user_table = Table(
    "user_table",
    db_metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String),
    Column("name", String(30)),
    Column("password_hash", String(512)),
    Column("privileges", privileges_enum, default="basic")  # TODO: по хорошему надо будет заменить на группы
)

author_table = Table(
    "author_table",
    db_metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(150))
)

genre_table = Table(
    "genre_table",
    db_metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(150))
)

book_table = Table(
    "book_table",
    db_metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("author", ForeignKey(author_table.c.id), nullable=True),
    Column("genre", ForeignKey(genre_table.c.id), nullable=True),
    Column("published_date", Date, nullable=True),
    Column("description", String, nullable=True),
    Column("image", String, nullable=True),
    Column("pdf_url", String)
)

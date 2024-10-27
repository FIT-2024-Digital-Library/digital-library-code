from sqlalchemy import MetaData, Table, Column, Integer, String, Date, LargeBinary, ForeignKey
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
    Column("privileges", privileges_enum, default="basic") # TODO: по хорошему надо будет заменить на группы
)

book_table = Table(
    "book_table",
    db_metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("author", String(150), nullable=True),
    Column("published_data", Date, nullable=True),
    Column("description", String, nullable=True),
    Column("image", LargeBinary, nullable=True),
    Column("pdf_url", String)
)
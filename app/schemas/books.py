from datetime import date

from pydantic import BaseModel, Field, HttpUrl


class Book(BaseModel):
    id: int
    title: str
    author: int
    genre: int
    published_date: date
    description: str
    image: str
    pdf_url: str

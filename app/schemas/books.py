from datetime import date
from typing import Optional
from pydantic import BaseModel

__all__ = ["Book", "CreateBook"]


class Book(BaseModel):
    id: int
    title: str
    author: int
    genre: Optional[int] = None
    published_date: Optional[date] = None
    description: Optional[str] = None
    image: Optional[str] = None
    pdf_url: str


class CreateBook(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    published_date: Optional[date] = None
    description: Optional[str] = None
    image: Optional[str] = None
    pdf_url: str

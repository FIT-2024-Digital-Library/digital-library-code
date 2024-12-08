from datetime import date
from typing import Optional
from .base import CamelCaseBaseModel

__all__ = ["Book", "CreateBook"]


class Book(CamelCaseBaseModel):
    id: int
    title: str
    author: int
    genre: Optional[int] = None
    published_date: Optional[date] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    pdf_url: str


class CreateBook(CamelCaseBaseModel):
    title: str
    author: str
    genre: Optional[str] = None
    published_date: Optional[date] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    pdf_url: str

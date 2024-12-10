from datetime import date
from .base import CamelCaseBaseModel

__all__ = ["ReviewCreate", "Review"]


class ReviewCreate(CamelCaseBaseModel):
    mark: int
    text: str
    book_id: int


class Review(ReviewCreate):
    id: int
    author_id: int
    last_edit_date: date

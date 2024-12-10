from datetime import date

from pydantic import Field

from .base import CamelCaseBaseModel

__all__ = ["ReviewCreate", "Review"]


class ReviewCreate(CamelCaseBaseModel):
    mark: int = Field(ge=1, le=5)
    text: str
    book_id: int


class Review(ReviewCreate):
    id: int
    author_id: int
    last_edit_date: date

from datetime import date

from pydantic import Field

from .base import CamelCaseBaseModel

__all__ = ["ReviewUpdate", "ReviewCreate", "Review"]


class ReviewUpdate(CamelCaseBaseModel):
    mark: int = Field(ge=1, le=5)
    text: str


class ReviewCreate(ReviewUpdate):
    book_id: int


class Review(ReviewCreate):
    id: int
    author_id: int
    last_edit_date: date

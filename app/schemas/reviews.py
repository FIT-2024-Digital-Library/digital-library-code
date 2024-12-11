from datetime import date
from typing import Optional

from pydantic import Field

from .base import CamelCaseBaseModel

__all__ = ["ReviewsFiltersScheme", "ReviewUpdate", "ReviewCreate", "Review"]


class ReviewsFiltersScheme(CamelCaseBaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    book_id: Optional[int] = None
    owner_id: Optional[int] = None


class ReviewUpdate(CamelCaseBaseModel):
    mark: int = Field(ge=1, le=5)
    text: str


class ReviewCreate(ReviewUpdate):
    book_id: int


class Review(ReviewCreate):
    id: int
    owner_id: int
    last_edit_date: date

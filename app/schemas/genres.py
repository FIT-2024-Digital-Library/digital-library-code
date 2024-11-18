from datetime import date

from pydantic import BaseModel, Field, HttpUrl


class Genre(BaseModel):
    id: int
    name: str


from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    published_date: Optional[date]
    summary: Optional[str] = Field(None, max_length=1000)
    genre: str = Field(..., min_length=1, max_length=50)


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    published_date: Optional[date]
    summary: Optional[str] = Field(None, max_length=1000)
    genre: Optional[str] = Field(None, max_length=50)


class BookInDB(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

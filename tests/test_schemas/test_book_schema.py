from app.schemas.book import BookCreate
from pydantic import ValidationError
import pytest
from datetime import date


def test_book_create_valid():
    book = BookCreate(
        title="A Book",
        author="An Author",
        published_date=date(2020, 1, 1),
        summary="Some summary",
        genre="Fiction",
    )
    assert book.title == "A Book"


def test_book_create_missing_required():
    with pytest.raises(ValidationError):
        BookCreate(author="Author Only", genre="Fiction")  # type: ignore[]


def test_book_create_title_too_long():
    with pytest.raises(ValidationError):
        BookCreate(
            title="a" * 201,  # exceeds max length
            author="Author",
            published_date=date(2020, 1, 1),
            summary="Summary",
            genre="Genre",
        )

from datetime import date

from app.schemas.book import BookCreate, BookUpdate
from app.crud.book import create_book, get_book, get_books, update_book, delete_book


# CREATE
def test_create_book_valid(db):
    book_in = BookCreate(
        title="Valid Book",
        author="Valid Author",
        published_date=date(2021, 1, 1),
        summary="This is a valid test summary",
        genre="Fiction",
    )
    book = create_book(db, book_in)
    assert book.id is not None
    assert book.title == book_in.title


# READ
def test_get_book_found(db):
    book = create_book(
        db,
        BookCreate(
            title="Test",
            author="Author",
            published_date=None,
            summary=None,
            genre="Fiction",
        ),
    )
    fetched = get_book(db, book.id)

    assert fetched is not None
    assert fetched.id == book.id


def test_get_book_not_found(db):
    assert get_book(db, 9999) is None


def test_get_books_pagination(db):
    for i in range(15):
        create_book(
            db,
            BookCreate(
                title=f"Book {i}",
                author="Author",
                published_date=None,
                summary=None,
                genre="Fiction",
            ),
        )
    result = get_books(db, skip=5, limit=5)

    assert len(result) == 5
    assert result[0].title == "Book 5"


# UPDATE
def test_update_book_valid(db):
    book = create_book(
        db,
        BookCreate(
            title="Old Title", author="A", published_date=None, summary=None, genre="G"
        ),
    )
    updated = update_book(db, book.id, BookUpdate(title="New Title", genre="New Genre"))  # type: ignore

    assert updated is not None
    assert updated.title == "New Title"
    assert updated.genre == "New Genre"


def test_update_book_not_found(db):
    result = update_book(db, 12345, BookUpdate(title="Ghost"))  # type: ignore
    assert result is None


# DELETE
def test_delete_book_success(db):
    book = create_book(
        db,
        BookCreate(
            title="To Delete",
            author="X",
            published_date=None,
            summary=None,
            genre="Drama",
        ),
    )
    deleted = delete_book(db, book.id)

    assert deleted is not None
    assert deleted.id == book.id
    assert get_book(db, book.id) is None


def test_delete_book_not_found(db):
    assert delete_book(db, 9999) is None

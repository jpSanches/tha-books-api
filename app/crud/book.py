from sqlalchemy.orm import Session
from app.db.models import Book
from app.schemas.book import BookCreate, BookUpdate


def get_book(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 10) -> list[Book]:
    return db.query(Book).offset(skip).limit(limit).all()


def create_book(db: Session, book_data: BookCreate) -> Book:
    db_book = Book(**book_data.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book_data: BookUpdate) -> Book | None:
    db_book = get_book(db, book_id)
    if not db_book:
        return None

    for field, value in book_data.model_dump(exclude_unset=True).items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> Book | None:
    db_book = get_book(db, book_id)
    if not db_book:
        return None

    db.delete(db_book)
    db.commit()
    return db_book

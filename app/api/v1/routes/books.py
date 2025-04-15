from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.schemas.book import BookCreate, BookUpdate, BookInDB
from app.db.models import Book
from app.crud import book as crud
from app.db.deps import get_db
from app.api import errors

router = APIRouter(prefix="/v1/books", tags=["Books"])


@router.post("/", response_model=BookInDB, status_code=status.HTTP_201_CREATED)
def create_book(book_in: BookCreate, db: Session = Depends(get_db)) -> Book:
    return crud.create_book(db, book_in)


@router.get("/", response_model=List[BookInDB])
def read_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
) -> List[Book]:
    return crud.get_books(db, skip=skip, limit=limit)


@router.get("/{book_id}", response_model=BookInDB)
def read_book(book_id: int, db: Session = Depends(get_db)) -> Book:
    book = crud.get_book(db, book_id)
    if not book:
        raise errors.resource_not_found(book_id)
    return book


@router.put("/{book_id}", response_model=BookInDB)
def update_book(
    book_id: int, book_in: BookUpdate, db: Session = Depends(get_db)
) -> Book:
    book = crud.update_book(db, book_id, book_in)
    if not book:
        raise errors.resource_not_found(book_id)
    return book


@router.delete("/{book_id}", response_model=BookInDB)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> Book:
    book = crud.delete_book(db, book_id)
    if not book:
        raise errors.resource_not_found(book_id)
    return book

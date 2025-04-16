from fastapi import APIRouter, BackgroundTasks, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.api import errors
from app.core.deps import get_current_user
from app.crud import book as crud
from app.db.deps import get_db
from app.db.models import Book
from app.schemas.book import BookCreate, BookUpdate, BookInDB
from app.services.sse_manager import sse_manager

router = APIRouter(prefix="/v1/books", tags=["Books"])


@router.post("/", response_model=BookInDB, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_in: BookCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
) -> Book:
    book = crud.create_book(db, book_in)

    background_tasks.add_task(
        sse_manager.broadcast,
        {
            "event": "book_created",
            "user": current_user,
            "payload": {
                "id": book.id,
                "title": book.title,
                "author": book.author,
            },
        },
    )

    return book


@router.get("/", response_model=List[BookInDB])
async def read_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1),
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
) -> List[Book]:
    return crud.get_books(db, skip=skip, limit=limit)


@router.get("/{book_id}", response_model=BookInDB)
async def read_book(
    book_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
) -> Book:
    book = crud.get_book(db, book_id)
    if not book:
        raise errors.resource_not_found(book_id)
    return book


@router.put("/{book_id}", response_model=BookInDB)
async def update_book(
    background_tasks: BackgroundTasks,
    book_id: int,
    book_in: BookUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
) -> Book:
    book = crud.update_book(db, book_id, book_in)
    if not book:
        raise errors.resource_not_found(book_id)

    background_tasks.add_task(
        sse_manager.broadcast,
        {
            "event": "book_updated",
            "user": current_user,
            "payload": {
                "id": book.id,
                "title": book.title,
                "author": book.author,
            },
        },
    )

    return book


@router.delete("/{book_id}", response_model=BookInDB)
async def delete_book(
    background_tasks: BackgroundTasks,
    book_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
) -> Book:
    book = crud.delete_book(db, book_id)
    if not book:
        raise errors.resource_not_found(book_id)

    background_tasks.add_task(
        sse_manager.broadcast,
        {
            "event": "book_deleted",
            "user": current_user,
            "payload": {
                "id": book.id,
                "title": book.title,
                "author": book.author,
            },
        },
    )

    return book

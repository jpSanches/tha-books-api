from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Date, String
from datetime import date
from app.db.database import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    published_date: Mapped[date] = mapped_column(Date, nullable=True)
    summary: Mapped[str] = mapped_column(String(1000), nullable=True)
    genre: Mapped[str] = mapped_column(String(50), nullable=False)

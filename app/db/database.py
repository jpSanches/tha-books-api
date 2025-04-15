from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# TODO: Replace this logic with a migration version control system (Alembic).
def init_db() -> None:
    Base.metadata.create_all(bind=engine)


class Base(DeclarativeBase):
    pass

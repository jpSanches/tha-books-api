from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.routes import books
from app.db.database import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(books.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Books API"}

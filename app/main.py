from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.routes import auth, books
from app.db.database import init_db
from app.core.exception_handlers import global_exception_handler


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.add_exception_handler(Exception, global_exception_handler)
app.include_router(books.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Books API"}

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.routes import auth, books, health, stream
from app.db.database import init_db
from app.core.exception_handlers import global_exception_handler


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Books API",
    description="API for managing books in a SQLite database.",
    version="v0.0.1",
    lifespan=lifespan,
    openapi_tags=[
        {
            "name": "Health",
            "description": "Health checker. Useful for liveness probe.",
        },
        {
            "name": "SSE",
            "description": "Server-Sent Events for real-time updates.",
        },
        {
            "name": "Books",
            "description": "CRUD operations for books.",
        },
        {
            "name": "Auth",
            "description": "Authentication to access secured endpoints.",
        },
    ],
)
app.add_exception_handler(Exception, global_exception_handler)
app.include_router(health.router)
app.include_router(stream.router)
app.include_router(books.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Books API"}

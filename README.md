# 📚 Books API – FastAPI CRUD Application

A simple **FastAPI** backend application for managing a books database. This project is a **take-home assignment** that showcases API design with **JWT authentication**, **CRUD operations**, **pagination**, and **real-time updates using Server-Sent Events (SSE)**.

---

## ✨ Features

- 🔐 **JWT-based Authentication** (Login & Token generation)
- 📖 **CRUD Endpoints** for managing books
- 📄 **Pagination** support for listing books
- ✅ **Pydantic Models** for validation and serialization
- ⚠️ **Robust Error Handling** (404, 422, 401, etc.)
- 🔁 **SSE Streaming Endpoint** for real-time updates (Bonus)
- 🧪 **OpenAPI/Swagger UI** available at `/docs`
- 🚀 **Deployable to Heroku**

---

## 🧱 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) – Web framework
- [SQLite](https://www.sqlite.org/index.html) – Lightweight relational DB
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM
- [Pydantic](https://docs.pydantic.dev/) – Validation and parsing
- [Uvicorn](https://www.uvicorn.org/) – ASGI server
- [Heroku](https://www.heroku.com/) – Deployment
- [Python-Jose](https://python-jose.readthedocs.io/) – JWT encoding/decoding

---

## 📁 Project Structure

```
books_api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   └── __init__.py
│   ├── db/
│   │   └── __init__.py
│   ├── schemas/
│   │   └── __init__.py
│   ├── crud/
│   │   └── __init__.py
│   ├── api/
│   │   └── v1/
│   │       └── routes/
│   │           └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   └── utils/
│       └── __init__.py
├── books.db
├── requirements.txt
├── Procfile
└── .gitignore
```

---
## 🚀 Getting Started

### 📥 Installation

1. **Clone the repo**:
   ```bash
   git clone https://github.com/jpSanches/tha-books-api.git
   cd tha-books-api
   ```

2. **Create virtualenv & install dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the app locally**:
   ```bash
   uvicorn main:app --reload
   ```

---

## 🔐 Authentication

Use the `/login` endpoint to obtain a **JWT token**.

- **Username**: `admin`
- **Password**: `admin`

Once authenticated, use the token in the `Authorization` header:

```
Authorization: Bearer <your_token>
```

All `/books/*` endpoints require this token.

---

## 📘 API Overview

### Auth

- `POST /login` – Login and get JWT token

### Books (Protected)

- `POST /books/` – Add a new book
- `GET /books/` – List all books (supports `skip` and `limit`)
- `GET /books/{id}` – Retrieve a book by ID
- `PUT /books/{id}` – Update a book by ID
- `DELETE /books/{id}` – Delete a book by ID

### SSE

- `GET /stream` – Stream server-side events

## 📌 Notes

- Error handling is included for:
  - Missing books (`404`)
  - Invalid input (`422`)
  - Unauthorized access (`401`)
- All schema validations are enforced using Pydantic
- SSE endpoint streams periodic updates for demonstration purposes




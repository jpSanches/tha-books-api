from fastapi.testclient import TestClient


def test_create_book_success(client: TestClient, auth_headers: dict):
    response = client.post(
        "/v1/books/",
        headers=auth_headers,
        json={
            "title": "Book A",
            "author": "Author X",
            "published_date": "2023-01-01",
            "summary": "Test summary",
            "genre": "Fiction",
        },
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Book A"


def test_create_book_missing_fields(client: TestClient, auth_headers: dict):
    response = client.post(
        "/v1/books/", headers=auth_headers, json={"title": "Incomplete"}
    )
    assert response.status_code == 422


def test_unauthenticated_create_book(client: TestClient):
    response = client.post("/v1/books/", json={})
    assert response.status_code == 401


def test_read_books(client: TestClient, auth_headers: dict):
    for i in range(3):
        client.post(
            "/v1/books/",
            headers=auth_headers,
            json={
                "title": f"Book {i}",
                "author": "Tester",
                "published_date": "2022-01-01",
                "summary": "Summary",
                "genre": "Tech",
            },
        )
    response = client.get("/v1/books/", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_read_book_not_found(client: TestClient, auth_headers: dict):
    response = client.get("/v1/books/9999", headers=auth_headers)
    assert response.status_code == 404


def test_update_book(client: TestClient, auth_headers: dict):
    created = client.post(
        "/v1/books/",
        headers=auth_headers,
        json={
            "title": "Old",
            "author": "Someone",
            "published_date": "2020-01-01",
            "summary": "Old summary",
            "genre": "Drama",
        },
    )
    book_id = created.json()["id"]
    updated = client.put(
        f"/v1/books/{book_id}", headers=auth_headers, json={"title": "New Title"}
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "New Title"


def test_update_book_not_found(client: TestClient, auth_headers: dict):
    response = client.put(
        "/v1/books/9999", headers=auth_headers, json={"title": "Ghost"}
    )
    assert response.status_code == 404


def test_delete_book(client: TestClient, auth_headers: dict):
    created = client.post(
        "/v1/books/",
        headers=auth_headers,
        json={
            "title": "To Delete",
            "author": "Author",
            "published_date": "2021-01-01",
            "summary": "To remove",
            "genre": "History",
        },
    )
    book_id = created.json()["id"]
    deleted = client.delete(f"/v1/books/{book_id}", headers=auth_headers)
    assert deleted.status_code == 200

    confirm = client.get(f"/v1/books/{book_id}", headers=auth_headers)
    assert confirm.status_code == 404


def test_delete_book_not_found(client: TestClient, auth_headers: dict):
    response = client.delete("/v1/books/9999", headers=auth_headers)
    assert response.status_code == 404


def test_internal_server_error_simulation(
    client: TestClient, auth_headers: dict, monkeypatch
):
    from app.crud import book as book_crud

    def broken_get_books(*args, **kwargs):
        raise Exception("Simulated DB failure")

    monkeypatch.setattr(book_crud, "get_books", broken_get_books)

    response = client.get("/v1/books/", headers=auth_headers)
    assert response.status_code == 500
    assert "Internal Server Error" in response.text

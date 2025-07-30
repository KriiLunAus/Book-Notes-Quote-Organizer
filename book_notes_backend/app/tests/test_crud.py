def test_create_and_get_authors(client):
    response = client.post("/authors/", json={"name": "Test Author"})
    assert response.status_code == 200
    author_id = response.json()["id"]
    assert response.json()["name"] == "Test Author"
    assert author_id is not None


def test_delete_author(client):
    response = client.post("/authors/", json={"name": "Author to Delete"})
    assert response.status_code == 200
    author_id = response.json()["id"]

    delete_response = client.delete(f"/authors/{author_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/authors/{author_id}")
    assert get_response.status_code == 404


def test_update_author(client):
    create_resp = client.post("/authors/", json={"name": "Original Author"})
    author = create_resp.json()

    update_data = {"name": "Updated Author"}
    resp = client.put(f"/authors/{author['id']}", json=update_data)
    assert resp.status_code == 200
    updated_author = resp.json()
    assert updated_author["name"] == update_data["name"]
    assert updated_author["id"] == author["id"]


def test_create_and_get_books(client):
    response = client.post(
        "/books/",
        json={
            "title": "Test Book",
            "author_id": 1})
    assert response.status_code == 200
    book_id = response.json()["id"]
    assert response.json()["title"] == "Test Book"
    assert book_id is not None

    get_response = client.get("/books/")
    books = get_response.json()
    assert get_response.status_code == 200
    assert any(book["title"] == "Test Book" for book in books)


def test_update_book(client):
    author_resp = client.post("/authors/", json={"name": "Book Author"})
    author = author_resp.json()

    book_resp = client.post("/books/", json={"title": "Original Book", "author_id": author["id"]})
    book = book_resp.json()

    update_data = {"title": "Updated Book Title", "author_id": author["id"]}
    resp = client.put(f"/books/{book['id']}", json=update_data)
    assert resp.status_code == 200
    updated_book = resp.json()
    assert updated_book["title"] == update_data["title"]
    assert updated_book["author"]["id"] == author["id"]


def test_delete_book(client):
    response = client.post("/authors/", json={"name": "Test Author"})
    author_id = response.json()["id"]
    
    response = client.post(
        "/books/",
        json={
            "title": "Book to Delete",
            "author_id": author_id})
    assert response.status_code == 200
    book_id = response.json()["id"]

    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404


def test_create_and_get_quotes(client):
    response = client.post(
        "/quotes/",
        json={
            "content": "Test Quote",
            "book_id": 1})
    assert response.status_code == 200
    quote_id = response.json()["id"]
    assert response.json()["content"] == "Test Quote"
    assert quote_id is not None

    get_response = client.get("/quotes/")
    quotes = get_response.json()
    assert get_response.status_code == 200
    assert any(quote["content"] == "Test Quote" for quote in quotes)


def test_update_quote(client):
    author_resp = client.post("/authors/", json={"name": "Quote Author"})
    author = author_resp.json()

    book_resp = client.post("/books/", json={"title": "Quote Book", "author_id": author["id"]})
    book = book_resp.json()

    quote_resp = client.post("/quotes/", json={"content": "Original quote", "tags": "tag1, tag2", "book_id": book["id"]})
    quote = quote_resp.json()

    update_data = {"content": "Updated quote content", "tags": "tag3,tag4", "book_id": book["id"]}
    resp = client.put(f"/quotes/{quote['id']}", json=update_data)
    assert resp.status_code == 200
    updated_quote = resp.json()
    assert updated_quote["content"] == update_data["content"]
    expected_tags = ",".join(sorted([t.strip() for t in update_data["tags"].split(",")]))
    assert updated_quote["tags"] == expected_tags


def test_delete_quote(client):
    response = client.post(
        "/quotes/",
        json={
            "content": "Quote to Delete",
            "book_id": 1})
    assert response.status_code == 200
    quote_id = response.json()["id"]

    delete_response = client.delete(f"/quotes/{quote_id}")
    assert delete_response.status_code == 200

    get_response = client.get(f"/quotes/{quote_id}")
    assert get_response.status_code == 404


def test_create_tags(client):
    response = client.post(
        "/quotes/",
        json={
            "content": "Test Quote With Tags",
            "tags": "inspirational, bold",
            "book_id": 1})
    assert response.status_code == 200
    quote = response.json()

    expected_tags = set(tag.strip()
                        for tag in "inspirational, bold".split(","))
    actual_tags = set(tag.strip() for tag in quote["tags"].split(","))

    assert actual_tags == expected_tags


def test_get_all_tags(client):
    response = client.get("/quotes/tags/")
    assert response.status_code == 200
    tags = response.json()

    assert isinstance(tags, list)
    assert "inspirational" in tags
    assert "bold" in tags


def test_export_notes_to_markdown(client):
    response = client.get("/export/markdown/")
    assert response.status_code == 200
    markdown_content = response.text

    assert "# Book Notes & Quotes" in markdown_content
    assert "## 📚 Test Book" in markdown_content
    assert "Test Quote" in markdown_content


def test_export_notes_to_json(client):
    response = client.get("/export/json/")
    assert response.status_code == 200
    json_content = response.json()

    assert isinstance(json_content, list)
    assert len(json_content) > 0

    first_author = json_content[0]
    assert "author" in first_author
    assert "books" in first_author

    books = first_author["books"]
    assert any(book["title"] == "Test Book" for book in books)

    all_quotes = [quote for book in books for quote in book.get("quotes", [])]
    assert any(quote["content"] == "Test Quote" for quote in all_quotes)

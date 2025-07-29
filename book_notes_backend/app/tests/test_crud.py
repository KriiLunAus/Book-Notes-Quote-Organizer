def test_create_and_get_authors(client):
    response = client.post("/authors/", json={"name": "Test Author"})
    assert response.status_code == 200
    author_id = response.json()["id"]
    assert response.json()["name"] == "Test Author"
    assert author_id is not None

def test_create_and_get_books(client):
    response = client.post("/books/", json={"title": "Test Book", "author_id": 1})
    assert response.status_code == 200
    book_id = response.json()["id"]
    assert response.json()["title"] == "Test Book"
    assert book_id is not None

    get_response = client.get("/books/")
    books = get_response.json()
    assert get_response.status_code == 200
    assert any(book["title"] == "Test Book" for book in books)
    
    
def test_create_and_get_quotes(client):
    response = client.post("/quotes/", json={"content": "Test Quote", "book_id": 1})
    assert response.status_code == 200
    quote_id = response.json()["id"]
    assert response.json()["content"] == "Test Quote"
    assert quote_id is not None

    get_response = client.get("/quotes/")
    quotes = get_response.json()
    assert get_response.status_code == 200
    assert any(quote["content"] == "Test Quote" for quote in quotes)
    
def test_create_tags(client):
    response = client.post("/quotes/", json={"content": "Test Quote With Tags", "tags": "inspirational, bold", "book_id": 1})
    assert response.status_code == 200
    quote = response.json()
    
    expected_tags = set(tag.strip() for tag in "inspirational, bold".split(","))
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
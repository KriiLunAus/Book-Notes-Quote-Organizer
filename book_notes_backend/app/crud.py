from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas


def create_author(db: Session, author: schemas.AuthorCreate):
    new_author = models.Author(**author.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_authors(db: Session):
    return db.query(models.Author).all()


def create_book(db: Session, book: schemas.BookCreate):
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_books(db: Session):
    return db.query(models.Book).all()


def create_quote(db: Session, quote: schemas.QuoteCreate):
    cleaned_tags = ",".join(
        sorted({tag.strip() for tag in quote.tags.split(",") if tag.strip()})
    )

    new_quote = models.Quote(
        content=quote.content,
        tags=cleaned_tags,
        book_id=quote.book_id
    )
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return new_quote


def get_quotes(db: Session, tags: str = None):
    query = db.query(models.Quote)
    if tags:
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        tag_filters = [models.Quote.tags.ilike(f"%{tag}%") for tag in tag_list]
        query = query.filter(or_(*tag_filters))
    return query.all()


def get_all_tags(db: Session):
    all_quotes = db.query(models.Quote.tags).all()
    tag_set = set()

    for (tag_string,) in all_quotes:
        if tag_string:
            tags = [tag.strip()
                    for tag in tag_string.split(",") if tag.strip()]
            tag_set.update(tags)

    return sorted(tag_set)


def export_notes_to_markdown(db: Session) -> str:
    authors = db.query(models.Author).all()
    books = db.query(models.Book).all()
    quotes = db.query(models.Quote).all()

    author_lookup = {author.id: author.name for author in authors}
    book_quotes = {}
    for quote in quotes:
        book_quotes.setdefault(quote.book_id, []).append(quote)

    md = "# Book Notes & Quotes\n\n"

    for book in books:
        md += f"## 📚 {book.title}\n"
        md += f"**Author:** {author_lookup.get(book.author_id, 'Unknown')}\n\n"

        book_qs = book_quotes.get(book.id, [])
        if book_qs:
            md += "### Quotes:\n"
            for q in book_qs:
                tag_line = f" _({q.tags})_" if q.tags else ""
                md += f"- {q.content.strip()}{tag_line}\n"
            md += "\n"
        else:
            md += "_No quotes yet._\n\n"

    return md


def export_notes_to_json(db: Session):
    authors = db.query(models.Author).all()
    books = db.query(models.Book).all()
    quotes = db.query(models.Quote).all()

    book_lookup = {}
    for book in books:
        book_lookup[book.id] = {
            "title": book.title,
            "author_id": book.author_id,
            "quotes": []
        }

    for quote in quotes:
        if quote.book_id in book_lookup:
            book_lookup[quote.book_id]["quotes"].append({
                "content": quote.content,
                "tags": quote.tags
            })

    # Nest books under authors
    result = []
    for author in authors:
        author_books = []
        for book in books:
            if book.author_id == author.id:
                b = book_lookup.get(book.id)
                if b:
                    author_books.append({
                        "title": b["title"],
                        "quotes": b["quotes"]
                    })
        result.append({
            "author": author.name,
            "books": author_books
        })

    return result

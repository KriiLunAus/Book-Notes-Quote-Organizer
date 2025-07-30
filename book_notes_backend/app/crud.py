from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from fastapi import HTTPException
from . import models, schemas


def create_author(db: Session, author: schemas.AuthorCreate):
    new_author = models.Author(**author.model_dump())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_authors(db: Session):
    return db.query(models.Author).all()


def get_author(db: Session, author_id: int):
    return db.query(
        models.Author).filter(
        models.Author.id == author_id).first()


def update_author(
        db: Session,
        author_id: int,
        updated_data: schemas.AuthorCreate):
    author = db.query(
        models.Author).filter(
        models.Author.id == author_id).first()
    if not author:
        return None
    for key, value in updated_data.model_dump().items():
        setattr(author, key, value)
    db.commit()
    db.refresh(author)
    return author


def delete_author(db: Session, author_id: int):
    author = db.query(
        models.Author).filter(
        models.Author.id == author_id).first()
    if not author:
        return None
    db.delete(author)
    db.commit()
    return author


def create_book(db: Session, book: schemas.BookCreate):
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_books(db: Session):
    return db.query(models.Book).all()


def get_book(db: Session, book_id: int):
    return db.query(
        models.Book).options(
        joinedload(
            models.Book.author)).filter(
                models.Book.id == book_id).first()


def update_book(db: Session, book_id: int, updated_data: schemas.BookCreate):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        return None
    for key, value in updated_data.model_dump().items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int):
    book = db.query(
        models.Book).options(
        joinedload(
            models.Book.author)).filter(
                models.Book.id == book_id).first()
    if not book:
        return None

    response_data = schemas.BookOut(
        id=book.id,
        title=book.title,
        author=schemas.AuthorNested(
            id=book.author.id,
            name=book.author.name
        )
    )

    db.delete(book)
    db.commit()

    return response_data


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


def get_quote(db: Session, quote_id: int):
    quote = db.query(models.Quote).filter(models.Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    book = quote.book
    author = book.author if book else None

    return schemas.QuoteOut(
        id=quote.id,
        content=quote.content,
        tags=quote.tags,
        book=schemas.BookOut(
            id=book.id,
            title=book.title,
            author=schemas.AuthorNested(
                id=author.id,
                name=author.name
            )
        )
    )


def update_quote(
        db: Session,
        quote_id: int,
        updated_data: schemas.QuoteCreate):
    quote = db.query(models.Quote).filter(models.Quote.id == quote_id).first()
    if not quote:
        return None
    cleaned_tags = ",".join(
        sorted({tag.strip() for tag in updated_data.tags.split(",")
                if tag.strip()})
    )
    update_fields = updated_data.model_dump()
    update_fields["tags"] = cleaned_tags
    for key, value in update_fields.items():
        setattr(quote, key, value)
    db.commit()
    db.refresh(quote)
    return quote


def delete_quote(db: Session, quote_id: int):
    quote = db.query(models.Quote).filter(models.Quote.id == quote_id).first()
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")

    book = quote.book
    author = book.author if book else None

    response_data = schemas.QuoteOut(
        id=quote.id,
        content=quote.content,
        tags=quote.tags,
        book=schemas.BookOut(
            id=book.id,
            title=book.title,
            author=schemas.AuthorNested(
                id=author.id,
                name=author.name
            )
        )
    )

    db.delete(quote)
    db.commit()
    return response_data


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

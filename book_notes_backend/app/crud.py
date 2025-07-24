from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas


def create_author(db: Session, author: schemas.AuthorCreate):
    new_author = models.Author(**author.dict())
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_authors(db: Session):
    return db.query(models.Author).all()


def create_book(db: Session, book: schemas.BookCreate):
    new_book = models.Book(**book.dict())
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

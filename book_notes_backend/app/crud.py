from sqlalchemy.orm import Session
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
    new_quote = models.Quote(**quote.dict())
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return new_quote


def get_quotes(db: Session, tag: str = None):
    query = db.query(models.Quote)
    if tag:
        query = query.filter(models.Quote.tags.ilike(f"%{tag}%"))
    return query.all()

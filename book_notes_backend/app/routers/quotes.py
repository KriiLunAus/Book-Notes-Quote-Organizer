from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/quotes", tags=["Quotes"])


@router.post("/", response_model=schemas.QuoteOut)
def create_quote(
    quote: schemas.QuoteCreate,
    db: Session = Depends(
        database.get_db)):
    return crud.create_quote(db, quote)


@router.get("/", response_model=list[schemas.QuoteOut])
def get_quotes(
    tags: str = Query(None),
    db: Session = Depends(
        database.get_db)):
    return crud.get_quotes(db, tags=tags)


@router.get("/tags", response_model=list[str])
def list_tags(db: Session = Depends(database.get_db)):
    return crud.get_all_tags(db)


@router.get("/{quote_id}", response_model=schemas.QuoteOut)
def get_quote(
    quote_id: int,
    db: Session = Depends(
        database.get_db)):
    quote = crud.get_quote(db, quote_id)
    return quote


@router.delete("/{quote_id}", response_model=schemas.QuoteOut)
def delete_quote(
        quote_id: int,
        db: Session = Depends(database.get_db)):
    return crud.delete_quote(db, quote_id)

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database, models

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


@router.put("/{quote_id}", response_model=schemas.QuoteOut)
def update_quote(quote_id: int, quote_update: schemas.QuoteCreate, db: Session = Depends(database.get_db)):
    quote = crud.update_quote(db, quote_id, quote_update)
    if not quote:
        raise HTTPException(status_code=404, detail="Quote not found")
    
    quote_full = db.query(models.Quote).filter(models.Quote.id == quote_id).first()
    if not quote_full:
        raise HTTPException(status_code=404, detail="Quote not found after update")
    return quote_full


@router.delete("/{quote_id}", response_model=schemas.QuoteOut)
def delete_quote(
        quote_id: int,
        db: Session = Depends(database.get_db)):
    return crud.delete_quote(db, quote_id)

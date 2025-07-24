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
def get_quotes(tag: str = Query(None), db: Session = Depends(database.get_db)):
    return crud.get_quotes(db, tag=tag)

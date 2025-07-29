from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.post("/", response_model=schemas.AuthorOut)
def create_author(
    author: schemas.AuthorCreate,
    db: Session = Depends(
        database.get_db)):
    return crud.create_author(db, author)


@router.get("/", response_model=list[schemas.AuthorOut])
def get_authors(db: Session = Depends(database.get_db)):
    return crud.get_authors(db)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

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


@router.get("/{author_id}", response_model=schemas.AuthorOut)
def get_author(
    author_id: int,
    db: Session = Depends(
        database.get_db)):
    author = crud.get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.put("/{author_id}", response_model=schemas.AuthorOut)
def update_author(
    author_id: int,
    author_update: schemas.AuthorCreate,
    db: Session = Depends(
        database.get_db)):
    author = crud.update_author(db, author_id, author_update)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.delete("/{author_id}", response_model=schemas.AuthorOut)
def delete_author(
        author_id: int,
        db: Session = Depends(database.get_db)):
    return crud.delete_author(db, author_id)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=schemas.BookOut)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(
        database.get_db)):
    return crud.create_book(db, book)


@router.get("/", response_model=list[schemas.BookOut])
def read_books(db: Session = Depends(database.get_db)):
    return crud.get_books(db)


@router.get("/{book_id}", response_model=schemas.BookOut)
def read_book(
        book_id: int,
        db: Session = Depends(database.get_db)):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=schemas.BookOut)
def update_book(
    book_id: int,
    book_update: schemas.BookCreate,
    db: Session = Depends(
        database.get_db)):
    book = crud.update_book(db, book_id, book_update)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{book_id}", response_model=schemas.BookOut)
def delete_book(
        book_id: int,
        db: Session = Depends(database.get_db)):
    return crud.delete_book(db, book_id)

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import crud, database

router = APIRouter(prefix="/export/json", tags=["JSON Export"])


@router.get("/", response_class=JSONResponse)
def export_json(db: Session = Depends(database.get_db)):
    data = crud.export_notes_to_json(db)
    return JSONResponse(content=data)

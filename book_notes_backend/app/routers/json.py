from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .. import crud, database

router = APIRouter()

@router.get("/export/json", response_class=JSONResponse)
def export_json(db: Session = Depends(database.get_db)):
    data = crud.export_notes_to_json(db)
    return JSONResponse(content=data)
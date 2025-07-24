from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.responses import Response
from .. import crud, database

router = APIRouter(prefix="/export/markdown", tags=["Markdown"])

@router.get("/", response_class=Response)
def export_markdown(db: Session = Depends(database.get_db)):
    content = crud.export_notes_to_markdown(db)
    return Response(
        content=content,
        media_type="text/markdown",
        headers={
            "Content-Disposition": "attachment; filename=book_notes.md"
        }
    )
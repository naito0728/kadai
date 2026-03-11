from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 検索
@router.post("/search")
def search_knowledge(request: schemas.SearchRequest, db: Session = Depends(get_db)):

    docs = db.query(models.Document).filter(
        models.Document.category_id == request.category_id,
        models.Document.content.contains(request.query),
    ).all()

    if docs:
        return {
            "result": "success",
            "documents": [
                {
                    "title": d.title,
                    "content": d.content
                }
                for d in docs
            ]
        }

    return {"result": "not_found"}
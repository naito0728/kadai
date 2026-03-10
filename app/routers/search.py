from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .. import models, schemas

router = APIRouter()
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 検索
@router.post("/search")
def search_knowledge(request: schemas.SearchRequest, credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):

    token = credentials.credentials

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
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

# ログ登録
@router.post("/logs")
def create_log(log: schemas.SearchLogCreate, db: Session = Depends(get_db)):

    log = models.SearchLog(
        query=log.query,
        category_id=log.category_id,
        result=log.result
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return {"message": "log saved"}
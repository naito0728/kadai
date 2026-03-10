from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/documents")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 一覧表示
@router.get("/")
def get_documents(db: Session = Depends(get_db)):
    return db.query(models.Document).all()

# 追加
@router.post("/")
def create_document(doc: schemas.DocumentCreate, db: Session = Depends(get_db)):

    new_doc = models.Document(
        category_id=doc.category_id,
        title=doc.title,
        content=doc.content
    )

    db.add(new_doc)
    db.commit()

    return {"message": "created"}

# id指定でフィルタリング
@router.put("/{id}")
def update_document(id: int, doc: schemas.DocumentUpdate, db: Session = Depends(get_db)):

    document = db.query(models.Document).filter(models.Document.id == id).first()

    document.category_id = doc.category_id
    document.title = doc.title
    document.content = doc.content

    db.commit()

    return {"message": "updated"}

# 削除
@router.delete("/{id}")
def delete_document(id: int, db: Session = Depends(get_db)):

    document = db.query(models.Document).filter(models.Document.id == id).first()

    db.delete(document)
    db.commit()

    return {"message": "deleted"}
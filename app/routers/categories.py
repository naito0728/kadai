from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas

router = APIRouter(prefix="/categories")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 一覧表示
@router.get("/")
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

# 登録
@router.post("/")
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):

    new_category = models.Category(name=category.name)

    db.add(new_category)
    db.commit()

    return {"message": "created"}

# id指定でフィルタリング
@router.put("/{id}")
def update_category(id: int, category: schemas.CategoryUpdate, db: Session = Depends(get_db)):

    cat = db.query(models.Category).filter(models.Category.id == id).first()

    cat.name = category.name
    db.commit()

    return {"message": "updated"}

# 削除
@router.delete("/{id}")
def delete_category(id: int, db: Session = Depends(get_db)):

    cat = db.query(models.Category).filter(models.Category.id == id).first()

    db.delete(cat)
    db.commit()

    return {"message": "deleted"}
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models, schemas
from .auth import create_access_token
import secrets

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ユーザ登録
@router.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user = models.User(
        user_id=user.user_id,
        user_name=user.user_name,
        user_role=user.user_role
    )

    db.add(new_user)
    db.commit()

    return {"message": "user created"}


# JWTトークン発行
@router.post("/login", response_model=schemas.TokenResponse)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.user_id == user.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="ユーザIDが存在しません"
        )

    token = create_access_token(
        data={"user_id": user.user_id}
    )

    return {
        "access_token": token,
        "user_name": user.user_name
    }


# APIキー発行
@router.post("/apikey", response_model=schemas.ApiKeyResponse)
def create_api_key(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.user_id == user.user_id
    ).first()

    if not db_user:
        return {"error": "user not found"}

    api_key = secrets.token_hex(32)

    db_user.api_key = api_key
    db.commit()

    return {"api_key": api_key}
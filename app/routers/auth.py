from jose import jwt
from datetime import datetime, timedelta
from fastapi import Header, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
import jwt

router = APIRouter()

SECRET_KEY = "secretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# トークン発行
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

# APIキー発行
def verify_api_key(api_key: str = Header(...), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.api_key == api_key
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return user

@router.post("/login")
def login(user_id: str, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.user_id == user_id
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    payload = {
        "user_id": user.user_id,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "token_type": "bearer"
    }